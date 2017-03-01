# Coding=utf-8
# Author By2048 Time 2017-1-18
import os
import urllib
import urllib.request
from bs4 import BeautifulSoup
import multiprocessing
import re
import socket
import sys

# 基本环境设置 超时等待时间 下载路径 进程池数量 已经下载的文件路径 浏览器标识
wait_time = 10
socket.setdefaulttimeout(wait_time) ##设置超时时间，避免爬虫在某个页面停留过久
pool_num = multiprocessing.cpu_count() * 3 ##获得当前cpu核数，设置进程池数量为其3倍
mzitu_path = "F:\\Image\\mzitu\\" ##设置文件下载路径
has_down_txt = "has_down.txt" ##存放已经下载的文件
start_url = 'http://www.mzitu.com/all' ##起始抓取地址
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
headers = {'User-Agent': user_agent}


# 连接类 连接名字 连接地址
class meizi:
    title = ""
    link = ""

    def __init__(self, title, link):
        self.title = title
        self.link = link


# 编码转换 去除非 汉字 英文字符
def change_coding(inStr):
    outStr = ""
    is_zh = re.compile(r"[\u4e00-\u9fff]")
    is_en = re.compile(r"[A-Za-z]")
    is_num = re.compile(r"[0-9]")
    is_spaces = re.compile(r"[\s]+")
    is_point = re.compile(r".")
    is_backslash = re.compile(r"\\")
    is_question_mark = re.compile(r"\?")
    is_exclamation_point = re.compile(r"! ")
    try:
        for word in inStr:
            if re.match(is_zh, word) != None:
                outStr += re.match(is_zh, word).group()
            elif re.match(is_en, word) != None:
                outStr += re.match(is_en, word).group()
            elif re.match(is_num, word) != None:
                outStr += re.match(is_num, word).group()
            elif re.match(is_spaces, word) != None:
                outStr += " "
            elif re.match(is_backslash, word) != None:
                outStr += ""
            elif re.match(is_point, word) != None:
                outStr += "."
            elif re.match(is_question_mark, word) != None:
                outStr += ""
            elif re.match(is_exclamation_point, word) != None:
                outStr += ""
    except:
        print("Change_Coding_Fail")
    finally:
        if (len(outStr) == 0):
            return "EmptyName"
        else:
            return outStr


# 创建下载文件夹目录文件目录
def create_keep_path(title):
    folder_path = mzitu_path + title
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# 根据图片下载连接获取图片名字
def get_image_name(link):
    return link.split('/')[-1]


# 获取主页下所有的meizi连接
def get_all_link(start_url):
    all_meizi_link = []
    html = urllib.request.Request(start_url, headers=headers)
    request = urllib.request.urlopen(html)
    soup = BeautifulSoup(request, "html.parser")
    all_ul = soup.find_all('ul', class_='archives')
    for ul in all_ul:
        links = ul.find_all('a')
        for link in links:
            tmp = meizi(change_coding(link.get_text()), link['href'])
            all_meizi_link.append(tmp)
    return all_meizi_link


# 获取一个页面的最大图片数量 方便合成连接
def get_max_num(link):
    html = urllib.request.Request(link, headers=headers)
    request = urllib.request.urlopen(html)
    soup = BeautifulSoup(request, "html.parser")
    for span in soup.find('div', class_='pagenavi').find_all('span'):
        if (span.get_text() == '下一页»'):
            max_num = span.parent.previous_sibling.find('span').get_text()
    return int(max_num)


# 获取图片下载连接
def get_img_down_link(link):
    html = urllib.request.Request(link, headers=headers)
    request = urllib.request.urlopen(html)
    soup = BeautifulSoup(request, "html.parser")
    img_down_link = []
    try:
        imgs = soup.find('div', class_='main-image').find_all('img')
        for img in imgs:
            img_down_link.append(img['src'])
            print('meizi_img_down_link : {0}'.format(img['src']))
    except:
        print('Get_img_link_fail')
    finally:
        return img_down_link


# 使用进程 获取主页连接下所有的图片下载连接
def get_down_link_list(link, max_num):
    pool_resule = [] ##初始进程池为空
    pool = multiprocessing.Pool(processes=pool_num) ##进程池，提供指定数量的进程，这里为12个进程
    for cnt in range(1, max_num + 1):
        detail_link = link + '/' + str(cnt)
        pool_resule.append(pool.apply_async(get_img_down_link, (detail_link,))) ##pool使用非阻塞方式，同时可进行多个进程，即多个get_img_link同时进行
    pool.close() ##关闭pool，使其不再接受新的任务
    pool.join() ##主进程阻塞，等待子进程结束
    # for tmp in pool_down_link:
    # 	print(tmp)
    # 	tmp_list.append(tmp.get())
    # down_link = [item for sub in tmp_list for item in sub]
    down_link = [item for sub in pool_resule for item in sub.get()]
    return down_link

# 下载回显
def call_back(blocknum, blocksize, totalsize):
    # @blocknum: 已经下载的数据块    @blocksize: 数据块的大小    @totalsize: 远程文件的大小
    percent = 100.0 * blocknum * blocksize / totalsize
    sys.stdout.write("\rDownloading : %.2f%%\r" % percent) ##类似于print，print相当于sys.stdout.write加上\n（换行）
    sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write("\rDownloading : %.2f%% -> " % 100)
        print('Download_Success ')


# 下载图片
def download(link, path):
    try:
        urllib.request.urlretrieve(link, path, call_back) #urlretrieve可以下载url上的内容到path，call_back为回调函数，可用来显示下载进度
    except:
        pass
        # print("Download_fail "+link+" "+path )


# 下载一组图片 一个连接下所有图片
def down_group_img(img_down_list, title):
    create_keep_path(title)
    pool = multiprocessing.Pool(processes=pool_num)
    for img_down_link in img_down_list:
        down_path = mzitu_path + title + '\\' + get_image_name(img_down_link)
        pool.apply_async(download, (img_down_link, down_path))
    pool.close()
    pool.join()


# 获取已经下载的连接  has_down.txt -> has_down_list
def get_has_down():
    file = open(has_down_txt, 'r')
    # has_down = [line.strip() for line in file]
    has_down = [line.split('<|>')[0].strip() for line in file]
    return has_down


# 保存已经下载的链接到
def keep_has_down(meizi):
    has_down_txt = open('has_down.txt', 'a')
    has_down_txt.write(meizi.link + '\t' + '<|>' + '\t' + meizi.title + '\n')
    has_down_txt.close()


# 主程序
def start_mzitu():
    print('\nStart')
    has_down_list = get_has_down()
    link = get_all_link(start_url)
    all_meizi = link
    for meizi in all_meizi:
        if meizi.link not in has_down_list:
            print('meizi_index_link  : ' + meizi.link + '\n')
            print('meizi_index_title : ' + meizi.title + '\n')
            try:
                max_num = get_max_num(meizi.link)
                down_link_list = get_down_link_list(meizi.link, max_num)
                down_group_img(down_link_list, meizi.title)
                keep_has_down(meizi)
            except:
                pass
    print('End')


if __name__ == '__main__':
    pass
