import urllib.request
import re
from bs4 import BeautifulSoup
import sys
import gzip

with open('has_down.txt', 'r') as f:
	url ='http://ymz.qqwmb.com/allimg/c161111/14NW060291E0-4O919.jpg'


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
headers = {'User-Agent': user_agent,
		   'Accept-Encoding': 'gzip'
		   }
girl_entry = []
pageurl = 'http://www.youmzi.com/xg/list_10_' + str(1) + '.html'
request = urllib.request.Request(pageurl, headers=headers)
response = urllib.request.urlopen(request)
decompress = gzip.GzipFile(fileobj=response)
content = decompress.read().decode('GBK')
list_part_pattern = re.compile(r"</dl>(.*?)</ul>", re.S)
list_part = re.findall(list_part_pattern, content)
repattern = re.compile(r'<li>.*?<a href="(.+?).html" title="(.+?)".*?<p><a href.*?</li>', re.S)
girl_link_found = re.findall(repattern, list_part[0])
for each in girl_link_found:
	# print(each)
	girl_entry.append(each)
	# print('---------------------------------')
	# print(girl_entry)
	# print('---------------------------------')
	# print(girl_entry[0])
url = 'http://www.youmzi.com/xg/list_10_1.html'
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
response = response.read().decode('GBK')
# print(response.read().decode('GBK'))
soup = BeautifulSoup(response, 'lxml')
max_page = soup.find('div', class_='jogger').find_all('li')[-1] #<li><span class="pageinfo">共 <strong>104</strong>页<strong>3104</strong>条</span></li>
max_page = max_page.get_text()
# print(max_page)
# print(type(max_page))
# imgurl = soup.find('div', class_='arpic').find('img')['src']
# print(imgurl)
# print(soup)
#最大页码
# page_num = soup.find('ul', class_='jogger2').find_all('a')[0].get_text()
# pattern = re.compile('共')
# num = page_num.sub(pattern, page_num)
# a = page_num.replace('共', '')
# b = a.replace('页', '')
# c = b.replace(':','')
# d = c.replace(' ', '')
# print(d)
# print(int(d))
# f = re.sub('\D','', page_num)
# print(f)
# for i in page_num:
	# print(i)
imgurl = 'http://css.youmzi.com/showpic.html?/uploads/allimg/c161111/14NW060291E0-4O919.jpg'
youmzi_path = 'F:\Image\youmzi\\'
title = '高清美女性感图片大合集'
folder_path = youmzi_path + title
# print(folder_path)
name = imgurl.split('/')[-1]
img_path = folder_path + '\\' + name
# print(img_path)
def call_back(blocknum, blocksize, totalsize):
    # @blocknum: 已经下载的数据块    @blocksize: 数据块的大小    @totalsize: 远程文件的大小
    percent = 100.0 * blocknum * blocksize / totalsize
    sys.stdout.write("\rDownloading : %.2f%%\r" % percent) ##类似于print，print相当于sys.stdout.write加上\n（换行）
    sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write("\rDownloading : %.2f%% -> " % 100)
        print('Download_Success ')

# urllib.request.urlretrieve(imgurl, img_path, call_back)