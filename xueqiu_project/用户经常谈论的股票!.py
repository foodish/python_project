from urllib.request import Request, urlopen
# import json

url = 'https://xueqiu.com/user/top_status_count_stock.json?count=5&uid=1955602780&_=1487575809738'
headers = {
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  'Cookie':'xq_a_token=ce97c94e1b31d1d7d671082fddfb70064a596325'
}
response = Request(url, headers=headers)
req = urlopen(response)
r = req.read().decode('utf-8')
str = 'refered_stocks =' + r
print(str)
print(r.split('[')[1].split(']')[0])
print(r.split('{')[1].split('}')[0])


