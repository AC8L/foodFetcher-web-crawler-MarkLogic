__author__ = 'sazari'
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class foodFetcherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uuid = Field()
    crawledTime = Field()
    title = Field()
    url = Field()
    fullText = Field()
    titleSHA1 = Field()
    urlSHA1 = Field()
    fullTextSHA1 = Field()

