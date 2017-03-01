from multiprocessing import Process
import os

#子进程要执行的代码
def run_process(name):
	print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__ =='__main__':
	print('Parent process %s.' % os.getpid())
	p = Process(target=run_process, args=('test',)) #创建子进程，传入一个执行函数和函数的参数，先创建Process实例
	print('Child process will start')
	p.start() #启动子进程
	p.join() #等待子进程结束后继续往下进行，通常用于进程间同步
	print('Child process end')