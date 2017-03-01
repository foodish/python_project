# coding=utf-8
#refer:http://cuiqingcai.com/1052.html?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io
import urllib.request
import urllib.parse

response=urllib.request.urlopen('https://www.python.org')
print(response)
print(response.read())
print(response.read().decode('utf-8'))
print(type(response))
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))


#Request
request=urllib.request.Request('http://www.baidu.com')
response=urllib.request.urlopen(request)
print(response.read())

#post
values={'username':'','password':''} #values={} values['username']='' values['password']=''
data=bytes(urllib.parse.urlencode(values),encoding='utf-8')
url='http://httpbin.org/post'
request=urllib.request.Request(url,data) # response=urllib.request.urlopen(url,data)
response=urllib.request.urlopen(request)
print(response.read())