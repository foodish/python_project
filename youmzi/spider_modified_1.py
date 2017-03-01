import urllib.request
import re
from bs4 import BeautifulSoup
import os
import gzip
import threading

url = 'http://www.youmzi.com/xg/list_10_1.html'
max_page = 104
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
headers = {'User-Agent': user_agent,
		   'Accept_Encoding': 'gzip'
		   }
girl_entry = []


# 请求网页并进行解析
def pageparse(url):
	request = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(request)
	response = response.read().decode('GBK')
	soup = BeautifulSoup(response, 'lxml')
	return soup


# 获得所有相册入口链接
def entry_link():
	global girl_entry
	for page in range(1, max_page + 1):
		pageurl = 'http://www.youmzi.com/xg/list_10_' + str(page) + '.html'
		request = urllib.request.Request(pageurl, headers=headers)
		response = urllib.request.urlopen(request)
		try:
			decompress = gzip.GzipFile(fileobj=response)
			content = decompress.read().decode('GBK')
		except:
			content = response.read().decode('GBK')
		list_part_pattern = re.compile(r"</dl>(.*?)</ul>", re.S)
		list_part = re.findall(list_part_pattern, content)
		repattern = re.compile(r'<li>.*?<a href="(.+?).html" title="(.+?)".*?<p><a href.*?</li>', re.S)
		girl_link_found = re.findall(repattern, list_part[0])
		for each in girl_link_found:
			girl_entry.append(each)


# 获取所有相册页面
def page_link(href):
	girl_series = []
	soup = pageparse(href)
	max_num = soup.find('ul', class_='jogger2').find_all('a')[0].get_text()
	max_num = re.sub('\D', '', max_num)
	for i in range(1, int(max_num) + 1):
		if i == 1:
			img_url = href
		else:
			img_url = href[:-5] + '_' + str(i) + '.html'
		girl_series.append(img_url)
	return girl_series


# 获取图片地址
def pic_link(url):
	link_pool = page_link(url)
	img_link = []
	for link in link_pool:
		soup = pageparse(link)
		# 获取图片真实地址
		imgurl = soup.find('div', class_='arpic').find('img')['src']
		img_link.append(imgurl)
	return img_link


# 保存图片
def save(pic_link_pool, title):
	# 创建目录
	isExists = os.path.exists(os.path.join('F:\Image\youmzi', title))  # 检查路径是否存在
	if not isExists:
		os.makedirs(os.path.join('F:\Image\youmzi', title))
		print('创建名为', title, '的文件夹')
	for link in pic_link_pool:
		name = link.split('/')[-1]
		# imgurl = soup.find('div', class_='xiazai').find_all('a')[0]['href']
		# img = requests.get(imgurl, headers=headers)
		try:
			a = urllib.request.Request(link, headers=headers)
			b = urllib.request.urlopen(a)
			c = gzip.GzipFile(fileobj=b)
			d = c.read()
		except:
			a = urllib.request.Request(link, headers=headers)
			b = urllib.request.urlopen(a)
			d = b.read()
		f = open(name, 'ab')  # wb二进制写，文件存储被清空,a追加模式，只能写在文件末尾
		f.write(d)
		f.close()
		print('妹子图下载成功')


# 对相册下载器进行封装
def worker():
	entry_link()
	global girl_entry
	while girl_entry:
		lock = threading.Lock()
		lock.acquire()
		entry_base = girl_entry.pop(0)
		lock.release()
		pic_link_pool = pic_link(entry_base[0])
		save(pic_link_pool, entry_base[1])


class worker_threads(threading.Thread):
	def __init__(self, func, thread_id):
		super(worker_threads, self).__init__()
		self.thread_id = thread_id
		self.func = func

	def run(self):
		print('线程%d启动' % self.thread_id)
		self.func()
		print('线程%d结束' % self.thread_id)


# 主函数
def main():
	threads = [worker_threads(worker, i) for i in range(1, 10)]
	for thread in threads:
		thread.start()
	for t in threads:
		t.join()


main()
