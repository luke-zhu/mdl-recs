# This script takes in a JSON file of shows and gets the 5 most similar shows.
import pandas as pd
import json

if __name__ == '__main__':
    popular_df = pd.read_json('../data/popular-shows.json')
    similarity_df = pd.read_csv('../data/cosine.csv')

    most_similar = {}
    for _, row in popular_df.iterrows():
        show1_df = similarity_df[similarity_df['show1'] == row['name']]
        show2_df = similarity_df[similarity_df['show2'] == row['name']]
        similar_shows = [(show['show2'], show['similarity'])
                         for _, show in show1_df.iterrows()]
        similar_shows += [(show['show1'], show['similarity'])
                          for _, show in show2_df.iterrows()]
        most_similar[row['name']] = sorted(similar_shows,
                                        key=lambda x: x[1],
                                        reverse=True)[:5]


    with open('../data/k-nearest-items.json', 'w') as outfile:
        json.dump(most_similar, outfile)