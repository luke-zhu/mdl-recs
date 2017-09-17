# This spider gets all the generic about all of the shows

import scrapy


class ShowSpider(scrapy.Spider):
    name = 'show'
    start_urls = ['http://mydramalist.com/shows/top']
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    page_number = 1
    users = {}

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_list)

    def parse_list(self, response):
        """Takes in a response from a list page and calls parse_show on each
        show link in the list.
        """
        # Parse the show pages
        show_urls = response.css('div.title a::attr(href)').extract()
        for url in show_urls:
            yield scrapy.Request(response.urljoin(url),
                                 callback=self.parse_show)

        # Get the next page
        self.page_number += 1
        if self.page_number == 358:
            yield self.users
        yield scrapy.Request('{}?page={}#comments'.format(self.start_urls[0],
                                                          self.page_number),
                             callback=self.parse_list)

    def parse_show(self, response):
        name = response.css('#show-details > h1 > span::text').extract_first()
        genres = response.css('.show-genres > a::text').extract()
        details = [s.strip() for s in
                   response.css('.content > .show-details li::text').extract()]

        yield {
            'url': response.url,
            'name': name,
            'genres': genres,
            'country': details[0],
            'type': details[1],
            'episodes': details[2],
            'aired': details[3],
            'duration': details[6],
            'score': details[7],
            'score_rank': details[8],
            'popularity_rank': details[9],
        }

        # Add users to the dictionary
        for url in response.css('a::attr(href)').extract():
            if 'profile' in url:
                if url in self.users:
                    self.users[url] += 1
                else:
                    self.users[url] = 1
