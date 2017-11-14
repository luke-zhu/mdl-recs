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



class RecommendationItem(scrapy.Item):
    """A user recommendation for two shows"""
    id = scrapy.Field()
    url = scrapy.Field()
    show1_id = scrapy.Field()  # String, lexicographically before show2
    show2_id = scrapy.Field()
    show1_title = scrapy.Field()  # String, lexicographically before show2
    show2_title = scrapy.Field()
    date_posted = scrapy.Field()
    num_votes = scrapy.Field()
    rec_text = scrapy.Field()


class ReviewItem(scrapy.Item):
    """A user review for a show"""
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()  # The name of the show
    date_posted = scrapy.Field()
    num_votes = scrapy.Field()  # THe number of helpful votes
    overall_score = scrapy.Field()
    story_score = scrapy.Field()
    acting_score = scrapy.Field()
    music_score = scrapy.Field()
    rewatch_score = scrapy.Field()
    review_text = scrapy.Field()


class ShowItem(scrapy.Item):
    """Information about a drama or movie"""
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    date_started = scrapy.Field()
    date_ended = scrapy.Field()
    average_score = scrapy.Field()
    num_rated = scrapy.Field()
    num_watched = scrapy.Field()
    genres = scrapy.Field()
    country = scrapy.Field()
    num_episodes = scrapy.Field()
    rank = scrapy.Field()
    popularity = scrapy.Field()


class DiscussionPostItem(scrapy.Item):
    """A post to a given discussion thread"""
    pass


class UserScoreItem(scrapy.Item):
    """The score a user gave for a show"""
    pass
