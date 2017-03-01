import os
import time
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from Download import request
from bs4 import BeautifulSoup
import re

SLEEP_TIME = 1

def mzitu_crawler(max_threads=10):
	crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')
	def pageurl_crawl(lock):
		while True:
			try:
				url = crawl_queue.pop()
				print(url)
			except KeyError:
				print('队列没有数据')
				break
			else:
				img_urls = []
				req = request.get(url, 3).text
				title = crawl_queue.pop_title(url)
				mkdir(title)
				with lock:
					os.chdir('F:\mzitu\\' + title)
					max_page = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
					for page in range(1, int(max_page) + 1):
						page_url = url + '/' + str(page)
						img_url = BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', {'class': 'main-image'}).find('img')
						img_urls.append(img_url)
						save(img_url)

	def save(img_url):
		name = img_url[-9:-4]
		print(u'开始保存：', img_url)
		img = request.get(img_url, 3)
		f = open(name + '.jpg', 'ab')
		f.write(img.content)
		f.close()

	def mkdir(path):
		path = path.strip()
		isExists = os.path.exists(os.path.join('F:\mzitu', path))
		if not isExists:
			print(u'创建一个名为', path, u'的文件夹！')
			os.makedirs(os.path.join('F:\mzitu', path))
			return True
		else:
			print(u'文件夹已经存在！')
			return False

	threads = []
	while threads or crawl_queue:
		"""
		这儿用到了crawl_queue,就是__bool__函数的作用，为真则代表mongo数列里还有数据
		threads 或者 crawl_queue为真都代表还没下载完，程序继续执行
		"""
		for thread in threads:
			# is_alive判断是否为空，不是空则在队列中删掉
			if not thread.is_alive():
				threads.remove(thread)
				# 线程池中的线程小于max_threads 或者 crawl_queue
		while len(threads) < max_threads or crawl_queue.peek():
			thread = threading.Thread(target=pageurl_crawl) ##创建线程
			thread.setDaemon(True) ##设置守护线程
			thread.start() ##启动线程
			threads.append(thread) ##添加进线程队列
		time.sleep(SLEEP_TIME)

def process_crawler():
	process = []
	num_cpus = multiprocessing.cpu_count()
	print('将会启动进程数为：', num_cpus)
	for i in range(num_cpus):
		p = multiprocessing.Process(target=mzitu_crawler) ##创建进程
		p.start() #启动进程
		process.append(p)
	for p in process:
		p.join() ##等待进程队列里的进程结束

if __name__ =='__main__':
	lock = multiprocessing.Lock()
	process_crawler()
