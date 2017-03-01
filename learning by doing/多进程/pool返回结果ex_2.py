import multiprocessing


def task(pid):
	print('pid:', pid)
	result = pid
	return result

def start():
	multiprocessing.freeze_support()  # Windows 平台要加上这句，避免 RuntimeError
	pool = multiprocessing.Pool()
	cpus = multiprocessing.cpu_count()
	results = []

	for i in range(0, cpus):
		result = pool.apply_async(task, args=(i,))
		results.append(result)

	pool.close()
	pool.join()

	for result in results:
		print(result.get())

if __name__ == '__main__':
	start()
"""
为什么不直接在 for 循环中直接 result.get()呢？这是因为pool.apply_async之后的语句都是阻塞执行的，
调用 result.get() 会等待上一个任务执行完之后才会分配下一个任务。事实上，获取返回值的过程最好放在
进程池回收之后进行，避免阻塞后面的语句。
"""
