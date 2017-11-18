import glob
import json
import os
import re

import dateparser


# Todo: Research and replace as much app-side processing w/ SQL
class ShowDataLoader:
    """Cleans, validates, and loads the scraped data.
    """

    def __init__(self):
        self.shows = []
        self.reviews = []
        self.recs = []
        self.comments = []

    def process_show_data(self, input_dirpath: str, output_dirpath: str):
        """Reads the show data from the given file input_dirpath, processes it, and
        loads it into a set of JSONlines files.
        """
        self.load_data(input_dirpath)
        self.clean_data()
        self.validate_data()
        self.save_data(output_dirpath)

    def load_data(self, dirpath: str):
        filepaths = glob.glob(os.path.join(dirpath, '*'))
        for filepath in filepaths:
            data = []
            with open(filepath) as f:
                for line in f:
                    data.append(json.loads(line))
            for item in data:
                if 'main_title' in item:  # Show
                    self.shows.append(item)
                elif 'has_more' in item:  # Comment
                    for comment in item['items']:
                        self.comments.append(comment)
                elif 'show_id' in item:  # Review
                    self.reviews.append(item)
                elif 'show_ids' in item:  # Rec
                    self.recs.append(item)
                else:
                    print('Item does not match any of the conditions: {}'.format(item))

    def clean_data(self):
        self.shows = self._unique(self.shows, 'id')
        self.reviews = self._unique(self.reviews, 'id')
        self.recs = self._unique(self.recs, 'id')
        self.comments = self._unique(self.comments, 'id')

        duration_pattern = re.compile(r'(?:(\d)+ hr. )?(\d)+ min.')
        for index, show in enumerate(self.shows):
            try:
                match_object = duration_pattern.search(show['duration'])
                hours = match_object.group(1)
                hours = int(hours) if hours else 0
                minutes = match_object.group(2)
                minutes = int(hours) if hours else 0
                show['duration'] = 60 * hours + minutes
            except (ValueError, AttributeError):
                print(show['url'], show['duration'])
                raise
            except KeyError:
                pass
            show['release_date'] = dateparser.parse(show['release_date']).isoformat()
            if 'episodes' in show and show['episodes'] == 0:
                show['episodes'] = None
            try:
                show['end_date'] = dateparser.parse(show['end_date']).isoformat()
            except (TypeError, AttributeError):
                show['end_date'] = None
            show['synopsis'] = show['synopsis'].strip()

        to_remove = []  # indices of recs to remove
        for index, rec in enumerate(self.recs):
            rec['text'] = rec['text'].strip()
            rec['votes'] = int(rec['votes'])
            try:
                rec['show_ids'] = sorted([int(id) for id in rec['show_ids']])
            except:
                to_remove.append(index)
            rec['id'] = int(rec['id'])

        for index in reversed(to_remove):
            del self.recs[index]

        for index, review in enumerate(self.reviews):
            review['show_id'] = int(review['show_id'])
            post_datetime = dateparser.parse(review['post_date'])
            review['post_date'] = post_datetime.isoformat()
            review['text'] = review['text'].strip()

        for index, comment in enumerate(self.comments):
            # Todo: Alot
            pass

        self._standardize_nulls()

    def _standardize_nulls(self):
        for show in self.shows:
            if 'network' not in show:
                show['network'] = ''
            if 'alt_titles' not in show:
                show['alt_titles'] = []
            if show['rank'] == 99999:
                show['rank'] = None
            if show['popularity'] == 99999:
                show['popularity'] = None

    def _unique(self, data: list, primary_key) -> list:
        unique_ids = set()
        unique_items = []
        for item in data:
            if item[primary_key] not in unique_ids:
                unique_ids.add(item[primary_key])
                unique_items.append(item)
        return unique_items

    def validate_data(self):
        # Since BigQuery already does type checks and null checks, we do range checks here
        # Todo: Range checks
        key_counts = {}
        nullable = ('episodes', 'end_date', 'score', 'rank', 'popularity')
        optional = ('episodes', 'network', 'alt_titles', 'native_title', 'duration')
        for show in self.shows:
            # Optional: (-6) episodes, end_date, score, network, alt_titles, native_title
            # (-3 not implemented)
            for key in show:
                if key in key_counts:
                    key_counts[key] += 1
                else:
                    key_counts[key] = 1
        for key in key_counts:
            if key not in optional:
                assert key_counts[key] == len(self.shows)

        for show in self.shows:
            for key in show:
                if key not in nullable:
                    assert show[key] is not None
            if 'episodes' in show:
                assert show['episodes'] is not 0
            if 'end_date' in show:
                assert show['end_date'] not in ('', '?')
            assert show['score'] is not 0
            assert show['rank'] is not 99999
            assert show['popularity'] is not 99999
            assert len(show) >= 15
        print(len(self.shows), key_counts)

        for rec in self.recs:
            for key in rec:
                assert rec[key] is not None
            assert len(rec) == 5

        for review in self.reviews:
            for key in review:
                assert review[key] is not None
            assert len(review) == 12

    def save_data(self, dirpath: str):
        self.save_jsonlines(self.shows, os.path.join(dirpath, 'shows'))
        self.save_jsonlines(self.reviews, os.path.join(dirpath, 'reviews'))
        self.save_jsonlines(self.recs, os.path.join(dirpath, 'recs'))
        self.save_jsonlines(self.comments, os.path.join(dirpath, 'comments'))

    def save_jsonlines(self, data: list, dirpath: str):
        """Saves the data in the given directory in files named
        like part-00000, part-00001, 100 lines per file.
        """
        file_index = 0
        file_size = 0
        os.makedirs(dirpath)
        filepath = os.path.join(dirpath, 'part-{0:05d}.jl'.format(file_index))
        file = open(filepath, 'w')
        for item in data:
            if file_size >= 100:
                file.close()
                file_size = 0
                file_index += 1
                filepath = os.path.join(dirpath, 'part-{0:05d}.jl'.format(file_index))
                file = open(filepath, 'w')
            line = json.dumps(dict(item)) + '\n'
            file.write(line)
            file_size += 1
