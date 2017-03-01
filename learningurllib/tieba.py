# coding=utf-8

from urllib.request import Request,urlopen
from urllib import error
import re

#处理页面标签类
class Tool:
    #去除img标签，7位长空格
    removeImg=re.compile('<img.*?>| {7}')
    #删除超链接标签
    removeAddr=re.compile('<a.*?>|</a>')
    #换行标签换为\n
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>换为\t
    replaceTD=re.compile('<td>')
    #段落开头换为\n加空两格
    replacePara=re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR=re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag=re.compile('<.*?>')
    def replace(self,x):
        x=re.sub(self.removeImg,'',x)
        x=re.sub(self.removeAddr,'',x)
        x=re.sub(self.replaceLine,'\n',x)
        x=re.sub(self.replaceTD,'\t',x)
        x=re.sub(self.replacePara,'\n',x)
        x=re.sub(self.replaceBR,'\n',x)
        x=re.sub(self.removeExtraTag,'',x)
        #strip()将前后多余内容删除
        return x.strip()

class Tieba:

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seedLZ,floorTag):
        #base链接地址
        self.baseUrl=baseUrl
        #是否只看楼主
        self.seedLZ='?see_lz='+str(seedLZ)
        #html标签剔除工具类对象
        self.tool=Tool()
        #全局file变量，文件写入操作对象
        self.file=None
        #楼层标号，初始为1
        self.floor=1
        #默认的标题，如果没有成功获取标题则用该标题
        self.defaultTitle=u'百度贴吧'
        #是否写入楼分隔符的标记
        self.floorTag=floorTag

    #传入代码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            #构建url
            url=self.baseUrl+self.seedLZ+'&pn='+str(pageNum)
            request=Request(url)
            response=urlopen(request)
            #返回UTF-8格式标码内容
            response=response.read().decode('utf-8')
            #print(response.read().decode('utf-8'))
            return response
        #无法连接时报错
        except error.URLError as e:
            if hasattr(e,'reason'):
                print('连接失败，错误原因：',e.reason)
                return None

    #获取标题
    def getTitle(self,page):
        #得到标题的正则表达式
        pattern = re.compile('core_title_txt.*?>(.*?)</h3>', re.S)
        result=re.search(pattern,page)
        if result:
            #如果存在则返回标题
            #print(result.group(1)) #测试输出
            return result.group(1).strip()
        else:
            return None

    #提取帖子页数
    def getPageNum(self,page):
        #pattern=re.compile('<span class="red.*?<span class="red">(.*?)</span>',re.S)
        pattern=re.compile('.*?max-page="(.*?)".*?')
        result=re.search(pattern, page)
        if result:
            print(result.group(1)) #测试输出
            return result.group(1).strip()
        else:
            return None

    #获取正文内容
    def getContent(self,page):
        pattern=re.compile('<div id="post_content.*?>(.*?)</div>',re.S)
        items=re.findall(pattern,page)
        contents=[]
        floor=1
        for item in items:
            #将文本剔除标签，同时在前后加入换行符
            content = '\n'+self.tool.replace(item)+'\n'
            contents.append(content.encode('utf-8'))
            #print(floor,'楼--------------------------------------------------------------------\n')
            #print(self.tool.replace(items[1]))
            #floor+=1
        return contents

    def setFileTitle(self,title):
        if title is not None:
            self.file=open(title+'.txt','wb')
        else:
            self.file=open(self.defaultTitle+'.txt','wb')

    def writeData(self,contents):
        #写入每一楼信息
        for item in contents:
            if self.floorTag=='1':
                #楼之间的分隔符
                floorLine='\n'+str(self.floor)+u'----------------------------------------------------\n'
                self.file.write(floorLine.encode())
            self.file.write(item)
            self.floor+=1

    def start(self):
        indexPage=self.getPage(1)
        pageNum=self.getPageNum(indexPage)
        title=self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum==None:
            print('URL已失效，请重试')
            return
        try:
            print('共有'+str(pageNum)+'页')
            for i in range(1,int(pageNum)+1):
                print('正在写入第'+str(i)+'页数据')
                page=self.getPage(i)
                contents=self.getContent(page)
                self.writeData(contents)
        #出现写入异常
        except IOError as e:
            print('写入异常，原因：'+e.message)
        finally:
            print('写入任务完成')

print(u'请输入帖子代号：')
baseURL='http://tieba.baidu.com/p/'+str(input(u''))
seedLZ=input('是否只看楼主，是输入1，否输入0\n')
floorTag=input('是否写入楼层信息，是输入1，否输入0\n')
#baseURL='http://tieba.baidu.com/p/3138733512'
bdtb=Tieba(baseURL,seedLZ,floorTag)
#bdtb.getPage(1)
#bdtb.getTitle()
#bdtb.getPageNum()
#bdtb.getContent()

bdtb.start()

