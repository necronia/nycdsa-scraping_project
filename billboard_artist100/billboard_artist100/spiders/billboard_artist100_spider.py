from scrapy import Spider, Request
from billboard_artist100.items import BillboardArtist100Item
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

class BillboardArtist100Spider(Spider):
	name = 'billboard_artist100_spider'
	allowed_urls = ['https://www.billboard.com/charts/artist-100/']
	start_urls = ['https://www.billboard.com/charts/artist-100/']

	def parse(self, response):
		# List comprehension to construct all the urls
		# 2016-10-29
		result_urls = ['https://www.billboard.com/charts/artist-100/{}'.format(x) for x in get_saterdays('2013-06-13')]

		# Yield the requests to different search result urls,
		# using parse_result_page function to parse the response.
		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):
		datagroups = response.xpath('//*[@class="chart-list chart-details__left-rail"]')

		date = response.url[-10:]

		for ii, datagroup in enumerate(datagroups):
			datas = datagroup.xpath('./div')
			#print(str(ii)+' ^'*10)
			for i, data in enumerate(datas):
				#print(str(i)+ ' -'*10)
				#print(data.xpath('./*').getall())
				#print('='*10)
				#import pdb;pdb.set_trace()
				if data.xpath('./div[1]').getall()[0][12:14] == 'ad':
					continue

				#print('-'*10)
				#print(data.getall())
				#print('-'*10)
				#rank = data.xpath('.//div[1]/div[1]/div/text()').extract_first()
				rank = data.xpath('./div[1]/div[1]/div[1]').extract_first()
				artist = data.xpath('.//span[@class="chart-list-item__title-text"]').extract_first()
				item = BillboardArtist100Item()
				item['date'] = date
				#item['rank'] = re.sub('<.*?>','',rank).strip()
				item['rank'] = re.sub('<.*?>','',rank).strip()
				item['artist'] = re.sub('<.*?>','',artist).strip()
				#print(item)
				yield item
