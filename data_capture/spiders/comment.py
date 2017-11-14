# -*- coding: utf-8 -*-
import scrapy
import numpy as np

import json

from urllib.parse import parse_qs

import time


class CommentSpider(scrapy.Spider):
    """Collects comment thread data from mydramalist.com show threads.

    To collect the comments, run the following command in your terminal:

        scrapy crawl comment --logfile logs/comment_spider.log -L INFO

    This should be run in the root workspace directory.
    """
    name = 'comment'
    allowed_domains = ['mydramalist.com']
    # Todo: Check for when this prefix_url will be changed
    prefix_url = 'https://beta4v.mydramalist.com/v1/threads?&c=title&t='

    custom_settings = {
        'LOG_LEVEL': 'INFO',  # Not working right now, use the terminal command
        'LOG_FILE': 'logs/comment_spider.log',  # Not working right now
        'DOWNLOAD_DELAY': 2,
    }

    def start_requests(self):
        """Returns urls of the form https://mydramalist.com/9025 from the
        number 1 up to 26000"""
        ids = np.random.permutation(
            26000)  # Todo: Implement stopping after multiple 404s
        # Returns a generator
        return (scrapy.Request('https://mydramalist.com/{}'.format(id))
                for id in ids)

    def parse(self, response: scrapy.http.Response):
        """Takes in a response from a show url of the form
        https://mydramalist.com/9025-nirvana-in-fire
        and yields a request to the show's comments.
        """
        show_id = response.url[24:].split('-')[0]
        next_url = self.prefix_url + show_id + '&page=1'
        yield scrapy.Request(next_url,
                             callback=self.parse_comments)

    def parse_comments(self, response: scrapy.http.Response):
        """Takes in a response from a comment thread page with url
        ending in &page=SOME_NUMBERand  yields the JSON in the
        page. Also yields a request to the next page, if it exists.
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
            yield scrapy.Request(response.urljoin(next_url),
                                 callback=self.parse_comments)
