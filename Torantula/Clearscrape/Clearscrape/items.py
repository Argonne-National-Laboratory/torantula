# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Site(Item):
    """
    The DarkSpider generates one of these items for every response it receives.

    """
    url = Field()
    body = Field()
    links = Field()

    def __str__(self):
        return ""
