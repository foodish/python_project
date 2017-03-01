from multiprocessing import Pool  # multiprocess
from multiprocessing.dummy import Pool as ThreadPool  # multithread
import time
import urllib.request

urls = [
	'http://www.python.org',
	'http://www.python.org/about/',
	'http://www.python.org/doc/',
	'http://www.python.org/download/',
	'http://www.python.org/getit/',
	'http://www.python.org/psf/',
]

# 单线程
start = time.time()
results = map(urllib.request.urlopen, urls)
print('Normal:', (time.time() - start))

# 多线程
start2 = time.time()
# 设置4个线程，未设置时默认为cpu核心数
pool = ThreadPool()
# 在线程中执行urllib.request.urlopen（url）并返回结果
results2 = pool.map(urllib.request.urlopen, urls)
pool.close()
pool.join()
print('ThreadPool:', (time.time() - start2))
