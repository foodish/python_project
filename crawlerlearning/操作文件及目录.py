import os

#查看当前目录的绝对路径
print(os.path.abspath('.'))
#在某个目录下创建一个新目录，首先把新目录的完整路径表示出来
os.path.join('F:/python/crawlerlearning', 'test')
#然后创建一个目录
# os.mkdir('F:/python/crawlerlearning/test')
#删掉一个目录
os.rmdir("F:/python/crawlerlearning/test")

"""
>>> import os
2 >>> m = os.path.join('路径','文件名.txt')
3 >>> m
4 '路径\\文件名.txt'
5 >>> m.replace('\\','/')
6 '路径/文件名.txt'

m = os.path.join('路径', '文件名.txt')
m
Out[7]: '路径\\文件名.txt'
m=os.path.abspath(m)
m
Out[9]: 'F:\\python\\crawlerlearning\\路径\\文件名.txt'
m.replace('\\','/')
Out[10]: 'F:/python/crawlerlearning/路径/文件名.txt'


"""
