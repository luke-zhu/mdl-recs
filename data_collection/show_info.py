import scrapy

origin_url = 'http://mydramalist.com/browse/all?' + \
             'types[]=68&types[]=83&sort[]=popular&countries[]=0'

class ShowInfoSpider(scrapy.Spider):
    name = 'show_info'
    allowed_domains = ['mydramalist.com']
    start_urls = [origin_url]
    index = 1
    # start_urls += [origin_url + '&page=' + str(index) for index in range(2, 11)]

    def parse(self, response):
        shows = response.css('div.titleBlock')
        for show in shows:
            image_src = show.css('div.cover img::attr(src)').extract_first()
            url = show.css('div.title a::attr(href)').extract_first()
            name = show.css('div.title a::text').extract_first()
            basic_info, num_episodes = show.css('div.info::text').extract()
            score = show.css('ul.statsInfo > li > b::text').extract_first()
            yield {
                'image_src': image_src,
                'url': url,
                'name': name,
                'info': basic_info,
                'score': float(score),
                'episodes': num_episodes,
            }
        if self.index >= 10:
            return
        else:
            self.index += 1
            yield scrapy.Request(origin_url + '&page=' + str(self.index))
