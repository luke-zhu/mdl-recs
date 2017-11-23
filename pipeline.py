"""A script encapsulating the full data extraction pipeline.
"""
from datacleaners import ShowDataCleaner

if __name__ == '__main__':
    loader = ShowDataCleaner()
    loader.process_data('datacollectors/data/show-1511337330',
                        'data/show-1511337330')
