import glob
import json
import os
import re

import dateparser


# Todo: Save output files in Avro instead of JSON
# Todo: Document the schema information in a single place
# Todo: Reorganize data cleaning with Spark SQL
# Todo: Refactor classes and write docstrings
class ShowDataLoader:
    """Cleans, validates, and loads scraped MyDramaList show data.
    """

    duration_pattern = re.compile(r'(?:(\d)+ hr. )?(\d)+ min.')

    def __init__(self):
        self.shows = []
        self.reviews = []
        self.recs = []
        self.comments = []

    def process_data(self, input_dirpath: str, output_dirpath: str):
        """Reads the show data from the given file input_dirpath,
        processes it, and
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
                    print(
                        'Item does not match any of the conditions: {}'.format(
                            item))

    def clean_data(self):
        """Removes duplicates and transforms the columns into the right format
        """
        self.shows = self.unique(self.shows, 'id')
        self.reviews = self.unique(self.reviews, 'id')
        self.recs = self.unique(self.recs, 'id')
        self.comments = self.unique(self.comments, 'id')

        self.clean_shows()
        self.clean_recs()
        self.clean_reviews()

    def clean_shows(self):
        """Makes sure that the show data is in the right format.
         The following transformations are done

         duration: string to integer (specifying minutes)
         release_date: string to ISO date string
         end_date: string to ISO date string
         synopsis: stripped whitespace padding
         network: default to empty string
         alt_titles: default to empty list
         rank: default as null instead of 99999
         popularity: default as null instead of 99999
         """
        for index, show in enumerate(self.shows):
            if 'duration' in show:
                show['duration'] = self.parse_duration(show['duration'])
            if 'episodes' in show and show['episodes'] == 0:
                show['episodes'] = None
            try:
                show['release_date'] = dateparser.parse(
                    show['release_date']).isoformat()
            except AttributeError:
                print(show['url'], show['release_date'])
                show['release_date'] = None
            try:
                show['end_date'] = dateparser.parse(
                    show['end_date']).isoformat()
            except (TypeError, AttributeError):
                show['end_date'] = None
            show['synopsis'] = show['synopsis'].strip()

        for show in self.shows:
            if 'network' not in show:
                show['network'] = ''
            if 'alt_titles' not in show:
                show['alt_titles'] = []
            if show['rank'] == 99999:
                show['rank'] = None
            if show['popularity'] == 99999:
                show['popularity'] = None

    def clean_recs(self):
        """Remove recs containing shows that no longer are in the
        database.
        """
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

    def clean_reviews(self):
        """Cast show id to integer. Convert the post date to an ISO string.
        Strip padding from the text column."""
        for index, review in enumerate(self.reviews):
            review['show_id'] = int(review['show_id'])
            post_datetime = dateparser.parse(review['post_date'])
            review['post_date'] = post_datetime.isoformat()
            review['text'] = review['text'].strip()

    # Todo:
    def clean_comments(self):
        for index, comment in enumerate(self.comments):
            pass

    def parse_duration(self, duration: str) -> int:
        """Converts a string into an integer value
        specifying the minute duration

        Ex. self.parse_duration('1 hr. 54 min.') returns 114
        """
        match_object = self.duration_pattern.search(duration)
        hours = match_object.group(1)
        hours = int(hours) if hours else 0
        minutes = match_object.group(2)
        minutes = int(hours) if minutes else 0
        return 60 * hours + minutes

    def unique(self, data: list, primary_key) -> list:
        """Takes in a list of dictionaries, each containing the
        primary_key field and ensures that each primary_key value
        occurs exactly once.

        The first occurence is kept
        """
        unique_ids = set()
        unique_items = []
        for item in data:
            if item[primary_key] not in unique_ids:
                unique_ids.add(item[primary_key])
                unique_items.append(item)
        return unique_items

    # Todo: Log the shows that have an empty alt-titles field
    def validate_data(self):
        """Ensures that the shows contain the right number of keys
        and that only certain fields contain null values or do not
        exist."""
        # Since BigQuery already does type checks and null checks, we do range checks here
        # Todo: Range checks
        self.validate_shows()

        for rec in self.recs:
            for key in rec:
                assert rec[key] is not None
            assert len(rec) == 5

        for review in self.reviews:
            for key in review:
                assert review[key] is not None
            assert len(review) == 12

    def validate_shows(self):
        key_counts = {}
        nullable = (
            'episodes', 'release_date', 'end_date', 'score', 'rank',
            'popularity')
        optional = (
            'episodes', 'end_date', 'network', 'alt_titles', 'native_title',
            'duration')

        for show in self.shows:
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
                filepath = os.path.join(dirpath,
                                        'part-{0:05d}.jl'.format(file_index))
                file = open(filepath, 'w')
            line = json.dumps(dict(item)) + '\n'
            file.write(line)
            file_size += 1
