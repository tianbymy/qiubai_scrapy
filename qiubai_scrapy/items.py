# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaiItem(scrapy.Item):
    # uuid
    uuid = scrapy.Field()
    # 作者
    name = scrapy.Field()
    avator = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()
    # 内容
    content = scrapy.Field()
    thumb = scrapy.Field()
    # 其他
    vote = scrapy.Field()
    comment = scrapy.Field()
