from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import re


url = 'http://cuiqingcai.com/'
domain = "cuiqingcai.com"
sites = set()
visited = set()

def get_local_pages(url, domain):
	global sites
	repeat_time = 0
	pages = set()

	# 防止url读取卡住
	while True:
		try:
			print('ready to open the web')
			time.sleep(1)
			print('opening the web', url)
			r = urlopen(url, timeout=3)
			print('success to open the web')
			break
		except:
			print('open url failed!repeat')
			time.sleep(1)
			repeat_time += 1
			if repeat_time == 5:
				return

	print('reading the web')
	soup = BeautifulSoup(r.read(), 'lxml')
	print('...........')
	tags = soup.find_all('a')
	for tag in tags:
		# 避免参数传递异常
		try:
			ret = tag['href']
		except:
			print('something wrong')
			continue
		o = urlparse(ret)
		for i in o:
			print(i)

		if 'http' not in o[0]:
			print('Bad page', ret)
			continue

		if domain not in o[1]:
			print('Bad page', ret)
			continue

		newpage = ret
		if newpage not in sites:
			print('add new page:', newpage)
			pages.add(newpage)
	return pages


# dft算法遍历全站
def dfs(pages):
	# 无法获取新的url说明遍历完成，结束dfs
	if not pages:
		return
	global url
	global domain
	global sites
	global visited
	sites.union(pages)
	# sites = set.union(sites, pages)
	for page in pages:
		if pages not in visited:
			print('visiting', page)
			visited.add(page)
			url = page
			pages = get_local_pages(url, domain)
			dfs(pages)

	print('success')

pages = get_local_pages(url, domain)
dfs(pages)
for i in sites:
	print(i)

