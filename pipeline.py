"""A script encapsulating the full data extraction pipeline.
"""

# Todo: Write the complete sequential pipeline
from pyspark import SparkConf
from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("User post counts")
             .config(conf=SparkConf())
             .getOrCreate())
