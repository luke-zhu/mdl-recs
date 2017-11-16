"""A collection of small throwaway programs ran at some point to
maintain the quality of the data.
"""

import re
from glob import glob
import json
from os.path import join

import os


def load_jsonlines(path_pattern):
    """Loads the items with the given path into a single array"""
    filenames = glob(path_pattern)
    data = []
    for file in filenames:
        with open(file) as f:
            for line in f:
                data.append(json.loads(line))
    return data


def save_jsonlines(data, dirpath):
    """Saves the data in the given directory in files named
    like part-00000, part-00001, 100 lines per file.
    """
    file_index = 0
    file_size = 0
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)
    filepath = join(dirpath, 'part-{0:05d}.jl'.format(file_index))
    file = open(filepath, 'w')
    for item in data:
        if file_size >= 100:
            file.close()
            file_size = 0
            file_index += 1
            filepath = join(dirpath, 'part-{0:05d}.jl'.format(file_index))
            file = open(filepath, 'w')
        line = json.dumps(dict(item)) + '\n'
        file.write(line)
        file_size += 1


def cleaning_11_14():
    """A cleaning routine done on 11/14 to resolve some schema issues"""
    data = load_jsonlines('data/comments/*')
    for item in data:
        item['show_id'] = item['show_id'][0]
    save_jsonlines(data, 'data/comments')


def parse_logs(show_id_items):
    """Add show_id dictionaries to the list of show_id_items"""
    with open('logs/comment_spider.log') as f:
        # Get to the start of the logs for the current session
        for line in f:
            if line.startswith(
                    '2017-11-14 16:36:51 [scrapy.core.engine] INFO:'):
                break
        pattern = re.compile(r'mydramalist\.com\/([0-9]+)')
        for line in f:
            match = pattern.search(line)
            try:
                show_id = match.group(1)
                show_id_items.append({
                    'status': 'errored',
                    'show_id': show_id,
                })
            except AttributeError:  # We skip NoneType errors
                pass

    with open('logs/comment_spider2.log') as f:
        # Get to the start of the logs for the current session
        pattern = re.compile(r'mydramalist\.com\/([0-9]+)')
        for line in f:
            match = pattern.search(line)
            try:
                show_id = match.group(1)
                show_id_items.append({
                    'status': 'errored',
                    'show_id': show_id,
                })
            except AttributeError:  # We skip NoneType errors
                pass


def persist_11_14():
    """Persisting the results from the commment spider in a file
    called state.txt.

    Overwrites the previous jsonlines. In the future use JOBDIR
    to persist the results from a run. Also consider using
    scrapyd
    """
    data = load_jsonlines('data/comments/*.jl')
    show_id_items = [{
        'status': 'scraped',
        'show_id': item['show_id'],
    } for item in data if not item['has_more']]
    parse_logs(show_id_items)
    with open('data/comments/state.txt', 'w') as f:
        # Todo: Update file_index or remove hardcoding
        num_files = len(glob('data/comments/*.jl'))
        line = '{"file_index": ' + str(num_files) + ', "file_size": 0}\n'
        f.write(line)
        for item in show_id_items:
            line = json.dumps(dict(item)) + '\n'
            f.write(line)

def print_num_shows():
    data = load_jsonlines('data/comments/*.jl')
    show_ids = {item['show_id'] for item in data}
    print(len(show_ids))
    errored_items = []
    parse_logs(errored_items)
    show_ids.union({item['show_id'] for item in errored_items})
    print('Unique show_ids:', len(show_ids))


def clean_comments():
    """Ran on 11/15 at 6pm"""
    data = load_jsonlines('data/comments/*.jl')
    data = list(data)

    unique = []
    seen_urls = set()
    for item in data:
        if item['url'] not in seen_urls:
            unique.append(item)
            seen_urls.add(item['url'])
    unique.sort(key=lambda x: int(x['show_id']))
    save_jsonlines(unique, 'data/comments-unique')


if __name__ == '__main__':
    data = load_jsonlines('data/comments/*.jl')
    show_ids = {row['show_id'] for row in data}
    with open('data/show_ids.txt', 'w') as f:
        for id in show_ids:
            f.write(id + '\n')

