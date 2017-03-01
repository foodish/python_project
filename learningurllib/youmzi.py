import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen, Request
import re

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
url='http://www.youmzi.com/xg/list_10_1.html'
html=requests.get(url,headers=headers)
# print(type(html))

req=Request(url,headers=headers)
response=urlopen(req)
page=response.read()
uniCodepage=page.decode('GBK')
#print(uniCodepage)
# print(response)
# print(type(response))
#print(page)
#print(type(page)) #<class 'bytes'>
#print(html.text) #concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容, 对于打印网页内容请使用text)
#print(html)
soup=BeautifulSoup(page,'lxml')
#print(soup)
#li_list=soup.find_all('li')
li_list=soup.find('div',{'class':'tzpic3-mzindex'}).find_all('a')
for li in li_list:
    #print(li)
    #title=li.get_text()
    title=li['title']
    href=li['href']
    req = Request(href, headers=headers)
    response = urlopen(req)
    page = response.read()
    html_soup=BeautifulSoup(page,'lxml')
    pattern=re.compile('共(.*?)页')
    maxpage=re.findall(pattern,page.decode('GBK'))
    maxpage=maxpage[0]
    for page in range(1,int(maxpage)+1):
        page_url='http://www.youmzi.com/xg/201702/14440_%s.html' % page
        print(page_url)
    # print(maxpage)
    # print(title,href)

# li_list=soup.find_all('img',{'src':re.compile('http.*\.jpg')})
#
# for li in li_list:
#     title=li['alt']
#     imgUrl=li['src']
#     print(title,imgUrl)