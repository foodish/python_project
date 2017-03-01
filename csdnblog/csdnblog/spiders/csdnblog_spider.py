from scrapy import Spider
from scrapy import Request
from csdnblog.items import CsdnblogItem
from bs4 import BeautifulSoup


class CsdnblogSpider(Spider):
	name = 'csdnblog'

	#减慢爬取速度为1s
	download_delay = 1
	allow_domains = ['blog.csdn.net']

	def start_requests(self):
		start_urls = 'http://blog.csdn.net/u012150179/article/details/11749017'
		yield Request(url=start_urls, callback=self.parse)

	def parse(self, response):
		# print('-------------')
		# print(response)
		soup = BeautifulSoup(response.text, 'lxml')
		content = soup.find('span', class_='link_title')
		item = CsdnblogItem()
		# print('-----------')
		# print(content)
		try:
			# article_url = 'http://blog.csdn.net' + content.a['href']
			article_url = response.url
			# article_name = content.a.text  # "article_name": "\r\n        写在开始            \r\n        "
			#article_name = content.a.get_text() # "article_name": "\r\n        写在开始            \r\n

			article_name = content.a.text.strip()  # 去除空白等
			# print('------------')
			# print(article_name)

			item['article_name'] = article_name
			item['article_url'] = article_url

			yield item # 最开始在最后用的return item，但进入不了pipelines，改为yield即可

			url = soup.find('li', class_='next_article').a['href']
			# print('-----------------------')
			# print(url)
			# print(url)
			url = 'http://blog.csdn.net' + url
			# print('-----------------------')
			# print(url)
			yield Request(url, callback=self.parse)
		except:
			pass
		# print('-------------')
		# print(item)

