# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
import json

import scrapy


class PaginatingPipeline(object):
    """Outputs the items into paginated files in a directory named
    after the """

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
            spider.log(' Directory data/ created',
                       level=logging.INFO)
        except FileExistsError:
            spider.log(' Directory data/ already exists',
                       level=logging.INFO)
        os.mkdir('data/{}'.format(spider.name))
        spider.log(' Directory data/{} created'.format(spider.name),
                   level=logging.INFO)
        filename = 'data/{0}/part-{1:05d}.jl'.format(spider.name, self.file_index)
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
            filename = 'data/{0}/part-{1:05d}.jl'.format(spider.name, self.file_index)
            self.file = open(filename, 'a')
            self.file_size = 0
            self.file_index += 1
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        self.file_size += 1
        return item