"""A set of crude tests ensuring that the ShowSpider does not
throw errors on typical pages.
"""

import subprocess


def test_popular_show():
    process = subprocess.run(
        ['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True', '-s',
         'ITEM_PIPELINES =\{\}', 'https://mydramalist.com/16921-go-hos-starry-night'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_popular_movie():
    process = subprocess.run(
        ['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True', '-s',
         'ITEM_PIPELINES =\{\}', 'https://mydramalist.com/2912-spellbound'], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_new_show():
    process = subprocess.run(
        ['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True', '-s',
         'ITEM_PIPELINES =\{\}', 'https://mydramalist.com/25143-honto-ni-atta-onna-no-jinsei'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_new_movie():
    process = subprocess.run(
        ['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True', '-s',
         'ITEM_PIPELINES =\{\}', 'https://mydramalist.com/24676-thief-actor'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output


def test_old_movie():
    process = subprocess.run(
        ['scrapy', 'parse', '-c', 'parse_show', '-d', '5', '-a', 'test=True', '-s',
         'ITEM_PIPELINES =\{\}', 'https://mydramalist.com/5037-frankenstein-conquers-the-world'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = process.stderr.decode()
    assert 'ERROR' not in output

# Todo: Test https://mydramalist.com/159-akai-ito