import glob
import json

import os
from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es = Elasticsearch()
    filepaths = glob.glob(os.path.join('data/show-1511337330/shows', '*'))
    for fp in filepaths:
        with open(fp) as f:
            for line in f:
                print(line)
                res = es.index(index='mydramalist', doc_type='show', body=json.loads(line))
                print(res['created'])
                break
        break
