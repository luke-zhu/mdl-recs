"""Takes in a list of links are returns counts"""
import pyspark

from pyspark import SparkConf
from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("User post counts")
             .config(conf=SparkConf())
             .getOrCreate())
    df = spark.read.json('data/profiles.json')
    counts = (df
              .groupBy('profile_link')
              .count()
              .sort('count', ascending=False))
    counts.write.csv('data/profile_counts.csv')
