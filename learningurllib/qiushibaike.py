# coding=utf-8
from urllib.request import Request, urlopen
from urllib import error
import re
import _thread
import time

#定义糗事百科爬虫类
class QSBK:

    #初始化，定义变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MISE 5.5; Windows NT)'
        #初始化headers
        self.headers = { 'User-Agent':self.user_agent }
        #存放段子的变量，每一个元素是每一页的段子
        self.stories=[]
        #存放程序是否继续运行的变量
        self.enable=False

    #传入某一页的索引以获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/8hr/page/'+str(pageIndex)+'/'
            request=Request(url,headers=self.headers)
            response=urlopen(request)
            pageCode=response.read().decode('utf-8')
            return pageCode

        except error.URLError as e:
            print('糗事百科连接失败，错误原因：',e.reason)
            return None

    #获取某一页内容
    def getPageItems(self,pageIndex):
        pageCode=self.getPage(pageIndex)
        pageStories=[]
        if not  pageCode:
            print('页面加载失败...')
            return None

        pattern = re.compile('<div class="author.*?<h2>(.*?)<.*?<span>(.*?)<.*?<i class="number">(.*?)<', re.S)
        items = re.findall(pattern, pageCode)
        for i in items:
            replaceBR=re.compile('<br/>')
            text=re.sub(replaceBR,'\n',i[1])
            #i[0]是作者，i[1]是内容，i[2]是点赞数
            pageStories.append([i[0].strip(),i[1].strip(),i[2].strip()])
        return pageStories
    #加载并提取内面内容，加入到列表
    def loadPage(self):
        #如果当前未看的页面数少于2页，则加载新一页
        if self.enable==True:
            if len(self.stories)<2:
                #获取新一页
                pageStories=self.getPageItems(self.pageIndex)
                #将该页的段子放入全局list
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完后页码索引加一，即下次读取下一页
                    self.pageIndex+=1

    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input_0=input()
            #每敲一次回车，判断是否加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input_0=='Q':
                self.enable=False
                return
            print(u'第%d页\t发布人：%s\t发布内容:%s\t赞：%s\n' % (page,story[0],story[1],story[2]))

    #开始方法
    def start(self):
        print('正在读取糗事百科，按回车查看新段子，Q退出')
        #使变量为Ture，程序正常运行
        self.enable=True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        newPage=0
        while self.enable:
            if len(self.stories)>0:
                #从全局list获取一个段子
                pageStories=self.stories[0]
                #当前读到页数加一
                newPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页段子
                self.getOneStory(pageStories,newPage)

spider=QSBK()
spider.start()



#page=1
#url = 'http://www.qiushibaike.com/8hr/page/'+str(page)+'/'
#user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#headers = {'User-Agent': user_agent}
#try:
    #request = Request(url,headers=headers)
    #response = urlopen(request)
    #content = response.read().decode('utf-8')
    #pattern = re.compile('<div class="author.*?<h2>(.*?)<.*?<span>(.*?)<.*?<i class="number">(.*?)<', re.S)
    #items = re.findall(pattern, content)
    #for i in items:
        #print(i[0], i[1], i[2])
#except error.URLError as e:
    #print(e.reason)
