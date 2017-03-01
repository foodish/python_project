from multiprocessing import Pool
import requests
from requests.exceptions import ConnectionError

"""运行无反应"""

def scrape(url):
	try:
		print(requests.get(url))
	except ConnectionError:
		print('error occured ', url)
	finally:
		print('URL', url, 'scraped')

if __name__ == '__mian__':
	pool = Pool(processes=3)
	urls = [
		# 'http://mzitu.com',
		'http://www.baidu.com',
		'http://youmzi.com',
		'http://jandan.net/ooxx',
		'http://meizitu.com'
	]
	pool.map(scrape, urls)