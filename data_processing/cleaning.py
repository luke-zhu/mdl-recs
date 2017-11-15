"""Simple cleaning methods implemented with pandas
"""
import pandas as pd


# Todo: Column renaming, type casting, range checking, uniqueness, null values, foreign-key, see https://en.wikipedia.org/wiki/Data_cleansing
def validate(df: pd.DataFrame):
    pass


def clean(df: pd.DataFrame):
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    pass
