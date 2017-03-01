# 输出中文乱码
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import csv


url = 'http://shop.freebuf.com/'
data = urlopen(url).read()
soup = BeautifulSoup(data, 'lxml')

# itemlist = soup.find_all('div', class_='col-md-12 col-lg-9 mar-top40')
# itemlist = soup.find_all('div', class_='col-sm-6 col-md-4 col-lg-4 mall-product-list')
photolist = soup.find_all('div', class_='photo')
itemlist = soup.find_all('div', class_='info')

for item in photolist:
	# print(item)
	# print(item.img)
	# print(item.img['src'])
	# print(item.img['src'][-4:])
	urlretrieve(url=item.img['src'], filename=item.img['alt']+item.img['src'][-4:])
# print(itemlist)

with open('items.csv', 'w+') as csvFile:
	writer = csv.writer(csvFile)

	writer.writerow(('name', 'price'))
	for item in itemlist:
		# print(item)
		name = item.find(name='h4').string
		print(name)
		price = item.find(name='strong').string
		# print(price)
		writer.writerow((name.encode('utf-8'), price.encode('utf-8')))
