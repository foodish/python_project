import scrapy
from dmoz.items import DmozItem


class DmozSpider(scrapy.Spider):
	name = 'dmoz'
	allowed_domains = ['dmoz.org']
	start_urls = [
		'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
		'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
	]

	def parse(self, response):
		for i in response.xpath('//ul/li'):
			item = DmozItem()
			item['title'] = i.xpath('a/text()').extract()
			item['link'] = i.xpath('a/@href').extract()
			item['desc'] = i.xpath('text()').extract()
			yield item
			# title = i.xpath('a/text()').extract()
			# link = i.xpath('a/@href').extract()
			# desc = i.xpath('text()').extract()
			# print(title, link, desc)

		# filename = response.url.split('/')[-2]
		# with open(filename, 'wb') as f:
		# 	f.write(response.body)