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
    id = scrapy.Field()  # Required
    url = scrapy.Field()  # Required
    show_ids = scrapy.Field()  # Required

    votes = scrapy.Field()
    text = scrapy.Field()


class ReviewItem(scrapy.Item):
    """A user review for a show"""
    id = scrapy.Field()  # Required
    url = scrapy.Field()  # Required
    show_id = scrapy.Field()  # Required
    show_title = scrapy.Field()
    post_date = scrapy.Field()
    votes = scrapy.Field()  # The number of helpful votes

    overall_score = scrapy.Field()
    story_score = scrapy.Field()
    acting_score = scrapy.Field()
    music_score = scrapy.Field()
    rewatch_score = scrapy.Field()

    text = scrapy.Field()


class ShowItem(scrapy.Item):
    """Information about a drama or movie"""
    id = scrapy.Field()  # int, required
    url = scrapy.Field()  # string,required

    main_title = scrapy.Field()  # string, required
    native_title = scrapy.Field()  # string, required
    alt_titles = scrapy.Field()  # list of strings,
    synopsis = scrapy.Field()

    type = scrapy.Field()  # string/category
    content_rating = scrapy.Field()  # string/category
    status = scrapy.Field()  # string/category
    duration = scrapy.Field()  # string
    episodes = scrapy.Field()  # int

    country = scrapy.Field()  #
    network = scrapy.Field()  #

    related_titles = scrapy.Field()  # list of objects/pairs, Todo

    cast = scrapy.Field()  # List of Cast objects, Todo

    release_date = scrapy.Field()  # date string not null
    end_date = scrapy.Field()  # date

    genres = scrapy.Field()
    tags = scrapy.Field()

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
