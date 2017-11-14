"""This spider uses the urls stored in dramalist_urls/ to get all of the
shows and scores each user's dramalist.

Run python3 dramalist.py collect the urls in scores.jsonl

Note: The data and logs folders must be created manually first.

"""

import logging

from glob import glob

import scrapy
import pandas as pd  # Fastest csv reader

from pandas.errors import EmptyDataError
from scrapy.crawler import CrawlerProcess


# Todo: Write unit and functionality tests
class DramaListSpider(scrapy.Spider):
    """Extracts the scores from the dramalist URLs in start_urls.
    """
    name = 'dramalist'
    allowed_domains = ['mydramalist.com']

    def parse(self, response: scrapy.http.Response):
        """Takes in a Response object referring to a dramalist
        page (like https://mydramalist.com/dramalist/cyclotomic)
        and yields the 6 td.sort fields in a flat JSON object.

        All of the yielded fields are strings or NoneTypes.
        """
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
                    episodes_seen, episodes_total = progress[1:]
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
                    'score': score,  # "0" default
                    'episodes_seen': episodes_seen,  # Nullable
                    'episodes_total': episodes_total,  # Nullable
                }


if __name__ == '__main__':
    process = CrawlerProcess({
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': '../logs/dramalist_spider.log',
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': '../data/scores.jsonl',
        'DOWNLOAD_DELAY': 1,
    })

    start_urls = []
    for filename in glob('../data/dramalist_urls/*.csv'):
        try:
            df = pd.read_csv(filename, header=None, usecols=[0])
            start_urls.extend(df[0].values)
        except EmptyDataError:
            logging.log(logging.INFO,
                        'Empty file: {}'.format(filename))

    DramaListSpider.start_urls = start_urls
    process.crawl(DramaListSpider)
    process.start()
