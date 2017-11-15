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
    """Processes items collected by the comment spider"""
    file_index = 0
    file_size = 0  # The number of items in the file
    state = []

    def open_spider(self, spider: scrapy.Spider):
        """Creates initializes the output folders to store the
        comment items.
        """
        self.initialize_fd()
        self.load_state(spider)

    def initialize_fd(self):
        if not os.path.isdir('data'):
            os.mkdir('data')
        # self.time_key = time.time()
        try:
            os.mkdir('data/comments')
        except FileExistsError:
            print('Directory exists. Attempting to resume run.')
        self.file = open(
                'data/comments/part-{0:05d}.jl'.format(self.file_index),
                'a')

    def load_state(self, spider: scrapy.Spider):
        """Loads the state to the item pipeline"""
        filepath = 'data/comments/state.txt'  # Todo: Consider key
        if os.path.isfile(filepath):
            with open(filepath) as f:
                pipeline_state = json.loads(f.readline())
                file_index = pipeline_state['file_index']
                file_size = pipeline_state['file_size']
                for line in f:
                    self.state.append(json.loads(line))

    def close_spider(self, spider: scrapy.Spider):
        """Closes the current open file and persists the
        state of the spider
        """
        self.file.close()
        with open('data/comments/state.txt', 'w') as f:
            firstline = json.dumps({
                'file_index': self.file_index,
                'file_size': self.file_size
            })
            f.write(firstline)
            for item in self.state:
                line = json.dumps(dict(item)) + '\n'
                f.write(line)

    def process_item(self, item: dict, spider: scrapy.Spider):
        """Writes the input item to a file in the directory. Changes the
        output file if the current file contains at least 100 items.
        Saves the item to state
        """
        if not item['has_more']:
            self.state.append({
                'status': 'scraped',
                'show_id': item['show_id'],
            })
        if self.file_size >= 100:
            self.file.close()
            self.file = open(
                    'data/comments/part-{0:05d}.jl'.format(self.file_index),
                    'a')
            self.file_size = 0
            self.file_index += 1
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        self.file_size += 1
        return item
