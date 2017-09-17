import pandas as pd
import numpy as np

RATINGS_COLS = ['country',
                'episodes_seen',
                'episodes_total',
                'score',
                'section',
                'title',
                'type',
                'user',
                'year']

# Find show-show similarity.
# Find pairs who have rated both shows

def cosine(ratings: pd.DataFrame) -> pd.Index:
    """Takes in a ratings df and returns the consine similarities of shows
    watched by more than 10 users.
    """
    assert ratings.columns.all(RATINGS_COLS)

    filtered = ratings[ratings['score'] > 0][['title', 'user', 'score']]
    grouped = filtered.groupby('title')
    popular = grouped.filter(lambda show: show['user'].size > 10)
    pairs = pd.merge(popular, popular, on='user')
    # Cosine similarity
    pairs['score_xy'] = pairs['score_x'] * pairs['score_y']
    pairs['score_xx'] = pairs['score_x'] ** 2
    pairs['score_yy'] = pairs['score_y'] ** 2
    filtered = pairs[pairs['title_x'] < pairs['title_y']]
    sums = filtered.groupby(['title_x', 'title_y']).sum()
    similarities = sums['score_xy'] / np.sqrt(sums['score_xx'] * sums['score_yy'])
    return similarities.sort_values(ascending=False)

def jaccard(ratings: pd.DataFrame) -> pd.Index:
    """Takes in a ratings df and returns the jaccard similarities of shows
    watched by more than 10 users.
    """
    assert ratings.columns.all(RATINGS_COLS)

    filtered = ratings[ratings['score'] > 0][['title', 'user']]
    grouped = filtered.groupby('title')
    popular = grouped.filter(lambda show: show['user'].size > 10)
    counts = popular.groupby('title').count().reset_index()
    counts.columns = ['title', 'count']
    merged = pd.merge(filtered, counts, on='title')
    pairs = pd.merge(merged, merged, on='user')
    pair_counts = pairs.groupby(['title_x', 'title_y']).agg({
        'user': 'count',
        'count_x': 'min',
        'count_y': 'min',
    })
    similarities = pair_counts['user'] / (pair_counts['count_x'] + pair_counts['count_y'])
    return similarities.sort_values(ascending=False)

def pageRank(ratings: pd.DataFrame) -> pd.Index:
    pass

if __name__ == '__main__':
    ratings = pd.read_json('../data/ratings.json')
    cosine = cosine(ratings)
    jaccard = jaccard(ratings)

    cosine.to_csv('../data/cosine.csv')
    jaccard.to_csv('../data/jaccard.csv')
