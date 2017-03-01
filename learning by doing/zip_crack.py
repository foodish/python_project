# http://www.secbox.cn/hacker/program/18045.html
import zipfile
from threading import Thread


def extractfile(zfile, password):
	try:
		zfile.extractall(pwd=password.encode('utf-8'))
		print('password:' + password + '\n')
		return password
	except:
		pass


def main():
	zfile = zipfile.ZipFile('evil.zip')
	passfile = open('pwd.txt')
	for line in passfile.readlines():
		password = line.strip('\n')
		t = Thread(target=extractfile, args=(zfile, password))
		t.start()
		t.join()


if __name__ == '__main__':
	main()

