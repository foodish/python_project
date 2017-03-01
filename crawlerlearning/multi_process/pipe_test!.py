from multiprocessing import Process, Pipe

"""程序未输出任何结果"""

class Consumer(Process):
	def __init__(self, pipe):
		Process.__init__(self)
		self.pipe = pipe

	def run(self):
		self.pipe.send('Consumer Words')
		print('Consumer Receiived:', self.pipe.recv())

class Producer(Process):
	def __init__(self, pipe):
		Process.__init__(self)
		self.pipe = pipe

		def run(self):
			print('Producer Receiived:', self.pipe.recv())
			self.pipe.send('Producer Words')

if __name__ == '__main__':
	pipe = Pipe()
	p = Producer(pipe[0])
	c = Consumer(pipe[1])
	p.daemin = c.daemon = True
	p.start()
	c.start()
	p.join()
	c.join()
	print('Ended')
