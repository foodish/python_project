from multiprocessing import Process, Queue, Lock, Semaphore
import time
from random import random

"""
该程序只能运行两行，可能是因将Semaphore定义为全局变量
"""

buffer = Queue(10)
empty = Semaphore(2)
full = Semaphore(0)
lock = Lock()

class Consumer(Process):

	def run(self):
		global buffer, empty, full, lock
		while True:
			full.acquire()
			lock.acquire()
			print('Consumer pop an element', buffer.get())
			time.sleep(1)
			lock.release()
			empty.release()

class Producer(Process):
	def run(self):
		global buffer, empty, full, lock
		while True:
			empty.acquire()
			lock.acquire()
			num = random()
			print('Producer append', num)
			buffer.put(num)
			time.sleep(1)
			lock.release()
			full.release()

if __name__ == '__main__':
	p = Producer()
	c = Consumer()
	p.daemon = c.daemon = True
	p.start()
	c.start()
	p.join()
	c.join()
	print('Ended')