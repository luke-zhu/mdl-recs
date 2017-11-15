# -*- coding: utf-8 -*-
import scrapy

from data_capture.items import RecommendationItem, ReviewItem, ShowMetadataItem


class ShowSpider(scrapy.Spider):
    name = "show"
    allowed_domains = ["mydramalist.com"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        # 'ITEM_PIPELINES': {'data_capture.pipelines.CommentPipeline': 300 }
        # 'CLOSESPIDER_ERRORCOUNT': 1,
    }

    def __init__(self):
        super().__init__()

    def start_requests(self):
        # Todo
        pass

    def parse(self, response: scrapy.http.Response):
        """Takes in a response from a show page
        (e.g. https://mydramalist.com/9025-nirvana-in-fire)
        and yields the data described in items.py
        """
        self.parse_metadata(response)
        self.parse_review(response)
        self.parse_rec(response)

    def parse_metadata(self, response: scrapy.http.Response):
        # Todo: shell https://mydramalist.com/9025-nirvana-in-fire
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

        metadata['duration'] = int(field_selectors.css('li:nth-child(7)::text')[0].extract().split()[0])

        metadata['average_score'] = int(10 * float(field_selectors.css('li:nth-child(1)::text')[1].extract().strip()))
        metadata['num_users_rated'] = int(response.css('[itemprop=ratingCount]::attr(content)')[0].extract())
        metadata['num_users_watched'] = int(response.css('.hfs b::text')[1].extract().replace(',', ''))

        metadata['genres'] = response.css('.show-genres a::text').extract()
        metadata['country'] = field_selectors.css('li:nth-child(2)::text')[0].extract().strip()
        metadata['num_episodes'] = int(field_selectors.css('li:nth-child(3)::text')[0].extract().strip())
        metadata['rank'] = int(field_selectors.css('li:nth-child(2)::text')[1].extract()[2:])
        metadata['popularity'] = int(field_selectors.css('li:nth-child(3)::text')[1].extract()[2:])
        yield metadata

    def parse_review(self, response: scrapy.http.Response):
        # Todo: https://mydramalist.com/9025-nirvana-in-fire/reviews
        review = ReviewItem()
        review['id'] = ''
        review['url'] = ''
        review['show_id'] = ''
        review['show_title'] = ''
        review['date_posted'] = ''
        review['num_votes'] = ''
        review['overall_score'] = 0
        review['story_score'] = 0
        review['acting_score'] = 0
        review['music_score'] = 0
        review['rewatch_score'] = 0
        review['review_text'] = ''
        yield review

    def parse_rec(self, response: scrapy.http.Response):
        # Todo: https://mydramalist.com/9025-nirvana-in-fire/recs
        rec = RecommendationItem()
        rec['id'] = ''
        rec['url'] = ''
        rec['show1_id'] = ''
        rec['show2_id'] = ''
        rec['show1_title'] = ''
        rec['show2_title'] = ''
        rec['date_posted'] = ''
        rec['num_votes'] = ''
        rec['rec_text'] = ''
        yield rec

    def parse_comments(self, response: scrapy.http.Response):
        # Todo: Migrate code from CommentSpider
        pass
