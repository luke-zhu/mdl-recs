# INFO
# This spider uses the urls stored in dramalist_links.json to get all of the
# shows and scores each user's dramalist. I used Sublime Text to add 
# http://www.mydramalist to the front of the URLs
# 
# Get the URLs by running the following command on your terminal:
# scrapy runspider data_collection/profile_link.py -o data/scores.json

import json

import scrapy
import logging

def profile_links():
    with open('data/dramalist_links.json') as f:
        data = json.load(f)
        links = [obj['dramalist_link'] for obj in data]
        return links

class DramaListSpider(scrapy.Spider):
    name = 'dramalist'
    allowed_domains = ['mydramalist.com']
    start_urls = profile_links()

    def parse(self, response):
        # This function yields all the shows in a user's dramalist
        sections = response.css('div.mylist')

        for section in sections:
            section_name = section.xpath('../h2/text()').extract_first()
            rows = section.css('tr')
            for show in rows:
                title = show.css('td.sort1 a::attr(title)').extract_first()
                country = show.css('td.sort2::text').extract_first()
                year = show.css('td.sort3::text').extract_first()
                show_type = show.css('td.sort4::text').extract_first()
                score = show.css('td.sort5::attr(abbr)').extract_first()
                episodes_seen, episodes_total = show.css('td.sort6 span::text').extract()

                prefix_url = 'http://www.mydramalist'
                yield {
                    'user': prefix_url + response.url,
                    'section': section_name,
                    'title': title,
                    'country': country,
                    'year': year,
                    'type': show_type,
                    'score': score,
                    'episodes_seen': episodes_seen,
                    'episodes_total': episodes_total,
                }


# URL (not necessarly same as name)
# Currently Watching
# Completed
# On Hold
# Dropped
# Plan to Watch
        
# Show - title, country, year, type, score, progress