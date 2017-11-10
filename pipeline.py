import pyspark

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace

def count_profile_urls(df):
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

def compute_cosine_similarity(df):
    pass

if __name__ == '__main__':
    # spark = (SparkSession
    #          .builder
    #          .appName("User post counts")
    #          .config(conf=SparkConf())
    #          .getOrCreate())
    # df = spark.read.json('data/profiles.json')
    # dramalists = process_profiles(df)
    # dramalists.write.csv('data/dramalist_counts')
    pass
