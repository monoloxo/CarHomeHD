# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarhomehdItem(scrapy.Item):
    category = scrapy.Field()       # 图片分类
    image_urls = scrapy.Field()     # 图片url
    images = scrapy.Field()     # 图片名

