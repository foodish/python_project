from urllib.request import Request, urlopen
import re
import json

url = 'https://xueqiu.com/simon'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Cookie':'xq_a_token=ce97c94e1b31d1d7d671082fddfb70064a596325'
}
request = Request(url, headers=headers)
response = urlopen(request)
r = response.read().decode('utf-8')
pattern = re.compile('<script>SNB.profileUser = (.*?)</script>', re.S)
userinfo_list = re.findall(pattern, r)
userinfo = userinfo_list[0]
json_dict = json.loads(userinfo)

user_id = json_dict['id']
user_name = json_dict['screen_name']
friends_count = json_dict['friends_count']
followers_count = json_dict['followers_count']
description = json_dict['description']
province = json_dict['province']
city = json_dict['city']
gender = json_dict['gender']
last_status_id = json_dict['last_status_id']
status_count = json_dict['status_count']
verified = json_dict['verified']
verified_description = json_dict['verified_description']
verified_type = json_dict['verified_type']
stocks_count = json_dict['stocks_count']
profile_image_url = json_dict['profile_image_url']
verified_realname = json_dict['verified_realname']
cube_count = json_dict['cube_count']

print('用户名：', user_name)
print('用户id：', user_id)
print('用户性别：', gender)
print('用户个人简介：', description)
print('用户地区：', province, city)
print('用户认证信息：', verified_description)
print('用户关注人数：', friends_count)
print('用户粉丝数：', followers_count)
print('用户关注股票数：', stocks_count)
print('用户组合数：', cube_count)
print('用户主贴数：', status_count)
