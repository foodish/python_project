import scrapy
from w3school.items import W3SchoolItem
from bs4 import BeautifulSoup
from scrapy import Request


class W3schoolSpider(scrapy.Spider):
	name = 'w3school'
	allowed_domains = ['w3school.com.cn']

	def start_requests(self):
		# start_urls = [
		# 	'http://www.w3school.com.cn/xml/xml_syntax.asp'
		# ]
		# for url in start_urls:
		# 	yield Request(url=start_urls, callback=self.parse)
		url = 'http://www.w3school.com.cn/xml/xml_syntax.asp'
		yield Request(url=url, callback=self.parse)

	def parse(self, response):
		# print(response.text)
		soup = BeautifulSoup(response.text, 'lxml')
		# print(soup.prettify())
		# print(soup)
		# sites = soup.find('body', class_='xml').find(id='course').find('ul').find_all('li')
		sites = soup.find(id='course').find('ul').find_all('li')
		# sites = soup.find_all('div', id_='course').find('ul').find_all('li')
		# print('------------------------')
		# print(sites)
		items = []

		for site in sites:
			item = W3SchoolItem()
			title = site.a.text
			link = 'http://www.w3school.com.cn'+ site.a['href']
			desc = site.a['title']

			item['title'] = title
			item['link'] = link
			item['desc'] = desc
			items.append(item)
		print(items)
		return items

