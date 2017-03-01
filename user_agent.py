import requests
from bs4 import BeautifulSoup

url = 'http://www.useragentstring.com/pages/useragentstring.php?name=Chrome'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

content = soup.find(id='content').find_all('li')
for i in content:
	i = '    ' + '\'' + i.text + '\','
	print(i)

