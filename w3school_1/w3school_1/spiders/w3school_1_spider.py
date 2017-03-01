from scrapy.spider import Spider
from scrapy.selector import Selector
from w3school_1.items import W3School1Item


class W3school_1Spider(Spider):
	name = 'w3school_1'
	allowed_domains = [
		'w3school.com.cn'
	]
	start_urls = [
		'http://www.w3school.com.cn/xml/xml_syntax.asp'
	]

	def parse(self, response):

		sel = Selector(response)
		print(sel)
		sites = sel.xpath('//div[@id="course"]/ul[1]/li')
		print(sites)
		items = []

		for site in sites:
			item = W3School1Item()

			title = site.xpath('a/text()').extract()
			print(title)
			link = site.xpath('a/@href').extract()
			desc = site.xpath('a/@title').extract()

			item['title'] = [t for t in title]
			item['link'] = [l for l in link]
			item['desc'] = [d for d in desc]
			items.append(item)


		return items