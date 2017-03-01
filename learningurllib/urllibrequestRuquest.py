# coding=utf-8
import urllib.request

request=urllib.request.Request('http://python.org')
response=urllib.request.urlopen(request)
print(response)
print(response.read())
print('-------------')
print(response.read().decode('utf-8'))