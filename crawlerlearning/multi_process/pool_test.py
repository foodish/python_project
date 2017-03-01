from multiprocessing import Lock, Pool
import time

def fun(index):
	print('start process: ', index)
	time.sleep(3)
	print('end process', index)
	return index

if __name__ == '__main__':
	pool = Pool(processes=3)
	for i in range(4):
		result = pool.apply_async(fun, (i,)) ##非阻塞方法，进程可同时进行
		# pool.apply(fun, (i,)) ##阻塞方法，上一进程结束才进行下一个
		print(result.get())

	print('started processes')
	pool.close()
	pool.join()
	print('subprocess done')