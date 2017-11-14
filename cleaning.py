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


def cleaning11_14():
    """A cleaning routine done on 11/14 to resolve some schema issues"""
    data = load_jsonlines('data/comments/*')
    for item in data:
        item['show_id'] = item['show_id'][0]
    save_jsonlines(data, 'data/comments')
