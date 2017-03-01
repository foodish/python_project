# http://computational-thinking.farbox.com/blog/2014-08-03-study-osn-using-python
"""
有时候运行显示某位置解码错误，但隔一会儿再运行又恢复正常

"""
import requests
from bs4 import BeautifulSoup

url = 'http://news.baidu.com/'
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text.encode('gbk'), 'lxml')
hotnews = soup.find('div', class_='hotnews').find_all('strong')
for news in hotnews:
	print(news.a['href'])
	# print(news.a.string)
	print(news.a.text)
	# print(news.a.get_text())