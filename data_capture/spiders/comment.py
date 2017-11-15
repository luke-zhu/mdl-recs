# -*- coding: utf-8 -*-
import logging
import os

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
    state = set() # This represents the visited show_ids

    custom_settings = {
        'LOG_LEVEL': 'INFO',  # Not working right now, use the terminal command
        'LOG_FILE': 'logs/comment_spider.log',  # Not working right now
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_ERRORCOUNT': 1,
    }

    def start_requests(self):
        """Returns urls of the form https://mydramalist.com/9025 from the
        number 1 up to 26000"""
        unvisited_ids = set(range(1, 26000))
        self.load_state()
        if self.state:
            unvisited_ids -= self.state
        self.log('Number of unvisited shows: {}'.format(len(unvisited_ids)),
                 level=logging.INFO)
        raise
        # Returns a generator
        return (scrapy.Request('https://mydramalist.com/{}'.format(id))
                for id in unvisited_ids)

    def load_state(self):
        """Loads the state to the item pipeline and to the
        spider (for start requests)"""
        filepath = 'data/comments/state.txt'  # Todo: Consider key
        if os.path.isfile(filepath):
            with open(filepath) as f:
                pipeline_state = json.loads(f.readline())
                file_index = pipeline_state['file_index']
                file_size = pipeline_state['file_size']
                for line in f:
                    show_id = json.loads(line)['show_id']
                    self.state.add(show_id)
                print(file_size, file_index, self.state)
        # Ensures that start_requests does not include already visited shows
        # Todo: Ignore the last

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
