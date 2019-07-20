from scrapy import Spider, Request
from melon.items import MelonItem
import re

def get_weekdays(_start_date):
	from datetime import datetime, timedelta

	_monday = datetime(int(_start_date.split('-')[0]), int(_start_date.split('-')[1]), int(_start_date.split('-')[2]))
	# If not Saturday, change to Saturday of the week
	_monday = _monday-timedelta(days=(_monday.weekday()))
	_sunday = _monday+timedelta(days=6)
	weekdays = []

	while True:
		weekdays.append((str(_monday.year)+twodigit(_monday.month)+twodigit(_monday.day), str(_sunday.year)+twodigit(_sunday.month)+twodigit(_sunday.day)))
		_monday = _monday + timedelta(days=7)
		_sunday = _sunday + timedelta(days=7)

		# Calculate only dates before today
		if _monday > datetime.now():
			break;

	return weekdays

def twodigit(n):
	if n<10:
		return '0'+str(n)
	else:
		return str(n)

class MelonSpider(Spider):
	name = 'melon_spider'
	allowed_urls = ['https://www.melon.com']
	start_urls = ['https://www.melon.com/chart/']

	def parse(self, response):
		# List comprehension to construct all the urls
		result_urls = ['https://www.melon.com/chart/search/list.htm?chartType=WE&age=2010&year=2012&mon=01&day={0}%5E{1}&classCd=DP0000&startDay={0}&endDay={1}&moved=Y'.format(*x) for x in get_weekdays('2013-06-13')]

		# Yield the requests to different search result urls,
		# using parse_result_page function to parse the response.
		for url in result_urls:
			print(url)
			yield Request(url=url, callback=self.parse_result_page, meta={'start_date':str(re.findall('[0-9]{8}',url)[0])})

	def parse_result_page(self, response):
		musics = response.xpath('//*[@id="frm"]/div/table/tbody/tr')

		date = response.meta['start_date']
		for music in musics:
			rank = music.xpath('.//td[2]/div/span[1]/text()').extract_first()
			album = music.xpath('.//div[@class="ellipsis rank03"]/a/text()').extract_first()
			song = music.xpath('.//div[@class="ellipsis rank01"]/span/a/text()').extract_first()
			artist = music.xpath('.//div[@class="ellipsis rank02"]/a/text()').extract_first()

			item = MelonItem()
			item['date'] = date
			item['rank'] = rank.strip()
			item['album'] = album.strip()
			item['song'] = song.strip()
			item['artist'] = artist.strip()

			yield item
