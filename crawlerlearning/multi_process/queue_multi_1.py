from multiprocessing import Process, Queue
import os, random, time

#写数据进程执行的代码
def write(q):
	for value in['A', 'B', 'C']:
		print('Process to write: %s' % os.getpid())
		print('Put %s to queue...' % value)
		q.put(value)
		time.sleep(random.random())

#读数据进程执行的代码
def read(q):
	while True:
		print('Process to read: %s' % os.getpid())
		value = q.get(True)
		print('Get %s from queue.' % value)

if __name__ == '__main__':
	#父进程创建queue，并传递给各个子进程
	q = Queue()
	pw = Process(target=write, args=(q,))
	pr = Process(target=read,args=(q,))
	#启动子进程pw，写入
	pw.start()
	#启动子进程pr，读取
	pr.start()
	#等待pw结束
	pw.join()
	#pr进程为死循环，无法等待其结束，只能强行停止
	pr.terminate()