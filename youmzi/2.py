import urllib.request
import re
from bs4 import BeautifulSoup
import os
import multiprocessing
import gzip

url = 'http://www.youmzi.com/xg/list_10_1.html'
max_page = 104
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
headers = {'User-Agent': user_agent,
		   'Accept_Encoding':'gzip'
		   }

class Youmzi():

	#请求网页并进行解析
	def pageparse(self, url):
		try:
			request = urllib.request.Request(url, headers=headers)
			response = urllib.request.urlopen(request)
			response = response.read().decode('GBK')
			soup = BeautifulSoup(response, 'lxml')
			return soup
		except:
			return None

	#获取所有套图入口地址（即套图第一张的地址）
	def imgs_entry(self):
		for page in range(1, max_page + 1):
			pageurl = 'http://www.youmzi.com/xg/list_10_' + str(page) + '.html'
			soup = self.pageparse(pageurl)
			list = soup.find('div', class_='tzpic3-mzindex').find_all('a')
			for li in list:
				title = li['title']
				path = str(title).replace('?', '_')
				self.mkdir(path)
				os.chdir('F:\Image\youmzi\\' + path)
				href = li['href']
				self.mkdir(title)
				self.Img_url(href)
	# 创建目录
	def mkdir(self, path):
		try:
			folder_path = os.path.join('F:\Image\youmzi', path)
			os.makedirs(folder_path)
			print('创建名为', path, '的文件夹')
		except:
			print('文件夹已存在')
		# os.chdir('F:\Image\youmzi\\' + title)

	#所有图片的地址
	def Img_url(self, href):
		soup = self.pageparse(href)
		img_urls = []
		# 最大页码
		max_num = soup.find('ul', class_='jogger2').find_all('a')[0].get_text()
		max_num = re.sub('\D', '', max_num)
	# 构造套图各图片页url
		for i in range(1, int(max_num) + 1):
			if i == 1:
				img_url = href
			else:
				img_url = href[:-5] + '_' + str(i) + '.html'
			self.Imgurl(img_url)

	#所有图片的下载地址
	def Imgurl(self,img_url):
			soup = self.pageparse(img_url)
			# 获取图片真实地址
			# imgurl = soup.find('div', class_='xiazai').find_all('a')[0]['href']
			imgurl = soup.find('div', class_='arpic').find('img')['src']
			# img = requests.get(imgurl, headers=headers)
			if imgurl not in self.has_down():
				self.save(imgurl)
				self.record(imgurl)
				print(imgurl, '下载成功')
			else:
				return None

	#下载图片到本地文件夹
	def save(self, imgurl):
		try:
			a = urllib.request.Request(imgurl, headers=headers)
			b = urllib.request.urlopen(a)
			c = gzip.GzipFile(fileobj=b)
			d = c.read()
		except:
			a = urllib.request.Request(imgurl, headers=headers)
			b = urllib.request.urlopen(a)
			d = b.read()
		name = imgurl.split('/')[-1]
		with open(name, 'ab') as f: #wb二进制写，文件存储被清空,a追加模式，只能写在文件末尾
			f.write(d)

	#记录已下载的链接
	def record(self, imgurl):
		with open('F:\python\youmzi\has_down.txt', 'a') as f:
			f.write(imgurl)
			f.write('\n')
		# print('美女图片下载成功', imgurl)

	#链接是否下载过
	def has_down(self):
		with open('F:\python\youmzi\has_down.txt', 'r') as f:
			has_down = [line.strip() for line in f]
			return has_down

def multi_process(func):
	process_pool = []
	pool_num = multiprocessing.cpu_count() * 3
	pool = multiprocessing.Pool(processes=pool_num)
	p = pool.apply_async(func)
	process_pool.append(p)
	pool.close()
	pool.join()

if __name__ == '__main__':
	youmzi = Youmzi()
	multi_process(youmzi.imgs_entry())