"""A collection of small programs ran at some point to maintain
the quality of the data.
"""

import re
from glob import glob
import json


def load_jsonlines(pathname):
    """Joins the comment files into 1 file"""
    filenames = glob(pathname)
    data = []
    for file in filenames:
        with open(file) as f:
            for line in f:
                data.append(json.loads(line))
    return data


def save_jsonlines(data, pathname):
    """Saves the data in the given path in files named like part-00000,
    part-00001, 100 lines per file.

    Note the pathname to should not end with a '/'
    """
    file_index = 0
    file_size = 0
    file = open(pathname + 'part-{0:05d}.jl', 'w')
    for item in data:
        if file_size >= 100:
            file.close()
            file = open(
                    'data/comments/part-{0:05d}.jl'.format(file_index),
                    'w')
            file_size = 0
            file_index += 1
        line = json.dumps(dict(item)) + '\n'
        file.write(line)
        file_size += 1


def cleaning_11_14():
    """A cleaning routine done on 11/14 to resolve some schema issues"""
    data = load_jsonlines('data/comments/*')
    for item in data:
        item['show_id'] = item['show_id'][0]
    save_jsonlines(data, 'data/comments')


def persist_11_14():
    """Persisting the results from the spider in a file called state.txt

    Overwrites the previous jsonlines
    """
    data = load_jsonlines('data/comments/*.jl')
    show_ids = [{
        'status': 'scraped',
        'show_id': item['show_id'],
    } for item in data if not item['has_more']]
    with open('logs/comment_spider.log') as f:
        # Get to the start of the logs for the current session
        for line in f:
            if line.startswith('2017-11-14 16:36:51 [scrapy.core.engine] INFO: Spider opened'):
                break
        pattern = re.compile(r'mydramalist\.com\/([0-9]+)')
        for line in f:
            match = pattern.search(line)
            try:
                show_id = match.group(1)
                show_ids.append({
                    'status': 'errored',
                    'show_id': show_id,
                })
            except AttributeError: # We skip NoneType errors
                pass

    with open('data/comments/state.txt', 'w') as f:
        f.write('{"file_index": 37, "file_size": 69}\n') # Todo: Remove hardcoding
        for item in show_ids:
            line = json.dumps(dict(item)) + '\n'
            f.write(line)


if __name__ == '__main__':
    persist_11_14()
