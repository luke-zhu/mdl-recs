"""This spider uses the urls stored in dramalist_links.json to get all of the
shows and scores each user's dramalist. I used Sublime Text to add
http://www.mydramalist to the front of the URLs

Get the URLs by running the following command on your terminal:
    scrapy runspider data_collection/profile_link.py -o data/scores.json
"""

import glob
import logging
import os

import scrapy
import pandas as pd  # Fastest csv reader

from pandas.errors import EmptyDataError
from scrapy.crawler import CrawlerProcess


class DramaListSpider(scrapy.Spider):
    """Extracts the scores from the dramalist URLs in start_urls.
    """
    name = 'dramalist'
    allowed_domains = ['mydramalist.com']

    def parse(self, response: scrapy.http.Response):
        # This function yields all the shows in a user's dramalist
        sections = response.css('div.box')

        for section in sections:
            section_name = section.css('h3::text').extract_first()
            rows = section.css('tr')
            for show in rows:
                title = show.css('td.sort1 a::attr(title)').extract_first()
                country = show.css('td.sort2::text').extract_first()
                year = show.css('td.sort3::text').extract_first()
                show_type = show.css('td.sort4::text').extract_first()
                score = show.css('td.sort5::attr(abbr)').extract_first()

                progress = show.css('td.sort6 span::text').extract()
                if progress:
                    episodes_seen, episodes_total = progress
                else:
                    episodes_seen = None
                    episodes_total = None

                yield {
                    'user': response.url,
                    'section': section_name,
                    'title': title,
                    'country': country,
                    'year': year,
                    'type': show_type,
                    'score': score,
                    'episodes_seen': episodes_seen,
                    'episodes_total': episodes_total,
                }


if __name__ == '__main__':
    process = CrawlerProcess({
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': '../logs/dramalist_spider.log',
        'FEED_FORMAT': 'jsonlines',
        'FEED_URL': 'score',
        'DOWNLOAD_DELAY': 0.25,
    })

    start_urls = []
    for filename in glob.glob('../data/dramalist_urls/*.csv'):
        try:
            df = pd.read_csv(filename, header=None, usecols=[0])
            start_urls.extend(df[0].values)
        except EmptyDataError:
            logging.log(logging.INFO,
                        'Empty file: {}'.format(filename))

    DramaListSpider.start_urls = start_urls
    process.crawl(DramaListSpider)
    process.start()
