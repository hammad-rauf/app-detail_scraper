# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class AppdetailItem(Item):

    app_link = Field()
    category = Field()
    title = Field()
    subtitle = Field()

    developer = Field()
    feature_1 = Field()
    feature_1_desc = Field()
    feature_2 = Field()
    feature_2_desc = Field()
    feature_3 = Field()
    feature_3_desc = Field()

    full_description = Field()
    images_links = Field()
    developper_website = Field()
    privacy_policy = Field()
    email = Field()
    pricing = Field()


    pass
