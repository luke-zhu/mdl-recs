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

    votes = scrapy.Field()
    text = scrapy.Field()


class ReviewItem(scrapy.Item):
    """A user review for a show"""
    id = scrapy.Field() # Required
    url = scrapy.Field() # Required
    show_id = scrapy.Field() # Required
    show_title = scrapy.Field()  # The name of the show,
    post_date = scrapy.Field()
    votes = scrapy.Field()  # THe number of helpful votes

    overall_score = scrapy.Field()
    story_score = scrapy.Field()
    acting_score = scrapy.Field()
    music_score = scrapy.Field()
    rewatch_score = scrapy.Field()

    text = scrapy.Field()


class ShowItem(scrapy.Item):
    """Information about a drama or movie"""
    id = scrapy.Field() # int, not null
    url = scrapy.Field() # string, not null

    main_title = scrapy.Field() # string, not null
    native_title = scrapy.Field() # string, not null, Todo
    alt_titles = scrapy.Field() # list of strings, Todo

    type = scrapy.Field() # string/category, Todo
    content_rating = scrapy.Field() # string/category, Todo
    status = scrapy.Field() # string/category, Todo
    duration = scrapy.Field() # int, Todo: the current version fails
    episodes = scrapy.Field() # int, Todo: check if current episodes always returns the right values

    country = scrapy.Field()  # Todo: Consider co-productions
    network = scrapy.Field()  # Todo: Consider release

    related_titles = scrapy.Field() # list of objects/pairs, Todo

    cast = scrapy.Field() # List of Cast objects, Todo

    release_date = scrapy.Field() # date string not null, Todo
    end_date = scrapy.Field() # date, Todo

    genres = scrapy.Field()
    tags = scrapy.Field()  # Todo

    rank = scrapy.Field()
    popularity = scrapy.Field()
    score = scrapy.Field()
    ratings = scrapy.Field()
    members = scrapy.Field()

# class DiscussionPostItem(scrapy.Item):
#     """A post to a given discussion thread"""
#     pass
#
#
# class UserScoreItem(scrapy.Item):
#     """The score a user gave for a show"""
#     pass
