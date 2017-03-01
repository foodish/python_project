#字符串编码问题
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='0728xiaobo', db='mysql')
cur = conn.cursor()
cur.execute('USE scraping')
url = 'http://shop.freebuf.com/'
data = urlopen(url).read()
soup = BeautifulSoup(data, 'lxml')
itemlist = soup.find_all('div', class_='info')

for item in itemlist:
	name = item.find(name='h4').string
	print(name)
	price = item.find(name='strong').string
	query = 'insert item(name,price) value('+"\'" +name+"\',"+price+');'
	cur.execute(query)

conn.commit()

query = 'select * from item where1;'
cur.execute(query)
print(cur.fetchall())

cur.close()
conn.close()