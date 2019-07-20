# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BillboardHot100Item(scrapy.Item):
	# define the fields for your item here like:
	date = scrapy.Field()
	rank = scrapy.Field()
	song = scrapy.Field()
	artist = scrapy.Field()
