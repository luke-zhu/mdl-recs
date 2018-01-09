import random

import elasticsearch.helpers
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch


class HighlightExtractor:
    """Extracts review or comment highlights for the shows.

    This process works by first getting the raw text data from the Elasticsearch
    server, then computing the TF-IDF values of the words. Finally, random words
    with high TF-IDF values are used to search for sentence highlights.
    """

    def __init__(self):
        self.es = Elasticsearch('localhost:9200')
        self.vectorizer = TfidfVectorizer(min_df=0.025,
                                          max_df=0.2,
                                          analyzer='word',
                                          stop_words='english',
                                          token_pattern=r'[a-zA-Z]{2,}')
        self.es_ids = {}  # show_id to elasticsearch id mapping
        self.documents = []
        self.show_ids = {}  # list index to show id mapping
        self.document_indices = {}  # show_id to list indices mapping
        self.significant_terms = {}  # show id to terms list mapping
        self.highlights = {}  # show id as key

    def read_data(self):
        """Loads Elasticsearch raw text into the documents list."""
        for show in elasticsearch.helpers.scan(self.es, index='show'):
            self.es_ids[show['_source']['id']] = show['_id']
        for i, review in enumerate(elasticsearch.helpers.scan(self.es, index='review')):
            self.documents.append(review['_source']['text'])
            self.show_ids[i] = review['_source']['show_id']
            if review['_source']['show_id'] in self.document_indices:
                self.document_indices[review['_source']['show_id']].append(i)
            else:
                self.document_indices[review['_source']['show_id']] = [i]

    def build_significant_terms(self):
        """Builds a dictionary from the input documents"""
        matrix = self.vectorizer.fit_transform(self.documents)
        # zip(self.vectorizer.get_feature_names(), self.vectorizer.idf_)
        feature_names = self.vectorizer.get_feature_names()
        for idx, vector in enumerate(matrix):
            terms = [feature_names[i] for i in vector.nonzero()[1]]
            if self.show_ids[idx] in self.significant_terms:
                self.significant_terms[self.show_ids[idx]] += terms
            else:
                self.significant_terms[self.show_ids[idx]] = terms
        # Filter the terms to a random 5
        for key in self.significant_terms:
            terms = self.significant_terms[key]
            filtered_size = min(5, len(terms))
            self.significant_terms[key] = random.sample(terms, filtered_size)

    def build_highlights(self):
        """Given the signficant terms dictionary, finds review or synopsis highlights in
        the array"""
        for show_id in self.significant_terms:
            self.highlights[show_id] = []
            for doc_index in self.document_indices[show_id]:
                sentences = self.documents[doc_index].split('.')
                for sentence in sentences:
                    for term in self.significant_terms[show_id]:
                        if term in sentence and sentence not in self.highlights[show_id]:
                            self.highlights[show_id].append(sentence)

    def load_highlights(self):
        """Loads the highlights into the Elasticsearch db"""
        for show_id in self.highlights:
            body = {
                'doc': {
                    'highlights': self.highlights[show_id],
                }
            }
            self.es.update(index='show', doc_type='show', id=self.es_ids[show_id], body=body)


if __name__ == '__main__':
    extractor = HighlightExtractor()
    extractor.read_data()
    extractor.build_significant_terms()
    extractor.build_highlights()
    extractor.load_highlights()
