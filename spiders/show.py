import scrapy


class ShowSpider(scrapy.Spider):
    name = 'show'
    allowed_domains = ['mydramalist.com']

    # Comments URL
    # https://beta4v.mydramalist.com/v1/threads?page=1&c=title&t=24678
    def parse(self, response: scrapy.http.Response):
        pass