from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient
from datetime import datetime
import re

class Mzitu():

    def __init__(self):
        client = MongoClient()
        db = client['meinvxiezhenji']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_urls = []

    def all_url(self, url):

        html = request.get(url, 3)
        all_a = BeautifulSoup(html.text,'lxml').find('div', {'class': 'all'}).find_all('a')
        for a in all_a:
            title = a.get_text()
            self.title = title
            print(u'开始保存：', title)
            path = str(title).replace('?', '_')
            self.mkdir(path)
            os.chdir('F:\mzitu\\'+path)
            href = a['href']
            self.url = href
            if self.meizitu_collection.find_one({'主题页面':href}):
                print(u'这个页面已经爬取过了')
            else:
                self.html(href)

    def html(self, href):
        html = request.get(href, 3)
        max_page = BeautifulSoup(html.text, 'lxml').find('div', {'class': 'pagenavi'}).find_all('span')[-2].get_text()
        page_num = 0
        for page in range(1, int(max_page)+1):
            page_num = page_num + 1
            page_url = href + '/' + str(page)
            self.img(page_url, max_page, page_num)

    def img(self,page_url, max_page, page_num):
        img_html = request.get(page_url, 3)
        img_dict = BeautifulSoup(img_html.text, 'lxml').find('div', {'class': 'main-image'}).find('img')
        if img_dict is not None:
            img_url = img_dict['src']
        else:
            print(u'没有获取到img_url*******************')
            return None

        #避免非法URL干扰爬虫继续运行
        img_url_reg = re.compile('http://.*?\.jpg', re.S)
        if re.match(img_url_reg, img_url):
            self.img_urls.append(img_url)

            if int(max_page) == page_num:
                self.save(img_url)
                post = {
                    '标题':self.title,
                    '主题页面':self.url,
                    '图片地址':self.img_urls,
                    '获取时间':datetime.now()
                }
                self.meizitu_collection.save(post)
                #每次post完清空一下，不然后面太多了
                self.urls = []
                print(u'插入数据库成功')
                print('==========>>>>>>>.>DB')
            else:
                self.save(img_url)
        else:
            print(u'图片不是有效地链接地址！！！！！！！！！！！！！！')


    def save(self, img_url):
        name = img_url[-9:-4]
        #如果名字出现像12/01.jpg的话，windows会报错：no such file directory
        name = re.sub(r'/', '_', name)
        img = request.get(img_url, 3)
        # 打开写入文件，ab为追加二进制模式，因为要写入图片
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path=path.strip()
        isExists = os.path.exists(os.path.join('F:\mzitu', path))
        if not isExists:
            print(u'创建一个名为', path, u'的文件夹！')
            os.makedirs(os.path.join('F:\mzitu',path))
            return True
        else:
            print(u'文件夹已经存在！')
            return False

mzitu = Mzitu()
mzitu.all_url('http://www.mzitu.com/all')