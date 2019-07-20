from scrapy import Spider, Request
from billboard.items import BillboardItem
import re

def get_saterdays(_start_date):
	from datetime import datetime, timedelta

	_saterday = datetime(int(_start_date.split('-')[0]), int(_start_date.split('-')[1]), int(_start_date.split('-')[2]))
	# If not Saturday, change to Saturday of the week
	_saterday = _saterday+timedelta(days=5)-timedelta(days=(_saterday.weekday()))

	saterdays = []

	while True:
		saterdays.append(str(_saterday.year)+'-'+twodigit(_saterday.month)+'-'+twodigit(_saterday.day))
		_saterday = _saterday + timedelta(days=7)

		# Calculate only dates before today
		if _saterday > datetime.now():
			break;

	return saterdays

def twodigit(n):
	if n<10:
		return '0'+str(n)
	else:
		return str(n)

class BillboardSpider(Spider):
	name = 'billboard_spider'
	allowed_urls = ['https://www.billboard.com/charts/billboard-200/']
	start_urls = ['https://www.billboard.com/charts/billboard-200/']

	def parse(self, response):
		# List comprehension to construct all the urls
		# 2016-10-29
		result_urls = ['https://www.billboard.com/charts/billboard-200/{}'.format(x) for x in get_saterdays('2013-06-13')]

		# Yield the requests to different search result urls,
		# using parse_result_page function to parse the response.
		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):
		musics = response.xpath('//div[@class="chart-list-item__first-row chart-list-item__cursor-pointer"]')

		date = response.url[-10:]
		for music in musics:
			rank = music.xpath('.//div[1]/div[1]/text()').extract_first()
			album = music.xpath('.//span[@class="chart-list-item__title-text"]/text()').extract_first()
			artist = music.xpath('.//div[@class="chart-list-item__artist"]').extract_first()

			item = BillboardItem()
			item['date'] = date
			item['rank'] = rank.strip()
			item['album'] = album.strip()
			item['artist'] = re.sub('<.*?>','',artist).strip()

			yield item
