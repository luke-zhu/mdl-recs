import glob
import json
import os

class ShowDataLoader:
    """Cleans, validates, and loads the scraped data.
    """

    def __init__(self):
        self.shows = []
        self.reviews = []
        self.recs = []
        self.comments = []
        pass

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
                    # Todo: Flatten the data
                    self.shows.append(item)
                elif 'has_more' in item:  # Comment
                    # Todo: Split the comment items into separate records
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

        for show in self.shows:
            # 0 episodes to none
            # duration to int
            # release_date to iso
            # end_date to iso
            pass

        for index, rec in enumerate(self.recs):
            self.recs[index]['text'] = rec['text'].strip()
            self.recs[index]['votes'] = int(rec['votes'])
            self.recs[index]['show_ids'] = sorted([int(id) for id in rec['show_ids']])
            self.recs[index]['id'] = int(rec['id'])

        for index, review in enumerate(self.reviews):
            self.reviews[index]['show_id'] = int(review['show_id'])
            self.reviews[index]['post_date'] = 0 # Todo: Turn date into iso format
            self.reviews[index]['text'] = review['text'].strip()

        for index, comment in enumerate(self.comments):
            # Todo: Alot
            pass




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
        pass

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
