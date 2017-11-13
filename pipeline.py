"""The data extraction pipeline.

The final product will do the following:

Run spiders/profile_url.py -> data/profile_urls.jsonl
Process data/profile_urls.jsonl -> data/dramalist_urls/*.csv
Run spiders/dramalist.py -> data/scores.jsonl
Compute similarities from scores.jsonl -> similarities/*.csv
"""

# Todo: Write the complete sequential pipeline
import pyspark
from math import sqrt

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def dramalist_urls(df: pyspark.sql.DataFrame):
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


def products(pair: tuple):
    """Takes in a (TITLE, ((USER, SCORE1) (USER, SCORE2))) pair and returns
    (TITLE, (SCORE1 * SCORE2, SCORE1 * SCORE1, SCORE2 * SCORE2))))

        ('100 Days with Mr. Arrogant',
        (('https://mydramalist.com/dramalist/Zombie_Girl', 50),
        ('https://mydramalist.com/dramalist/Shifterz', 30)))

    The result will be summed and used to compute cosine similarity
    """
    (user1, score1), (user2, score2) = pair[1]

    if user1 > user2:
        user1, user2 = user2, user1

    return (user1, user2), (score1 * score2, score1 * score1, score2 * score2)


def partial_cosine(df: pyspark.sql.DataFrame):
    score_avgs = df.groupBy('title').avg('score')
    # Finds users who have watched the most shows
    top1000_users = (df
                     .filter('score > 0')
                     .groupBy('user')
                     .count()
                     .sort('count')
                     .limit(1000))
    return top1000_users


# Todo: Refactor the lambdas into named functions
def cosine_similarity(df: pyspark.sql.DataFrame) -> pyspark.rdd:
    """Takes in a Dataframe and uses Spark RDDs to compute
    the cosine similarity.
    """
    rdd = df.rdd

    # Computes the average score of each move
    avgs = (rdd
            .filter(lambda row: row['score'] and row['score'] > 0)
            .map(lambda row: (row['title'], row['score']))
            .combineByKey(lambda score: (score, 1),
                          # TODO: Subract score average
                          lambda pair, score: (
                              pair[0] + score, pair[1] + 1),
                          lambda pair1, pair2: (
                              pair1[0] + pair2[0], pair1[1] + pair2[1]))
            .map(lambda tup: (tup[0], tup[1][0] / tup[1][1])))

    ratings = (rdd
               .filter(lambda row: row['score'] and row['score'] > 0)
               .map(lambda row: (row['title'], (row['user'], row['score']))))

    similarities = (ratings
                    .join(ratings)  # Todo: Check join partitioning
                    # Tuples should contain scores from different users
                    .filter(lambda tup: tup[1][0] != tup[1][1])
                    .map(products)  # Todo: Filter if not enough common shows
                    .reduceByKey(lambda tup1, tup2: (tup1[0] + tup2[0],
                                                     tup1[1] + tup2[1],
                                                     tup1[2] + tup2[2]))
                    .map(lambda tup:
                         (tup[0], tup[1][0] / sqrt(tup[1][1] * tup[1][2])))
                    .map(lambda tup:
                         '{},{},{}'.format(tup[0][0], tup[0][1], tup[1])))

    return similarities


if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("User post counts")
             .config(conf=SparkConf())
             .getOrCreate())

    df = spark.read.json('data/scores.jsonl')
    df = df.withColumn('score', df['score'].cast('int'))
    similarities = cosine_similarity(df)
    similarities.saveAsTextFile('data/similarities')
