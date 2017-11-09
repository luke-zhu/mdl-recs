"""This spider collects the profile URLs of users who have posted on
any of the recent discussion threads.

To store the URLs in data/profile_links.json, run the following
command in your terminal while in the root directory of this
project

    scrapy runspider \
        --output=data/profiles.json \
        --output-format=jsonlines \
        --loglevel=INFO \
        --logfile=logs/profiles.log \
        data_collection/profiles.py
"""

import random
import time
import logging

import scrapy


class ProfileLinkSpider(scrapy.Spider):
    """Spider that collects links to MyDramaList user profiles.
        example: https://mydramalist.com/profile/cyclotomic
    """
    name = 'profiles'
    allowed_domains = ['mydramalist.com']
    start_urls = ['http://mydramalist.com/discussions/recent_discussions']

    def parse(self, response):
        """Takes in a scrapy HTTP response to a discussion list page
        and calls parse discussion on each discussion on the page.

        Example input: scrapy.http.Response object from
            https://mydramalist.com/discussions/recent_discussions

        This method is invoked w/ response objects from the start_urls
        attribute.
        """
        discussion_links = response \
            .css('td.thread--discussion a.text-primary::attr(href)') \
            .extract()

        for link in discussion_links:
            yield scrapy.Request(response.urljoin(link),
                                 callback=self.parse_discussion)
            # Sleep ~ 1 second before next the call to be mindful
            time.sleep(random.random())

        # Continues if a next list page exists
        next_page = response.css('li.page-item.next a::attr(href)')
        if next_page:
            next_page_link = next_page.extract_first()
            logging.log(
                logging.INFO, 'Next list page: {}'.format(next_page_link))
            yield scrapy.Request(response.urljoin(next_page_link))

    def parse_discussion(self, response):
        """Takes in a response object from a discussion page
        and yields the profile links of all

        Example output:
            {'profile_link': 'https://mydramalist.com/profile/cyclotomic'}
        """
        profile_links = response.css(
            'div.post__username a::attr(href)').extract()

        if not profile_links:
            logging.log(logging.ERROR,
                        'No profile links found on {}'.format(response.url))

        for link in profile_links:
            yield {'profile_link': response.urljoin(link)}

        # Continues if a next list page exists
        next_page = response.css('li.page-item.next a::attr(href)')
        if next_page:
            next_page_link = next_page.extract_first()
            logging.log(logging.INFO,
                        'Next discussion page: {}'.format(next_page_link))
            yield scrapy.Request(response.urljoin(next_page_link),
                                 callback=self.parse_discussion)
