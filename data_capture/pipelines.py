# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
import json

import scrapy


# Todo: Move the ITEM_PIPELINE setting to custom_settings in CommentSpider
class CommentPipeline(object):
    """Processes items collected by the comment spider"""

    def __init__(self):
        self.file: os.io.TextIOWrapper = None
        self.file_index = 0
        self.file_size = 0

    def open_spider(self, spider: scrapy.Spider):
        """Creates initializes the output folders to store the
        comment items.
        """
        try:
            os.mkdir('data')
        except FileExistsError:
            spider.log(' Directory data/ exists. Attempting to resume run.',
                       level=logging.INFO)
        try:
            os.mkdir('data/comments')
        except FileExistsError:
            spider.log('Directory data/comments/ exists. Attempting to'
                       'resume run.',
                       level=logging.INFO)
        # Todo: Remove mentions of state when done with current run
        try:
            # Path used in comment.py as well
            with open('data/comments/state.txt') as f:
                pipeline_state: dict = json.loads(f.readline())
                self.file_index = pipeline_state['file_index']
                self.file_size = pipeline_state['file_size']
        except FileNotFoundError:
            spider.log('State file not found. Crawling all pages')
        filename = 'data/comments/part-{0:05d}.jl'.format(self.file_index)
        self.file = open(filename, 'a')

    def close_spider(self, spider: scrapy.Spider):
        """Closes the current open file and persists the
        state of the spider
        """
        self.file.close()

    def process_item(self, item: dict, spider: scrapy.Spider) -> dict:
        """Writes the input item to a file in the directory. Changes the
        output file if the current file contains at least 100 items.
        """
        if self.file_size >= 100:
            self.file.close()
            filename = 'data/comments/part-{0:05d}.jl'.format(self.file_index)
            self.file = open(filename, 'a')
            self.file_size = 0
            self.file_index += 1
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        self.file_size += 1
        return item


class TestPipeline():
    pass