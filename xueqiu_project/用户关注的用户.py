from urllib.request import Request, urlopen
import json
import re
from pymongo import MongoClient
import time
import multiprocessing
import socket

wait_time = 10
socket.setdefaulttimeout(wait_time)
client = MongoClient()  # 连接至本地数据库
db = client['pythonproject']  # 选择一个数据库
xueqiu_users = db['xueqiu']  # 在上面的数据库中选择一个集合
xueqiu_users.ensure_index('id', unique=True)
pool_num = multiprocessing.cpu_count() * 3


def get_response(url):
	num_retries = 6
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Cookie': 'xq_a_token=6959ef57b6e111ae3d70d258bfd0f7e2fc6f656e'
	}
	for i in range(num_retries):
		try:
			request = Request(url, headers=headers)
			response = urlopen(request).read().decode('utf-8')
			return response
		except:
			if num_retries > 0:
				num_retries = num_retries - 1


def get_friendscount(userid):
	url = 'https://xueqiu.com/' + str(userid)
	response = get_response(url)
	pattern = re.compile('SNB\.profileUser\s+[=\s]+({"subscribeable":.*})')
	print(type(response))
	result = pattern.findall(response)
	r = result[0]
	json_dict = json.loads(r)
	n = json_dict['friends_count']
	return n


def get_userfriendsinfo(userid):
	friends_num = get_friendscount(userid)
	max_page = (friends_num - 1) // 20 + 1
	print(userid, friends_num, max_page)
	idlist = []
	for i in range(1, max_page + 1):
		print(i)
		try:
			url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, userid)
			response = get_response(url)
			data = json.loads(response)
			count = data['count']
			page = data['page']
			maxPage = data['maxPage']
			users = data['users']
			if i != max_page:
				for k in range(20):
					try:
						user = users[k]
						user_id = user['id']
						if xueqiu_users.find_one({'id': user_id}):
							pass
						else:
							user_name = user['screen_name']
							friends_count = user['friends_count']
							followers_count = user['followers_count']
							# description = user['description']
							user_province = user['province']
							user_city = user['city']
							user_gender = user['gender']
							# last_status_id = user['last_status_id']
							status_count = user['status_count']
							# verified = user['verified']
							# verified_description = user['verified_description']
							# verified_type = user['verified_type']
							stocks_count = user['stocks_count']
							# profile_image_url = user['profile_image_url']
							# verified_realname = user['verified_realname']
							# cube_count = user['cube_count']
							user_info = {'id': user_id, 'name': user_name, 'gender': user_gender, 'province': user_province,
									 'city': user_city, 'followNum': friends_count, 'followerNum': followers_count,
									 'discusNum': status_count, 'stocksNum': stocks_count}
							xueqiu_users.save(user_info)
							idlist.append(user_id)
					except:
						print(userid, '好友列表的第', i, '页', k, '项出了点小差错', url)
						continue
			else:
				for k in range(friends_num % 20):
					try:
						user = users[k]
						user_id = user['id']
						if xueqiu_users.find_one({'id': user_id}):
							pass
						else:
							user_name = user['screen_name']
							friends_count = user['friends_count']
							followers_count = user['followers_count']
							# description = user['description']
							user_province = user['province']
							user_city = user['city']
							user_gender = user['gender']
							# last_status_id = user['last_status_id']
							status_count = user['status_count']
							# verified = user['verified']
							# verified_description = user['verified_description']
							# verified_type = user['verified_type']
							stocks_count = user['stocks_count']
							# profile_image_url = user['profile_image_url']
							# verified_realname = user['verified_realname']
							# cube_count = user['cube_count']
							user_info = {'id': user_id, 'name': user_name, 'gender': user_gender, 'province': user_province,
									 'city': user_city, 'followNum': friends_count, 'followerNum': followers_count,
									 'discusNum': status_count, 'stocksNum': stocks_count}
							xueqiu_users.save(user_info)
							idlist.append(user_id)
					except:
						print(userid, '好友列表的第', i, '页', k, '项出了点小差错', url)
						continue
		except:
			print(userid, '好友列表的第', i, '页出问题了', url)
			continue
		time.sleep(1)
	return idlist


def dup(id_liat):
	for i in id_list:
		list = get_userfriendsinfo(i)
		for k in list:
			id_list.append(k)
			get_userfriendsinfo(k)
	return id_list


if __name__ == '__main__':
	# seedid = 1955602780 #不明真相的群众，关注较多
	id_list = []
	for user in xueqiu_users.find():
		id_list.append(user['id'])
	for i in id_list:
		list0 = get_userfriendsinfo(i)
		for k in list0:
			id_list.append(k)
			list1 = get_userfriendsinfo(k)
			for j in list1:
				id_list.append(j)
				list2 = get_userfriendsinfo(j)

	print(xueqiu_users.count())
# for user in xueqiu_users.find():
# 	print(user)
# 162页输出完毕后一直报错
# 492页后报错
