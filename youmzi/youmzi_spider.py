import urllib.request
import re
from bs4 import BeautifulSoup
import os
import requests

url = 'http://www.youmzi.com/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
headers = {'User-Agent': user_agent}
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
response = response.read().decode('GBK')
# print(response.read().decode('GBK'))
soup = BeautifulSoup(response, 'lxml')
# print(soup)
list = soup.find('div', class_='tzpic3-mzindex').find_all('a')
# print(list)
for li in list:
	title = li['title']
	href = li['href']
	# print(title, href)
	# 创建目录
	# youmzi_path = 'F:\Image\youmzi'
	# folder_path = youmzi_path + title
	isExists = os.path.exists(os.path.join('F:\Image\youmzi', title))  # 检查路径是否存在
	if not isExists:
		os.makedirs(os.path.join('F:\Image\youmzi', title))
	os.chdir('F:\Image\youmzi\\' + title)
	# if not os.path.exists(folder_path):
	# 	os.makedirs(folder_path)
	request = urllib.request.Request(href, headers=headers)
	response = urllib.request.urlopen(request)
	response = response.read().decode('GBK')
	# print(response.read().decode('GBK'))
	soup = BeautifulSoup(response, 'lxml')
	# 最大页码
	max_num = soup.find('ul', class_='jogger2').find_all('a')[0].get_text()
	# print(max_num)
	max_num = re.sub('\D', '', max_num)
	# 第一页是http://www.youmzi.com/14485.html，后面各页为http://www.youmzi.com/14485_2.html
	# 构造图片页url
	for i in range(1, int(max_num) + 1):
		if i == 1:
			img_url = href
		else:
			img_url = href[:-5] + '_' + str(i) + '.html'
		# print(img_url)
		request = urllib.request.Request(img_url, headers=headers)
		response = urllib.request.urlopen(request)
		response = response.read().decode('GBK')
		soup = BeautifulSoup(response, 'lxml')
		# 获取图片真实地址
		# imgurl = soup.find('div', class_='xiazai').find_all('a')[0]['href']
		imgurl = soup.find('div', class_='arpic').find('img')['src']
		img = requests.get(imgurl, headers=headers)
		# request = urllib.request.Request(img_url, headers=headers)
		# response = urllib.request.urlopen(request)
		print(imgurl)
		name = imgurl.split('/')[-1]
		# print(name)
		f = open(name, 'ab') #wb二进制写，文件存储被清空,a追加模式，只能写在文件末尾
		f.write(img.content)
		f.close()
		# img_path = folder_path + '\\' + name
		# print(img_path)
		# img_cpntent =