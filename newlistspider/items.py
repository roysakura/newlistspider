# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewlistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    quote = scrapy.Field()
    on_stock = scrapy.Field()
    cut_off = scrapy.Field()
    philip_statistic = scrapy.Field()

    pass
