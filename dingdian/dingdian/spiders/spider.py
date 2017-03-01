import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem
"""
此处from dingdian import 错误，将spider中同名的dingdian.py改为
spider.py后未解决问题；
将dingdian项目目录左键make_directory as-->sources root后解决，
意为将当前工作的文件夹加入source_path
"""


class Myspider(scrapy.Spider):

	name = 'dingdian'
	allowed_domains = ['23us.com']
	bash_url = 'http:www.23us.com/class/'
	# bash_url = 'http:www.23us.com/map/'
	bashurl = '.html'

	def start_requests(self):
		for i in range(1,11):
			url = self.bash_url + str(i) +'_1' + self.bashurl
			yield Request(url, self.parse)
		yield Request('http://www.23us.com/quanben/1',self.parse)

	def parse(self, response):
		max_num = BeautifulSoup(response.text, 'lxml').find('div',class_='pagelink').find_all('a')[-1].get_text()
		bashurl = str(response.url)[:-7]
		for num in range(1, int(max_num) + 1):
			url =bashurl + '_' + str(num) + self.bashurl
			yield Request(url, callback=self.get_name)
			"""
			yield Request,请求新的url，后面跟的是回调函数，需要哪一个函数来处理返回值就使用哪个函数，返回值会以参数的形式传递给调用的函数
			"""

	def get_name(self, response):
		tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor_='#FFFFFF')
		for td in tds:
			"""这儿使用循环是因为find_all取出的标签是列表形式，不然没办法继续使用find"""
			novelname = td.find('a').get_text()
			novelurl = td.find('a')['href']
			yield Request(novelurl, callback=get_chapterurl, meta={'name':novelname, 'url':novelurl})

	def get_chapterurl(self, response):
		item = DingdianItem()
		item['name'] = str(response.meta['name']).replace('\xa0', 'td')
		item['novelurl'] = response.meta['url']
		category = BeautifulSoup(response.text, 'lxml').find('table').find('a').get_text()
		author = BeautifulSoup(response.text, 'lxml').find('table').find('td')[1].get_text()
		bash_url = BeautifulSoup(response.text, 'lxml').find('p', class_='btnlinks').fine('a', class_='read')['href']
		name_id = str(bash_url)[-6:-1].replace('/','')
		item['category'] = str(category).replace('/','')
		item['author'] = str(author).replace('/','')
		item['name_id'] = name_id
		return item