# 雪球用户专栏
from urllib.request import Request, urlopen
import re

url = 'https://xueqiu.com/1955602780/column'
headers = {
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  'Cookie':'xq_a_token=4939ec38314fd03eb90e7d93a689a274dfb6487e'
}
response = Request(url, headers=headers)
req = urlopen(response)
r = req.read().decode('utf-8')
pattern = re.compile('<h1 class="title">(.*?)</h1>', re.S)
column_name = re.findall(pattern, r)
print(column_name[0])
