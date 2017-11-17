# -*- coding: utf-8 -*-
import json
import logging
from urllib.parse import parse_qs

import scrapy
from scrapy.utils.log import configure_logging

from data_collection.items import RecommendationItem, ReviewItem, ShowMetadataItem


class ShowSpider(scrapy.Spider):
    """Collects drama and movie data, given a file of show ids shows_ids.txt
    Run the spider by calling

        scrapy crawl somespider -s JOBDIR=crawls/somespider-1
    """
    name = "show"
    allowed_domains = ["mydramalist.com"]
    custom_settings = {'DOWNLOAD_DELAY': 1,
                       'ITEM_PIPELINES': {'data_capture.pipelines.PaginationPipeline': 300},
                       'CLOSESPIDER_ERRORCOUNT': 10, }
    base_url = 'https://www.mydramalist.com/'
    comments_endpoint = 'https://beta4v.mydramalist.com/v1/threads?&c=title&t='

    def __init__(self, *args, **kwargs):
        configure_logging(
            {'LOG_LEVEL': 'INFO', 'LOG_FILE': 'logs/show_spider.log', 'LOG_ENABLED': True, })
        super().__init__(*args, **kwargs)

    def start_requests(self):
        """Yields a generator of requests to show homepages using
        ids in the file data/show_ids.txt"""
        # Todo: Make show_ids.txt public, keep the ids updated as new shows are added
        show_ids = []
        with open('data/show_ids.txt') as f:
            for line in f:
                show_ids.append(line.strip())
        return (scrapy.Request('https://www.mydramalist.com/' + id) for id in show_ids)

    def parse(self, response: scrapy.http.Response):
        """Takes in a response from a show page
        (e.g. https://mydramalist.com/9025-nirvana-in-fire)
        and yields the data described in items.py
        """
        self.parse_metadata(response)
        yield scrapy.Request(response.url + '/reviews', callback=self.parse_reviews)
        yield scrapy.Request(response.url + '/recs', callback=self.parse_recommendations)
        # Todo: Uncomment when done with current scrape
        # show_id = response.url[24:].split('-')[0]
        # yield scrapy.Request(self.comments_endpoint + show_id + '&page=1',
        #                      callback=self.parse_recommendations)

    def parse_metadata(self, response: scrapy.http.Response):
        """Takes in a response from a show homepage
        (e.g. https://mydramalist.com/9025-nirvana-in-fire) and
        yields the contained show metadata.
        """
        field_selectors = response.css('.list-item.p-a-0')
        metadata = ShowMetadataItem()
        metadata['id'] = response.css('[data-type=title]::attr(data-id)')[0].extract()
        metadata['url'] = response.url
        metadata['title'] = field_selectors.css('[itemprop=name]::text')[0].extract()
        date_strings = field_selectors.css('li:nth-child(4)::text')[0].extract().split('-')
        metadata['date_started'] = date_strings[0].strip()
        try:
            metadata['date_ended'] = date_strings[1].strip()
        except IndexError:
            metadata['date_ended'] = ''
        metadata['duration'] = int(
            field_selectors.css('li:nth-child(7)::text')[0].extract().split()[0])
        metadata['average_score'] = int(
            10 * float(field_selectors.css('li:nth-child(1)::text')[1].extract().strip()))
        metadata['num_users_rated'] = int(
            response.css('[itemprop=ratingCount]::attr(content)')[0].extract())
        metadata['num_users_watched'] = int(
            response.css('.hfs b::text')[1].extract().replace(',', ''))
        metadata['genres'] = response.css('.show-genres a::text').extract()
        metadata['country'] = field_selectors.css('li:nth-child(2)::text')[0].extract().strip()
        metadata['num_episodes'] = int(
            field_selectors.css('li:nth-child(3)::text')[0].extract().strip())
        metadata['rank'] = int(field_selectors.css('li:nth-child(2)::text')[1].extract()[2:])
        metadata['popularity'] = int(field_selectors.css('li:nth-child(3)::text')[1].extract()[2:])

        yield metadata

    def parse_reviews(self, response: scrapy.http.Response):
        """Takes in a response from a user review page and
        (e.g. https://mydramalist.com/9025-nirvana-in-fire/reviews)
        yields the contained review data.
        """
        for selector in response.css('.review'):
            review = ReviewItem()
            review['id'] = selector.css('.review::attr(id)').extract_first()[7:]
            review['url'] = response.url  # TODO: the url of the review
            review['show_id'] = response.css('[property*=rid]::attr(content)').extract_first()
            review['show_title'] = response.css('[property*=title]::attr(content)').extract_first()
            review['date_posted'] = selector.css('.datetime::text').extract_first()
            review['num_votes'] = int(selector.css('[class*=stats-helpful]::text').extract_first())
            review['overall_score'] = int(float(selector.css('.score::text').extract_first()) * 10)
            subscores = selector.css('.p-l-md::text').extract()
            review['story_score'] = int(float(subscores[0]) * 10)
            review['acting_score'] = int(float(subscores[1]) * 10)
            review['music_score'] = int(float(subscores[2]) * 10)
            review['rewatch_score'] = int(float(subscores[3]) * 10)
            review['review_text'] = ''.join(selector.css('.review-body::text').extract())
            yield review

    def parse_recommendations(self, response: scrapy.http.Response):
        """Takes in a response from a show recommendation page
        (e.g. https://mydramalist.com/9025-nirvana-in-fire/recs)
        and yields the contained user recs.
        """
        for selector in response.css('[id*=rec_]'):
            rec = RecommendationItem()
            rec['id'] = selector.css('[id*=rec_]::attr(id)').extract_first()[4:]
            rec['url'] = response.url  # Todo: Url of more recs
            show_ids = {response.css('[property*=rid]::attr(content)').extract_first(),
                        selector.css('::attr(data-id)').extract_first()}
            rec['show_ids'] = sorted(list(show_ids))
            rec['num_votes'] = selector.css('.like-cnt::text').extract_first()
            rec['rec_text'] = ''.join(selector.css('.recs-body::text').extract())
            yield rec

    def parse_comments(self, response: scrapy.http.Response):
        """Takes in a response from a comment thread page
        (e.g. https://beta4v.mydramalist.com/v1/threads?&c=title&t=9025&page=1)
        and yields. Also yields a request to the next comment
        page, if more comments do exists.
        """
        data = json.loads(response.body)
        show_id = parse_qs(response.url)['t'][0]
        data['show_id'] = show_id
        data['url'] = response.url  # Include the url for future reference
        yield data
        if data['has_more']:
            parts = response.url.split('=')
            parts[-1] = str(int(parts[-1]) + 1)  # Last token must be a number
            next_url = '='.join(parts)
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse_comments)
