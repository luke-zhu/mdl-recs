import glob
import json
import os

from elasticsearch import Elasticsearch


def load_data(es, index, dirpath):
    """Loads the jsonlines data from the given dirpath to
    the given mapping in the mydramalist index.
    """
    filepaths = glob.glob(os.path.join(dirpath, '*'))
    for fp in filepaths:
        with open(fp) as f:
            for line in f:
                item = json.loads(line)
                es.index(index=index,
                         doc_type=index,
                         id=item['id'],
                         body=item)


if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    load_data(es, 'show', 'data/show-1511337330/shows')
    load_data(es, 'comment', 'data/show-1511337330/comments')
    load_data(es, 'rec', 'data/show-1511337330/recs')
    load_data(es, 'review', 'data/show-1511337330/reviews')


