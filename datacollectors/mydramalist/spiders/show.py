# -*- coding: utf-8 -*-
import json
from typing import Generator
from urllib.parse import parse_qs

import scrapy
import scrapy.utils.log

from ..items import (RecommendationItem, ReviewItem, ShowItem)


class ShowSpider(scrapy.Spider):
    """Collects drama and movie data, given a file of show ids shows_ids.txt
    Run the spider by calling

        scrapy crawl show
    """
    name = "show"
    allowed_domains = ["mydramalist.com"]
    custom_settings = {'DOWNLOAD_DELAY': 1,  # 'CLOSESPIDER_ERRORCOUNT': 10,
                       'ITEM_PIPELINES': {'mydramalist.pipelines.PaginationPipeline': 300}, }
    base_url = 'https://www.mydramalist.com/'

    comments_endpoint = 'https://beta4v.mydramalist.com/v1/threads?&c=title&t='

    start_urls = ['https://mydramalist.com/search?adv=titles']

    def __init__(self, test=False, *args, **kwargs):
        if not test:
            scrapy.utils.log.configure_logging(
                {'LOG_LEVEL': 'INFO', 'LOG_FILE': 'logs/show.log', 'LOG_ENABLED': True, })
        super().__init__(*args, **kwargs)

    def parse(self, response: scrapy.http.Response) -> Generator:
        """Takes in a response from a start url and yields the data from each of the
        up to 20 shows in the main list.
        """
        for url in response.css('.title a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_show)

        next_url = response.css('.next a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url))

    def parse_show(self, response: scrapy.http.Response) -> Generator:
        """Takes in a response from a show page
        (e.g. https://mydramalist.com/9025-nirvana-in-fire)
        and yields the metadata, reviews, and recs from
        the
        """
        yield from self.parse_metadata(response)
        yield scrapy.Request(response.url + '/reviews', callback=self.parse_reviews)
        yield scrapy.Request(response.url + '/recs', callback=self.parse_recommendations)
        show_id = response.url[24:].split('-')[0]
        yield scrapy.Request(self.comments_endpoint + show_id + '&page=1',
                             callback=self.parse_comments)

    # Todo: Split this method into separate parts
    def parse_metadata(self, response: scrapy.http.Response) -> Generator[ShowItem, None, None]:
        """Takes in a response from a show homepage
        (e.g. https://mydramalist.com/9025-nirvana-in-fire) and
        yields the contained show metadata.

        Test urls:
        https://mydramalist.com/9025-nirvana-in-fire
        https://mydramalist.com/4517-miracle-in-cell-no.-7
        https://mydramalist.com/24676-thief-actor
        """
        metadata = ShowItem()

        metadata['id'] = int(response.css('meta[property*=rid]::attr(content)')[0].extract())
        metadata['url'] = response.url

        metadata['main_title'] = response.css('meta[property*=title]::attr(content)')[0].extract()

        details_box = response.css('div.box')[0]
        metadata['type'] = details_box.css('b::text')[0].extract()[:-1]
        metadata['content_rating'] = details_box.css('li.content-rating::text')[0].extract().strip()
        # metadata['status'] Todo
        for list_item in details_box.css('li'):
            if list_item.css('b::text').extract_first() == 'Duration:':
                metadata['duration'] = list_item.css('li::text')[0].extract().strip()
            if list_item.css('b::text').extract_first() == 'Episodes:':
                metadata['episodes'] = int(list_item.css('li::text')[0].extract().strip())
            if list_item.css('b::text').extract_first() == 'Country:':
                metadata['country'] = list_item.css('li::text')[0].extract().strip()
            if list_item.css('b::text').extract_first() == 'Network:':
                metadata['network'] = list_item.css('a::text')[0].extract().strip()
            if list_item.css('b::text').extract_first() in ('Release Date:', 'Aired:', 'Airs:'):
                date_strings = list_item.css('li::text')[0].extract().split('-')
                metadata['release_date'] = date_strings[0].strip()
                try:
                    # Note: This may equal the string '?'
                    metadata['end_date'] = date_strings[1].strip()
                except IndexError:
                    metadata['end_date'] = None

        metadata['genres'] = response.css('.show-genres a::text').extract()
        metadata['tags'] = response.css('.show-tags a::text').extract()

        statistics_box = response.css('div.box')[1]
        metadata['rank'] = int(statistics_box.css('li:nth-child(2)::text')[0].extract()[2:])
        metadata['popularity'] = int(statistics_box.css('li:nth-child(3)::text')[0].extract()[2:])

        main_box = response.css('#show-detailsxx')
        for list_item in main_box.css('li'):
            if list_item.css('b::text').extract_first() == 'Native title:':
                metadata['native_title'] = list_item.css('li::text')[0].extract().strip()
            if list_item.css('b::text').extract_first() == 'Also Known as:':
                alts = list_item.css('li::text')[0].extract()
                metadata['alt_titles'] = [title.strip() for title in alts.split(';') if title.strip()]

        metadata['synopsis'] = ''.join(main_box.css('.show-synopsis ::text').extract())
        # Todo:
        # metadata['related_titles']
        # Todo:
        # cast
        try:
            score = main_box.css('[itemprop=ratingValue]::text').extract_first()  # Can equal 'N/A'
            metadata['score'] = int(10 * float(score))
        except (ValueError, TypeError):
            metadata['score'] = None
        try:
            ratings = main_box.css('[itemprop=ratingCount]::attr(content)').extract_first()
            metadata['ratings'] = int(ratings)
        except (ValueError, TypeError):
            metadata['ratings'] = 0
        metadata['members'] = int(main_box.css('.hfs b::text')[1].extract().replace(',', ''))

        yield metadata

    def parse_reviews(self, response: scrapy.http.Response) -> Generator[ReviewItem, None, None]:
        """Takes in a response from a user review page and
        (e.g. https://mydramalist.com/9025-nirvana-in-fire/reviews)
        yields the contained review data.
        """
        for selector in response.css('.review'):
            review = ReviewItem()
            review['id'] = int(selector.css('.review::attr(id)')[0].extract()[7:])
            review['url'] = selector.css('.actions a::attr(href)')[0].extract()
            review['show_id'] = response.css('[property*=rid]::attr(content)')[0].extract()
            review['show_title'] = response.css('[property*=title]::attr(content)')[0].extract()
            review['post_date'] = selector.css('.datetime::text')[0].extract()
            review['votes'] = int(selector.css('[class*=stats-helpful]::text')[0].extract())

            review['overall_score'] = int(float(selector.css('.score::text')[0].extract()) * 10)
            subscores = selector.css('.p-l-md::text').extract()
            review['story_score'] = int(float(subscores[0]) * 10)
            review['acting_score'] = int(float(subscores[1]) * 10)
            review['music_score'] = int(float(subscores[2]) * 10)
            review['rewatch_score'] = int(float(subscores[3]) * 10)
            review['text'] = ''.join(
                selector.css('.review-body::text,.review-bodyfull-read::text').extract())
            yield review

            next_url = response.css('.next a::attr(href)').extract_first()
            if next_url:
                yield scrapy.Request(response.urljoin(next_url), callback=self.parse_reviews)

    def parse_recommendations(self, response: scrapy.http.Response) -> Generator[
        RecommendationItem, None, None]:
        """Takes in a response from a show recommendation page
        (e.g. https://mydramalist.com/9025-nirvana-in-fire/recs)
        and yields the contained user recs.
        """
        url = response.url
        show_id1 = response.css('[property*=rid]::attr(content)')[0].extract()
        for selector in response.css('[id*=rec_]'):
            rec = RecommendationItem()
            rec['id'] = selector.css('[id*=rec_]::attr(id)')[0].extract()[4:]
            rec['url'] = url
            show_ids = {show_id1, selector.css('::attr(data-id)')[0].extract()}
            rec['show_ids'] = sorted(list(show_ids))

            rec['votes'] = selector.css('.like-cnt::text')[0].extract()
            rec['text'] = ''.join(selector.css('.recs-body::text').extract())
            yield rec

        next_url = response.css('.next a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse_recommendations)

    def parse_comments(self, response: scrapy.http.Response) -> Generator[dict, None, None]:
        """Takes in a response from a comment thread page
        (e.g. https://beta4v.mydramalist.com/v1/threads?&c=title&t=9025&page=1)
        and yields. Also yields a request to the next comment
        page, if more comments do exists.
        """
        data = json.loads(response.body)
        show_id = parse_qs(response.url)['t'][0]
        data['show_id'] = show_id
        data['url'] = response.url
        yield data
        if data['has_more']:
            parts = response.url.split('=')
            parts[-1] = str(int(parts[-1]) + 1)
            next_url = '='.join(parts)
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse_comments)
