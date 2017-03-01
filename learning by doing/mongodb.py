# 参考：http://www.cnblogs.com/hhh5460/p/5838516.html
from pymongo import MongoClient

client = MongoClient('192.168.40.87', 27037)
db_name = 'tset_1'
db = client[db_name]
collention_user = db['user']
"""
save()和insert()
mongodb的save和insert函数都可以向collection里插入数据，区别在于：

一、save函数实际就是根据参数条件,调用了insert或update函数.如果想插入的数据对象存在,insert函数会报错,而save
函数是改变原来的对象;如果想插入的对象不存在,那么它们执行相同的插入操作.这里可以用几个字来概括它们两的区别,
即所谓"有则改之,无则加之".

二、insert可以一次性插入一个列表，而不用遍历，效率高， save则需要遍历列表，一个个插入。
"""
