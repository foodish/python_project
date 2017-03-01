import http.cookiejar
import urllib.request
import urllib.parse

cookie=http.cookiejar.CookieJar() #声明CookieJar对象
handler=urllib.request.HTTPCookieProcessor(cookie) #构建handler
opener=urllib.request.build_opener(handler) #构建opener
response=opener.open('https://www.baidu.com')
for item in cookie:
    print(item.name+'='+item.value)

#output to txt
filename='cookie.txt'
cookie=http.cookiejar.MozillaCookieJar(filename)
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
response=opener.open('https://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)

filename='cookie.txt'
cookie=http.cookiejar.LWPCookieJar(filename)
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
response=opener.open('https://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)


#read cookie file
cookie=http.cookiejar.LWPCookieJar()
cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
response=opener.open('https://www.baidu.com')
print(response.read())
#print(response.read().decode('utf-8'))

#使用cookie模拟登陆网站
filename='cookie_1.txt'
cookie=http.cookiejar.MozillaCookieJar(filename)
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
passinfo={'username':'xxxxxx','password':'xxxxxx'}
data=bytes(urllib.parse.urlencode(passinfo),encoding='utf-8')
loginUrl='http://kindle10000.com/member.php?mod=logging&action=login'
result=opener.open(loginUrl,data)
cookie.save(ignore_discard=True,ignore_expires=True)
Url='http://www.kindle10000.com/forum.php?mod=viewthread&tid=131072'
result=opener.open(Url)
print(result.read())