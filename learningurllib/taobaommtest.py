# coding=utf-8

from urllib.request import Request,urlopen
from urllib import error
import re
import os
import tool
from bs4 import BeautifulSoup

class Spider:

    #页面初始化
    def __init__(self):
        self.siteURL='https://mm.taobao.com/json/request_top_list.htm'
        self.tool=tool.Tool()

    #获取索引页面的内容
    def getPage(self, pageIndex):
        url=self.siteURL+'?page='+str(pageIndex)
        # print(url)
        try:
            request = Request(url)
            response=urlopen(request)
            response=response.read().decode('gbk')
            # print(response)
            return response
        except error.URLError as e:
            print('连接失败')

    #获取索引界面所有MM的信息，list格式
    def getContents(self,pageIndex):
        page=self.getPage(pageIndex)
        pattern=re.compile('lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?data-userid="(.*?)">',re.S)
        items = re.findall(pattern,page)
        #print(items)
        contents=[]
        for item in items:
            # print(item)
            # print(item[0])
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents

    # 获取MM个人详情页面
    def getDetailPage(self, infoURL):
        response = urlopen(infoURL)
        response=response.read().decode('gbk')
        #print(response)
        return response

    # 获取个人基本信息
    def getBrief(self, id):
        url = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id'+str(id)
        html=urlopen(url)
        bs0bj=BeautifulSoup(html.read().decode('gbk'),'lxml')
        #print(bs0bj)
        # page = self.getDetailPage(url)
        # #print(page)
        # pattern = re.compile('<.*?>(.*?)<.*?>')
        # result=re.findall(pattern,page)
        # #result = re.search(pattern, page)
        # print(result)
        # return self.tool.replace(result.group(1))

    # 获取页面所有图片
    def getAllImg(self, url):
        page=urlopen(url).read().decode('gbk')
        pattern = re.compile('<img src="(.*?)" width')
        # 获取页面所有图片链接
        imageUrls = re.findall(pattern, page)
        images=[]
        for imgurl in imageUrls:
            imgurl='http:'+imgurl
            images.append(imgurl)
            #print(images)
        #print(content)
        # 从代码中提取图片
        # patternImg = re.compile()
        # images = re.findall(patternImg, content.group(1))
        return images

        # 保存多张写真图片
    def saveImgs(self, images, name):
        number = 1
        n=len(images)
        print('发现', name, '共有',n, '张照片')
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = 'jpg'
            fileName = name + '/' + str(number) + '.' + fTail
            self.saveImgs(imageURL, fileName)
            number += 1

 #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取第一页淘宝MM列表
        contents=self.getContents(pageIndex)
        for item in contents:
            #item[0]URL，item[1]姓名，item[2]年龄，item[3]居住地，item[4]id
            print('发现一位模特，名字叫',item[1],'芳龄',item[2],'她在',item[3],'她的id是',item[4])
            print('正在偷偷保存',item[1],'的信息')
            #个人详情页URL
            detailURL='https:'+item[0]
            print('又意外发现她的个人地址是', detailURL)
            #得到个人详情页代码
            detailPage=self.getDetailPage(detailURL)
            #获取所有图片列表
            imgUrl='https://mm.taobao.com/self/album/open_album_list.htm?user_id%20='+str(item[4])
            images=self.getAllImg(imgUrl)
            # self.mkdir(item[2])
            # #保存个人简介
            # self.saveBrief(brief,item[2])
            # #保存头像
            # self.saveIcon(item[1],item[2])
            #保存图片
            self.saveImgs(images,item[1])
a=Spider()
#a.getPage(1)
# a.getContents(1)
#a.savePageInfo(1)
#a.savePageInfo(1)
a.savePageInfo(1)


