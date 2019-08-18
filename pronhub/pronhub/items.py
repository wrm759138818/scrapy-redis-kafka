# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PronhubItem(scrapy.Item):
    design = scrapy.Field()
    seed = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    hot = scrapy.Field()
    size = scrapy.Field()
    pass
