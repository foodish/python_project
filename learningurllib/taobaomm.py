# coding=utf-8

from urllib.request import Request,urlopen
from urllib import error
import re
import os
import tool

class Spider:

    #页面初始化
    def __init__(self):
        self.siteURL='https://mm.taobao.com/json/request_top_list.htm'
        self.tool=tool.Tool()

    #获取索引页面的内容
    def getPage(self,pageIndex):
        url=self.siteURL+'?page='+str(pageIndex)
        #print(url)
        try:
            request = Request(url)
            response=urlopen(request)
            response=response.read().decode('gbk')
            #print(response)
            return response
        except error.URLError as e:
            print('连接失败')

    #获取索引界面所有MM的信息，list格式
    def getContents(self,pageIndex):
        page=self.getPage(pageIndex)
        pattern = re.compile('lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?data-userid="(.*?)">',re.S)
        items = re.findall(pattern,page)
        contents=[]
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents
            # print(item)
            # print('---------------------------------------------------------------------------------\n')
            # print(item[0])

    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        response=urlopen(infoURL)
        response=response.read().decode('gbk')
        return response

    #获取个人文字简介
    # def getBrief(self,page):
    #     pattern=re.compile()
    #     result=re.search(pattern,page)
    #     return self.tool.replace(result.group(1))

    #获取页面所有图片
    def getAllImg(self,page):
        pattern=re.compile()
        #个人信息页面所有代码
        content=re.search(pattern,page)
        #从代码中提取图片
        patternImg=re.compile()
        images=re.findall(patternImg,content.group(1))
        return images

    #保存多张写真图片
    def saveImgs(self,images,name):
        number=1
        print('发现',name,'共有',len(images),'张照片')
        for imageURL in images:
            splitPath=imageURL.split('.')
            fTail=splitPath.pop()
            if len(fTail) > 3:
                fTail='jpg'
            fileName=name+'/'+str(number)+'.'+fTail
            self.saveImg(imageURL,fileName)
            number+=1

    #保存头像
    def saveIcon(self,iconURL,name):
        splitPath=iconURL.split('.')
        fTail=splitPath.pop()
        fileName=name+'/icon.'+fTail
        self.saveImg(iconURL,fileName)

    #保存个人简介
    def saveBrief(self,content,name):
        fileName=name+'/'+name+'.txt'
        f = open(fileName, 'wb')
        print(u'正在偷偷保存她的个人信息为', fileName)
        f.write(content.encode('utf-8'))

    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
        u=urlopen(imageURL)
        data=u.read()
        f=open(fileName,'wb')
        f.write(data)
        f.close()

    #创建新目录
    def mkdir(self,path):
        path=path.strip()
        #判断路径是否存在，存在 True；不存在 False
        isExists=os.path.exists(path)
        #判断结果
        if not isExists:
            #不存在则创建目录
            print('偷偷新建了名字叫做',path,'的文件夹')
            #创建目录操作函数
            os.makedirs(path)
            return True
        else:
            #目录存在则不创建，并提示目录已存在
            print('文件夹已存在')
            return False

     #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取第一页淘宝MM列表
        contents=self.getContents(pageIndex)
        for item in contents:
            #item[0]个人详情URL,item[1]头像URL，item[2]姓名item[3]年龄item[4]居住地
            # item[0]URL，item[1]姓名，item[2]年龄，item[3]居住地，item[4]id
            print('发现一位模特，名字叫', item[1], '芳龄', item[2], '她在', item[3], '她的id是', item[4])
            print('正在偷偷保存', item[1], '的信息')
            #个人详情页URL
            # https: // mm.taobao.com / self / model_info.htm?user_id = 687471686
            detailURL='https:'+item[0]
            print('又意外发现她的个人地址是:', detailURL)
            #得到个人详情页代码
            detailPage=self.getDetailPage(detailURL)
            # #获取个人简介
            # brief=self.getBrief(detailPage)
            #获取所有图片列表
            images=self.getAllImg(detailPage)
            self.mkdir(item[2])
            #保存个人简介
            self.saveBrief(brief,item[2])
            #保存头像
            self.saveIcon(item[1],item[2])
            #保存图片
            self.saveImgs(images,item[2])

    #传入起始和终止页码，获取MM照片
    def savePagesInfo(self, start, end):
        for i in range(start,end+1):
            print('正在偷偷寻找第', i, '个地方，看看MM们在不在')
            self.savePageInfo(i)

spider = Spider()
spider.savePagesInfo(2,10)

