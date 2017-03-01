from multiprocessing import Pool
import time


def func(m):
	print('m:', m)
	time.sleep(3)
	print('end')
	return 'done' + m

if __name__ == '__main__':
	pool = Pool(processes=12)
	result = []
	for i in range(3):
		m = 'hello %d' % (i)
		result.append(pool.apply_async(func, (m, )))
	pool.close()
	pool.join()
	for r in result:
		print(r.get())
	print('subprocess done')
	time.sleep(3)


