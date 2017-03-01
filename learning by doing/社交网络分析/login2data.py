import http.cookiejar
from urllib import request, parse,error
import re
import time
from PIL import Image
import json

email_url = 'https://www.zhihu.com/login/email'
phone_url = 'http://www.zhihu.com/login/phone_num'
#  建立一个可以保持Cookie的实例对象，利用LWPCookieJar将Cookie保存为本地文件
filename = 'cookie'
cookie = http.cookiejar.LWPCookieJar(filename)

# 从本地加载已保存的cookie，ignore_discard=True表示cookie将被丢弃也把它保存下来
try:
	cookie.load(filename=filename, ignore_discard=True)
except:
	print('Cookie未加载！')

# 建立一个可以处理cookies的opener
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'
}
opener = request.build_opener(request.HTTPCookieProcessor(cookie)) # 建立一个可以处理cookies的opener
opener.addheaders = [(key, value) for key, value in headers.items()] # 给opener添加headers，addheaders属性接受元组而非字典

# 获取_xsrf
def get_xsrf():
	req = opener.open('https://www.zhihu.com')
	html = req.read().decode('utf-8')
	pattern = re.compile('<input type="hidden" name="_xsrf" value="(.*?)"/>')
	# 返回多个值，取第一个
	_xsrf = re.findall(pattern, html)[0]
	return _xsrf

# 获取验证码
def get_captcha():
	"""
	获取验证码本地显示
	返回你输入的验证码
	"""
	t = str(int(time.time()*1000))
	# 验证码完整网址
	captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
	# 下载验证码图片
	request.urlretrieve(captcha_url, 'captcha.gif')
	# 用Pillow库显示图片，免去手动打开文件夹的麻烦
	im = Image.open('cptcha.gif')
	im.show()
	captcha = input('本次登陆需要输入验证码：')
	return captcha

# 尝试模拟登陆
def login(username, password):
	# 检测到11位数字则是手机登陆
	if re.match('\d{11}$', account):
		print('使用手机登陆中...')
		url = phone_url
		# post的数据
		data = {
			'_xsrf':get_xsrf(),
			'password':password,
			'remember_me':'true',
			'phone_num':username
		}
	else:
		print('使用邮箱登陆中...')
		url = email_url
		# post的数据
		data = {
			'_xsrf': get_xsrf(),
			'password': password,
			'remember_me': 'true',
			'email': username
		}
	# 若不用验证码，直接登录
	try:
		post_data = parse.urlencode(data).encode('utf-8')
		r = opener.open(url, post_data)
		result = r.read().decode('utf-8')
		# 打印返回的响应，r = 1 表示响应失败，msg是失败的原因
		print((json.loads(result))['msg'])
	# 要使用验证码时，post后提交
	except:
		data['captcha'] = get_captcha()
		post_data = parse.urlencode(data).encode('utf-8')
		r = opener.open(url, post_data)
		result = r.read().decode('utf-8')
		# 打印返回的响应，r = 1 表示响应失败，msg是失败的原因
		print((json.loads(result))['msg'])

	# 保存cookie到本地
	cookie.save(ignore_discard=True, ignore_expires=True)

if __name__ == '__main__':
	account = input('输入账号：')
	password = input('输入密码：')
	login(account, password)

	# 设置里的简介页面，登陆后才能查看。验证是否登陆成功
	get_url = 'https://www.zhihu.com/settings/profile'
	try:
		get = opener.open(get_url)
		content = get.read().decode('utf-8')
		print(content)
	except error.HTTPError as e:
		print(e.reason)
	except error.URLError as e:
		print(e.reason)


