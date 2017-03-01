from urllib.request import Request, urlopen
import json
import re
from pymongo import MongoClient
import time
import multiprocessing
import socket

wait_time = 10
socket.setdefaulttimeout(wait_time)
client = MongoClient() #连接至本地数据库
db = client['pythonproject'] #选择一个数据库
xueqiu_users = db['xueqiu'] #在上面的数据库中选择一个集合
xueqiu_users.ensure_index('id', unique=True)
pool_num = multiprocessing.cpu_count() * 3
seed_id = 1955602780

def get_response(url):
	num_retries = 6
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Cookie': 'xq_a_token=280dee5696661da23161c033e7ce7facef8af94d'
	}
	for i in range(num_retries):
		try:
			request = Request(url, headers=headers)
			response = urlopen(request).read().decode('utf-8')
			return response
		except:
			if num_retries > 0:
				num_retries = num_retries - 1

def get_friendscount(id):
	url = 'https://xueqiu.com/' + str(id)
	response = get_response(url)
	pattern = re.compile('SNB\.profileUser\s+[=\s]+({"subscribeable":.*})')
	result = pattern.findall(response)
	r = result[0]
	json_dict = json.loads(r)
	n = json_dict['friends_count']
	return n


def get_userfriends(id):
	friends_num = get_friendscount(id)
	max_page = (friends_num - 1)//20 + 1
	print(friends_num, max_page)
	idlist = []
	for i in range(1, (friends_num//20) + 1):
		print('开始第', i, '页')
		url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, id)
		response = get_response(url)
		data = json.loads(response)
		count = data['count']
		page = data['page']
		maxPage = data['maxPage']
		users = data['users']
		idlist = get_userfriendsinfo(users)
	return idlist


def get_userfriendsinfo(users):
	userInfoList = []
	id_list = []
	for user in users:
		user_id = user['id']
		user_name = user['screen_name']
		friends_count = user['friends_count']
		followers_count = user['followers_count']
		user_city = user['city']
		user_gender = user['gender']
		status_count = user['status_count']
		user_info = {'id': user_id, 'name': user_name, 'gender': user_gender, 'city': user_city,
					 'followNum': friends_count, 'followerNum': followers_count, 'discusNum': status_count}
		xueqiu_users.save(user_info)
		userInfoList.append(user_info)
		id_list.append(user_id)
		time.sleep(1)
		return id_list


if __name__ == '__main__':
	list = get_userfriends(seed_id)
	print(list)
	a = xueqiu_users
	print(a.count())


