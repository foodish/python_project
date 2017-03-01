import time
from multiprocessing import Pool


def func(x):
	time.sleep(1)
	return x*x

if __name__ == '__main__':
	list = []
	for i in range(10):
		list.append(i)
	print('start')
	s = time.time()
	for x in list:
		func(x)

	e = time.time()
	print('单进程执行时间：', e - s)

	print('采用多进程示例如下：')
	pool = Pool(8)
	r = pool.map(func, list)
	pool.close()
	pool.join()
	e2 = time.time()
	print('多进程执行时间：', e2 - e)
	print(r)