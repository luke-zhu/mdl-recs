"""A set of crude tests for the showspider"""

import subprocess


def test_popular_show():
    process = subprocess.run(['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True',
                              'https://mydramalist.com/16921-go-hos-starry-night'],
                             stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_popular_movie():
    process = subprocess.run(['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True',
                              'https://mydramalist.com/2912-spellbound'], stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_new_show():
    process = subprocess.run(['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True',
                              'https://mydramalist.com/25143-honto-ni-atta-onna-no-jinsei'],
                             stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_new_movie():
    process = subprocess.run(['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True',
                              'https://mydramalist.com/24676-thief-actor'], stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output
