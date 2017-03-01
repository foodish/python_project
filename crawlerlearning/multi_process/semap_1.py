import multiprocessing
import time


def worker(s, i):

	s.acquire()
	print(multiprocessing.current_process().name + 'acquire')
	time.sleep(1)
	print(multiprocessing.current_process().name + 'release\n')
	s.release()

if __name__ == '__main__':
	s = multiprocessing.Semaphore(2)
	for i in range(5):
		p = multiprocessing.Process(target= worker, args=(s, 1*2))
		p.start()
