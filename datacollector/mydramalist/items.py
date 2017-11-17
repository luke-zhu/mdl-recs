# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class CommentThreadItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     """A comment thread on a show information page"""
#     pass

# Todo: Include information about item type and nullability
class RecommendationItem(scrapy.Item):
    """A user recommendation for two shows"""
    id = scrapy.Field()
    url = scrapy.Field()
    show_ids = scrapy.Field()
    num_votes = scrapy.Field()
    rec_text = scrapy.Field()


class ReviewItem(scrapy.Item):
    """A user review for a show"""
    id = scrapy.Field()
    url = scrapy.Field()
    show_id = scrapy.Field()
    show_title = scrapy.Field()  # The name of the show
    date_posted = scrapy.Field()
    num_votes = scrapy.Field()  # THe number of helpful votes
    overall_score = scrapy.Field()
    story_score = scrapy.Field()
    acting_score = scrapy.Field()
    music_score = scrapy.Field()
    rewatch_score = scrapy.Field()
    review_text = scrapy.Field()


class ShowMetadataItem(scrapy.Item):
    """Information about a drama or movie"""
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    # alt_titles
    date_started = scrapy.Field()
    date_ended = scrapy.Field()
    duration = scrapy.Field()
    average_score = scrapy.Field()
    num_users_rated = scrapy.Field()
    num_users_watched = scrapy.Field()
    genres = scrapy.Field()
    # tags
    country = scrapy.Field()
    num_episodes = scrapy.Field()
    rank = scrapy.Field()
    popularity = scrapy.Field()

# class DiscussionPostItem(scrapy.Item):
#     """A post to a given discussion thread"""
#     pass
#
#
# class UserScoreItem(scrapy.Item):
#     """The score a user gave for a show"""
#     pass
