import http.cookiejar
import requests
import re
import time
from PIL import Image
import json


headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'
}
filename = 'cookie_1'
# 创建会话，可以吧同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
session = requests.session()
#  建立一个可以保持Cookie的实例对象，利用LWPCookieJar将Cookie保存为本地文件
session.cookies = http.cookiejar.LWPCookieJar(filename)

# 从本地加载已保存的cookie，ignore_discard=True表示cookie将被丢弃也把它保存下来
try:
	session.cookies.load(filename=filename, ignore_discard=True)
except:
	print('Cookie未加载！')

# 获取_xsrf
def get_xsrf():
	response = session.get('https://www.zhihu.com', headers=headers)
	html = response.text
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
	response = session.get(captcha_url, headers=headers)
	# 下载验证码图片
	with open('cptcha.gif', 'wb') as f:
		f.write(response.content)
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
		url =  'http://www.zhihu.com/login/phone_num'
		# post的数据
		data = {
			'_xsrf':get_xsrf(),
			'password':password,
			'remember_me':'true',
			'phone_num':username
		}
	else:
		print('使用邮箱登陆中...')
		url = 'https://www.zhihu.com/login/email'
		# post的数据
		data = {
			'_xsrf': get_xsrf(),
			'password': password,
			'remember_me': 'true',
			'email': username
		}
	# 若不用验证码，直接登录
	try:
		result = session.post(url, data=data, headers=headers)
		# 打印返回的响应，r = 1 表示响应失败，msg是失败的原因
		print((json.loads(result.text))['msg'])
	# 要使用验证码时，post后提交
	except:
		data['captcha'] = get_captcha()
		result = session.post(url, data=data, headers=headers)
		# 打印返回的响应，r = 1 表示响应失败，msg是失败的原因
		print((json.loads(result.text))['msg'])

	# 保存cookie到本地
	session.cookies.save(ignore_discard=True, ignore_expires=True)

if __name__ == '__main__':
	account = input('输入账号：')
	password = input('输入密码：')
	login(account, password)

	# 设置里的简介页面，登陆后才能查看。验证是否登陆成功
	get_url = 'https://www.zhihu.com/settings/profile'
	resp = session.get(get_url, headers=headers, allow_redirects=False)
	print(resp.text)


