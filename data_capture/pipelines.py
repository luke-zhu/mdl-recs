# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

import time

import scrapy


# Todo: Move the ITEM_PIPELINE setting to custom_settings in CommentSpider
class CommentPipeline(object):
    """Processes items collected by t"""
    file_index = 0
    file_size = 0  # The number of items in the file

    def open_spider(self, spider: scrapy.Spider):
        """Creates initializes the output folders to store the
        comment items.
        """
        if not os.path.isdir('data'):
            os.mkdir('path')
        self.time_key = time.time()
        try:
            os.mkdir('data/comments-{}'.format(self.time_key))
        except FileExistsError:
            print('The directory data/comments already exists. Move or remove'
                  'the directory and retry running the spider')
            raise
        self.file = open(
                'data/comments-{}/part-{0:05d}.jl'.format(self.time_key,
                                                          self.file_index),
                'w')

    def close_spider(self, spider: scrapy.Spider):
        self.file.close()

    def process_item(self, item: dict, spider: scrapy.Spider):
        """Writes the input item to a file in the directory. Changes the
        output file if the current file contains at least 100 items.
        """
        if self.file_size >= 100:
            self.file.close()
            self.file = open(
                    'data/comments-{}/part-{0:05d}.jl'.format(self.time_key,
                                                              self.file_index),
                    'w')
            self.file_size = 0
            self.file_index += 1
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        self.file_size += 1
        return item
