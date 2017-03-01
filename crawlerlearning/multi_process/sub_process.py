# -*- coding: utf-8 -*-
import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)

"""
subprocess包主要功能是执行外部的命令和程序。比如说，我需要使用wget下载文件。
我在Python中调用wget程序。从这个意义上来说，subprocess的功能与shell类似。
代码的意思为在Python代码中运行命令nslookup www.python.org，这和命令行直接运行的效果是一样的
直接命令行输入nslookup，可显示本机DNS服务器名和ip地址；
nslookup www.python.org为查询www.python.org这个域名的信息

"""