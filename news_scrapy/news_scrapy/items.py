# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsItem(scrapy.Item):
    link_title = scrapy.Field()
    url = scrapy.Field()
    sentiment = scrapy.Field()
    text = scrapy.Field()