# -*- coding: utf-8 -*-
import logging
from random import shuffle

import scrapy
import json
from urllib.parse import parse_qs


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
        'LOG_FILE': 'logs/comment_spider.log',
        # custom logging not working, use command line options
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 0.5,
        # 'CLOSESPIDER_ERRORCOUNT': 1,
    }

    def start_requests(self) -> iter:
        """Returns urls of the form https://mydramalist.com/9025 from the
        number 1 up to 26000"""
        visited_ids: set = self.load_visited()
        unvisited_ids = list(set(range(1, 26000)) - visited_ids)
        shuffle(unvisited_ids)
        self.log('Number of unvisited shows: {}'.format(len(unvisited_ids)),
                 level=logging.INFO)
        return (scrapy.Request('https://mydramalist.com/{}'.format(id))
                for id in unvisited_ids)

    @classmethod
    def load_visited(cls) -> set:
        """Loads a state.txt file to the item pipeline and to the
        spider (for start requests)"""
        visited = set()
        try:
            # Used in pipelines.py as well
            with open('data/comments/state.txt') as f:
                f.readline()  # First line should contain file_index info
                for line in f:
                    show_id = json.loads(line)['show_id']
                    # Todo: Error message for state.txt in wrong format
                    visited.add(int(show_id))
        except FileNotFoundError:
            pass
        return visited

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
