"""The data extraction pipeline.

The final product will do the following:

Run spiders/profile_url.py -> data/profile_urls.jsonl
Process data/profile_urls.jsonl -> data/dramalist_urls/*.csv
Run spiders/dramalist.py -> data/scores.jsonl
Compute similarities from scores.jsonl -> similarities/*.csv
"""

# Todo: Write the complete sequential pipeline
import pyspark

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace


def dramalist_urls(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    """Takes in a PySpark DataFrame of profile links and
    returns a DataFrame of unique dramalist links with the
    forum post counts of the corresponding user.
    """
    count_df = (df
                .groupBy('profile_url')
                .count()
                .select(regexp_replace('profile_url',
                                       'profile',
                                       'dramalist'),
                        'count')
                .sort('count', ascending=False))
    return count_df


if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("User post counts")
             .config(conf=SparkConf())
             .getOrCreate())

    df = spark.read.json('data/scores.jsonl')
