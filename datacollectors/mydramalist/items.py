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
    id = scrapy.Field()  # REQUIRED
    url = scrapy.Field()  # REQUIRED
    show_ids = scrapy.Field()  # REQUIRED

    votes = scrapy.Field()  # REQUIRED
    text = scrapy.Field()  # # REQUIRED, Todo: defaults to "" should default to NULL


class ReviewItem(scrapy.Item):
    """A user review for a show"""
    id = scrapy.Field()  # REQUIRED
    url = scrapy.Field()  # REQUIRED
    show_id = scrapy.Field()  # REQUIRED
    show_title = scrapy.Field()  # REQUIRED
    post_date = scrapy.Field()  # REQUIRED
    votes = scrapy.Field()  # REQUIRED

    overall_score = scrapy.Field()  # REQUIRED # Todo: Make sure it does not default to 0
    story_score = scrapy.Field()  # REQUIRED
    acting_score = scrapy.Field()  # REQUIRED
    music_score = scrapy.Field()  # REQUIRED
    rewatch_score = scrapy.Field()  # REQUIRED

    text = scrapy.Field()  # REQUIRED, Todo: defaults to "" should default to NULL


class ShowItem(scrapy.Item):
    """Information about a drama or movie"""
    id = scrapy.Field()  # int, REQUIRED
    url = scrapy.Field()  # string, REQUIRED

    main_title = scrapy.Field()  # string, REQUIRED

    type = scrapy.Field()  # string/category, REQUIRED?? Todo: Validate and ensure not null
    content_rating = scrapy.Field()  # string/category, defaults to Not Yet Rated
    # status = scrapy.Field()  # string/category Todo
    duration = scrapy.Field()  # string, optional
    episodes = scrapy.Field()  # int, optional
    country = scrapy.Field()  # string/category, REQUIRED?? Todo: Validate and ensure not null
    network = scrapy.Field()  # string/category, optional

    # related_titles = scrapy.Field()  # list of objects/pairs, Todo
    # cast = scrapy.Field()  # List of Cast objects, Todo

    release_date = scrapy.Field()  # date string, REQUIRED Todo: Validate and ensure not null
    end_date = scrapy.Field()  # date, optional

    genres = scrapy.Field()  # list of strings, defaults to empty list
    tags = scrapy.Field()  # list of strings,  defaults to empty list

    native_title = scrapy.Field()  # string, optional
    alt_titles = scrapy.Field()  # list of strings, optional
    synopsis = scrapy.Field()  # string, REQUIRED, "" if none

    rank = scrapy.Field()  # int, default 99999
    popularity = scrapy.Field()  # int, default 99999
    score = scrapy.Field()  # int, REQUIRED, nullable
    ratings = scrapy.Field()  # int, defaults to zero
    members = scrapy.Field()  # int, REQUIRED?

# class DiscussionPostItem(scrapy.Item):
#     """A post to a given discussion thread"""
#     pass
#
#
# class UserScoreItem(scrapy.Item):
#     """The score a user gave for a show"""
#     pass
