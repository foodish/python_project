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
	crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')  # 调用MogoQueue（mogodb_queue模块中）#这里是获取的url队列
	img_queue = MogoQueue('meinvxiezhenji', 'img_queue')  ##图片实际url的队列

	# 抓取页面地止
	def pageurl_crawler():
		while True:
			"""
			try....except...else(用于捕获异常)的语法：
			try:
			<语句>        #运行别的代码
			except <名字>：
			<语句>        #如果在try部份引发了'name'异常
			except <名字> as <数据>:
			<语句>        #如果引发了'name'异常，获得附加的数据
			else:
			<语句>        #如果没有异常发生

			"""
			try:
				url = crawl_queue.pop()  # MogoQueue中的pop函数，查询列队中等待抓取的对象，并改变状态
				print(url)
			except KeyError:
				print('队列没有数据')
				break
			else:
				lock = threading.Lock()
				lock.acquire()
				img_urls = []  # 创建图片地址列表备用
				req = request.get(url, 3).text  # 请求需要抓取的页面
				max_page = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()  # 获取最大页码
				title = crawl_queue.pop_title(url)  # 取出主题
				mkdir(title)  # 调用后面的mkdir函数创建名为title的文件夹
				os.chdir('F:\image\mzitu\\' + title)  # 切换到上面创建的文件夹
				for page in range(1, int(max_page) + 1):
					page_url = url + '/' + str(page)  # 构造套图中每张图片所在页面
					img_dict = BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', {'class': 'main-image'}).find('img')
					# print(img_dict)
					if img_dict is not None:
						img_url = img_dict['src']  # 获取每张图片真实地址用于此后下载
					else:
						print(u'没有获取到img_url*******************')
					img_url_reg = re.compile('http://.*?\.jpg', re.S)  # 筛选有效图片链接的正则
					if re.match(img_url_reg, img_url):
						img_urls.append(img_url)  # 添加有效图片地址到图片地址列表
					else:
						print(u'图片不是有效地链接地址！！！！！！！！！！！！！！')
					save(img_url)  # 调用后面的save函数保存有效图片
				lock.release()  # 释放锁
				crawl_queue.complete(url)  # 设置为完成状态
				img_queue.push_imgurl(title, img_urls) #插入有效图片地址到队列
				print('插入数据库成功')

	def save(img_url):
		name = img_url[-9:-4] #获取图片名字
		print(u'开始保存：', img_url)
		img = request.get(img_url, 3) #请求图片地址
		f = open(name + '.jpg', 'ab') #创建二进制的jpg文件
		f.write(img.content) #写入文件
		f.close() #关闭文件

	def mkdir(path):
		path = path.strip() #去除空格
		isExists = os.path.exists(os.path.join('F:\image\mzitu', path)) #检查路径是否存在
		if not isExists:
			print(u'创建一个名为', path, u'的文件夹！')
			os.makedirs(os.path.join('F:\image\mzitu', path)) #创建文件夹
			return True
		else:
			print(u'文件夹已经存在！')
			return False

	threads = [] #创建线程列表备用
	while threads or crawl_queue:
		"""
		这儿用到了crawl_queue,就是__bool__函数的作用，为真则代表mongo数列里还有数据
		threads 或者 crawl_queue为真都代表还没下载完，程序继续执行
		"""
		for thread in threads:
			# is_alive判断线程是否为激活的，未激活则在队列中删掉
			if not thread.is_alive():
				threads.remove(thread)
		# 线程池中的线程小于max_threads 或者 crawl_queue中还有OUTSTANDING对象
		#peek表示取出队列中状态为OUTSTANDING的对象并返回_id（URL）
		while len(threads) < max_threads or crawl_queue.peek():
			thread = threading.Thread(target=pageurl_crawler)  ##创建线程，线程中的对象为pageurl_crawler
			thread.setDaemon(True)  ##设置守护线程
			thread.start()  ##启动线程
			threads.append(thread)  ##添加进线程队列
		time.sleep(SLEEP_TIME)

#多进程处理
def process_crawler():
	process = []
	num_cpus = multiprocessing.cpu_count()  # 获取cpu核数
	print('将会启动进程数为：', num_cpus)
	for i in range(num_cpus):
		p = multiprocessing.Process(target=mzitu_crawler)  ##创建进程，进程中任务为mzitu_crawler
		p.start()  # 启动进程
		process.append(p) #添加进进程队列
	for p in process:
		p.join()  ##等待进程队列里的进程结束


if __name__ == '__main__':
	process_crawler()
