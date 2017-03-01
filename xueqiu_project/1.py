from pymongo import MongoClient

client = MongoClient() #连接至本地数据库
db = client['pythonproject'] #选择一个数据库
xueqiu_users = db['xueqiu'] #在上面的数据库中选择一个集合
xueqiu_users.ensure_index('id', unique=True)

#查询数据条数
print(xueqiu_users.count())

print(xueqiu_users.find({'followerNum':{'$gt':100000}})) #！输出为<pymongo.cursor.Cursor object at 0x000001828D391C88>
print(xueqiu_users.find().sort('followerNum')) #！输出为<pymongo.cursor.Cursor object at 0x000001828D391C88>

#查询集合中所有数据
# for user in xueqiu_users.find():
# 	print(user)

#查询某一条记录
print(xueqiu_users.find_one({'id':6899676041}))

#随机查询一条结果
print(xueqiu_users.find_one())


print(xueqiu_users.find({'id':6899676041})) #！<pymongo.cursor.Cursor object at 0x0000022DC81CB240>

#查询符合条件的记录
for user in xueqiu_users.find({'id':6899676041}):
	print(user)

#查询符合记录的数据条数
print(xueqiu_users.find({'id':6899676041}).count())

#查询粉丝数大于100000的记录；$gt:大于；$lt:小于
for user in xueqiu_users.find({'followerNum':{'$gt':100000}}):
	print(user)

#查询粉丝数大于100000的记录并按粉丝数从小到大排列；$gt:大于；$gte:大于等于；$lte:小于等于
for user in xueqiu_users.find({'followerNum':{'$gt':100000}}).sort('followerNum'):
	print(user)

print(xueqiu_users.find({'followerNum':{'$gte':100000}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':50000, '$lt':100000}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':10000, '$lt':50000}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':5000, '$lt':10000}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':1000, '$lt':5000}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':500, '$lt':1000}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':100, '$lt':500}}).count())
print(xueqiu_users.find({'followerNum':{'$gte':50, '$lt':100}}).count())
print(xueqiu_users.find({'followerNum':{'$lt':50}}).count())
print(xueqiu_users.find().count())
print(xueqiu_users.find({'followNum':{'$gt':10000}}).count())

# for user in xueqiu_users.find({'followerNum':{'$gte':100000}}):
# 	print(user['id'])
#
# for user in xueqiu_users.find({'followNum':{'$gte':10000}}):
# 	print(user)
#
# for user in xueqiu_users.find({'followNum':0}):
# 	print(user)
#
# for user in xueqiu_users.find({'followNum':1}):
# 	print(user)