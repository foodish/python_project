# http://www.secbox.cn/hacker/program/18045.html
import zipfile
from threading import Thread, Lock
import optparse


lock = Lock()


def extractfile(zfile, password):
	try:
		lock.acquire()
		zfile.extractall(pwd=password.encode('utf-8'))
		return password
	except:
		pass
	lock.release()


def main():
	parser = optparse.OptionParser('usage%prog' + '-f<zipfile> -d <dictionary>')
	parser.add_option('-f', dest='zname', type='string', help='specify zip file')
	parser.add_option('-d', dest='dname', type='string', help='specify zip file')
	(options, args) = parser.parse_args()

	if (options.zname == None) | (options.dname == None):
		print(parser.usage)
		exit(0)
	else:
		zname = options.zname
		dname = options.dname
		zfile = zipfile.ZipFile(zname)
		passfile = open(dname)
		for line in passfile.readlines():
			password = line.strip('\n')
			t = Thread(target=extractfile, args=(zfile, password))
			t.start()
			t.join()


if __name__ == '__main__':
	main()

"""
运行方法：
python zip_crack_1.py -f 文件名 -d 字典名
"""