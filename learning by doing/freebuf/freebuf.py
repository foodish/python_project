"""
http://www.freebuf.com/news/topnews/96821.html
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def get_all_url(url):
	urls = []
	r = urlopen(url)
	soup = BeautifulSoup(r.read(), 'lxml')
	tags_a = soup.find_all('a',{'href':re.compile('^https?://')})
	try:
		for a in tags_a:
			href = a['href']
			text = a.get_text()
			urls.append(href)
	except:
		pass
	return urls

def get_local_url(url):
	local_urls = []
	remote_urls = []
	urls = get_all_url(url)
	for _url in urls:
		ret = _url
		if 'freebuf' in ret.replace('//','').split('.'):
			local_urls.append(_url)
		else:
			remote_urls.append(_url)
	return local_urls, remote_urls

def __main__():
	url = 'http://freebuf.com/'
	lurls, rurls = get_local_url(url)
	print('------remote urls------')
	for ret in rurls:
		print(ret)
	print('------local urls----------')
	for ret in lurls:
		print(ret)

if __name__ == '__main__':
	__main__()