# wiki六度分割理论 from 《python网络数据采集》
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='mysql')
cur = conn.cursor()
cur.execute('USE scraping')

cur.execute('select * from pages where id=2')
print(cur.fetchone())
cur.close()
conn.close()
