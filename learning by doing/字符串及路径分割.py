"""
split()和os.path.split()
split()：拆分字符串。通过指定分隔符对字符串进行切片，并返回分割后的字符串列表（list）
语法：str.split(str="",num=string.count(str))[n]

参数说明：
str：   表示为分隔符，默认为空格，但是不能为空('')。若字符串中没有分隔符，则把整个字符串作为列表的一个元素
num：表示分割次数。如果存在参数num，则仅分隔成 num+1 个子字符串，并且每一个子字符串可以赋给新的变量
[n]：   表示选取第n个分片

注意：当使用空格作为分隔符时，对于中间为空的项会自动忽略
-----------------------------------------------------------
os.path.split()：按照路径将文件名和路径分割开
语法：os.path.split('PATH')

参数说明：
PATH指一个文件的全路径作为参数：
如果给出的是一个目录和文件名，则输出路径和文件名
如果给出的是一个目录名，则输出路径和为空文件名
"""
u = "www.doiido.com.cn"
print(u.split())
print(u.split('.'))
print(u.split('.', 0))
print(u.split('.', 1))
print(u.split('.', 2))
#分割两次，并取序列为1的项
print(u.split('.', 2)[1])
#分割最多次，跟不加bum参数相同
print(u.split('.', -1))
#分割两次，并把分割后的三个部分保存到三个文件
u1, u2, u3 = u.split('.', 2)
print(u1, u2, u3)

#去掉换行符
c = """say
hello
baby"""
print(c)

print(c.split('\n'))

#分离文件名和路径
import os

print(os.path.split('/dodo/soft/python/'))
print(os.path.split('/dodo/soft/python'))

#example
str = 'hello boy<[www.doiido.com]>byebye'

print(str.split('[')[1].split(']')[0])
print(str.split('[')[1].split(']')[0].split('.'))