# 原址：https://github.com/guofh/XueqiuSpider/blob/master/user_spider.py
# coding=utf-8
import sys
import pymongo
import requests
import redis
from lxml import etree
import json

'''
爬虫核心逻辑
'''


class Spider():
	def __init__(self, userId):

		self.userId = userId
		self.url = "http://xueqiu.com/friendships/groups/members.json?page=1&uid=" + str(userId) + "&gid=0"
		self.header = {}

		# cookie要自己从浏览器获取
		self.header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
		self.cookies = {"xq_a_token": "ce97c94e1b31d1d7d671082fddfb70064a596325"}

	# 获得当前用户的所有关注用户信息，返回list
	def get_user_data(self):
		userInfoList = []
		followee_url = self.url
		try:
			get_html = requests.get(followee_url, cookies=self.cookies, headers=self.header, verify=False, timeout=10)
		except:
			print("requests get error!url=" + followee_url)
			return userInfoList

		if get_html.status_code == 200:

			content = json.loads(get_html.text)
			count = content['count']
			page = content['page']
			maxPage = content['maxPage']
			userContent = content['users']

			curList = self.analy_profile(userContent)
			userInfoList.extend(curList)

			page = page + 1
			while page <= maxPage:
				curUrl = "http://xueqiu.com/friendships/groups/members.json?page=" + str(page) + "&uid=" + self.userId + "&gid=0"
				# print curUrl
				try:
					curHtml = requests.get(curUrl, cookies=self.cookies, headers=self.header, verify=False, timeout=10)
					if curHtml.status_code == 200:
						curContent = json.loads(curHtml.text)
						curUserContent = curContent['users']
						curList = self.analy_profile(curUserContent)
						userInfoList.extend(curList)
					else:
						print('[ERROR]curHtml.status_code error !!!')
				except:
					print("requests get error!url=" + curUrl)

				page = page + 1


		else:
			print('[ERROR]get_html.status_code error !!!')

		return userInfoList

	# 解析每一页的关注用户，json格式
	def analy_profile(self, userContent):

		userInfoList = []

		for curUser in userContent:
			user_id = curUser['id']
			user_name = curUser['screen_name']
			user_gender = curUser['gender']
			user_city = curUser['province']
			user_followerNum = curUser['followers_count']
			user_disNum = curUser['status_count']
			user_followNum = curUser['friends_count']

			userInfo = {'id': user_id, 'name': user_name, 'gender': user_gender, 'city': user_city,
						'followNum': user_followNum, 'followerNum': user_followerNum, 'discusNum': user_disNum}

			global red

			if red.sadd('red_had_spider', user_id):
				red.lpush('red_to_spider', user_id)
				userInfoList.append(userInfo)
			# print 'insert id = '+str(user_id)+' name = '+user_name

		return userInfoList


# 核心模块,bfs宽度优先搜索
def BFS_Search():
	global red
	global post_info
	userInfoList = []

	while True:
		tempUser = red.rpop('red_to_spider') #Redis Rpop 命令用于移除并返回列表的最后一个元素

		if tempUser == None:
			print('empty')
			break

		result = Spider(tempUser)
		curList = result.get_user_data()
		userInfoList.extend(curList)
		print('userId : ' + tempUser + ',cur list data number: ' + str(len(curList)) + ',total data number : ' + str(len(userInfoList)))

		# 每一千个数据向mongodb中插入，减少io次数。
		if len(userInfoList) > 1000:
			print('insert to mongodb,data number = ' + str(len(userInfoList)))
			post_info.insert_many(userInfoList)
			userInfoList = []

	return "ok"


# 连接redis，如果redis中没有数据，插入一个种子用户（不明真相的群众）
red = redis.Redis(host='localhost', port=6379, db=1)
seedUser = "1955602780"
if red.sadd('red_had_spider', seedUser):
	red.lpush('red_to_spider', seedUser)

# 连接mongodb数据库
connection = pymongo.MongoClient()
tdb = connection.Xueqiu
post_info = tdb.userInfo

# 执行爬虫
BFS_Search()
