"""A script encapsulating the full data extraction pipeline.
"""
from dataloaders import ShowDataLoader

if __name__ == '__main__':
    loader = ShowDataLoader()
    loader.process_show_data('datacollectors/data/show-1510961743', 'data/show-1510961743')


    # spark = (
    #     SparkSession.builder.appName("User post counts").config(conf=SparkConf()).getOrCreate())
