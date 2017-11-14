from scrapy.http import HtmlResponse
import pytest

from dramalist import DramaListSpider
from discussion import DiscussionSpider


def test_discussion_spider():
    with open('test_discussion.html') as f:
        text = f.read()
    res = HtmlResponse('https://mydramalist.com/discussions/recent_discussions',
                       body=text.encode())
    spider = DiscussionSpider()
    expected_urls = [
        'https://mydramalist.com/discussions/general-discussion/30905-30-day-character-challenge-by-elle',
        'https://mydramalist.com/discussions/recommendation-forum/31110-school-or-college-setting-drama'
    ]
    generator = spider.parse(res)
    assert next(generator).url == expected_urls[0]
    assert next(generator).url == expected_urls[1]

    # 15 - 2 thread links remaining on the page + 1 list page link
    assert sum(1 for _ in generator) == 16 - 2


def test_dramalist_spider():
    with open('test_dramalist.html') as f:
        text = f.read()
    res = HtmlResponse('https://mydramalist.com/dramalist/cyclotomic',
                       body=text.encode())
    spider = DramaListSpider()
    expected = {'user': 'https://mydramalist.com/dramalist/cyclotomic',
                'section': 'Currently Watching',
                'title': 'Healer',
                'country': 'South Korea',
                'year': '2014',
                'type': 'Drama',
                'score': '95',
                'episodes_seen': '14',
                'episodes_total': '20'}
    generator = spider.parse(res)
    assert next(generator) == expected
    assert sum(1 for _ in generator) == 9
