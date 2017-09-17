# INFO
# This spider collects the distinct profile URLs of users who have posted on
# any of the recent discussion threads
# 
# Get the URLs by running the following command on your terminal in the mydramalist/ folder
# scrapy runspider data_collection/profile_link.py -o data/profile_links.json

# -*- coding: utf-8 -*-
import random
import time

import scrapy
import logging

class ProfileLinkSpider(scrapy.Spider):
    name = 'profile_link'
    allowed_domains = ['mydramalist.com']
    start_urls = ['http://mydramalist.com/discussions/recent_discussions']

    prefix_url = 'http://www.mydramalist'
    username_links = set()


    def parse(self, response):
        # Call each individual thread
        thread_links = response \
            .css('div.thread-container td.thread--discussion h4 a::attr(href)') \
            .extract()
        
        for link in thread_links:
            yield scrapy.Request(response.urljoin(link),
                callback=self.parse_discussion)
            # Sleep to be mindful
            time.sleep(random.random())

        # Parse the next list page
        next_page = response.css('div.thead-container-bottom li')[-1]
        next_page_link = next_page.css('a::attr(href)').extract_first()

        # Stops on the last list page
        if next_page_link:
            logging.log(logging.INFO, 'Next discussion page: {}'.format(next_page_link))
            yield scrapy.Request(response.urljoin(next_page_link))

    def parse_discussion(self, response):
        new_username_links = response.css('div.post__username a::attr(href)').extract()
        
        for link in new_username_links:
            if link not in self.username_links:
                self.username_links.add(link)
                yield { 'profile_link': self.prefix_url + link }

        

# Tip: Remember that the timeout is the bottleneck, don't optimize
# other code right now