from pymongo import MongoClient

#获取mongodb客户端
# client = MongoClient('127.0.0.1', 27017)
client = MongoClient() #默认连接本地数据库
# 获取所要操作的数据库
# db = client.get_database('test')
db = client['test'] #数据库名
table = db['user'] #表名
table.insert({'id':'1', 'name': 'cnki'})
# 往数据库集合中添加数据
db.person.save({'id': 5, 'name': 'kaka', 'gender': 'male'})
db.person.save({'id': 1, 'name': 'meixi', 'gender': 'male'})
# 查询数据库集合所有数据
results = db.person.find()
for result in results:
	print(result)

print('--------------------------')
# 查询指定数据   #报错
# results = db.person.find({'id', 1})
# for result in results:
# 	print(result)
# 删除指定数据 #不成功
db.person.remove({'id': 1})
for result in results:
	print(result)

print('------------------------------')
# 查询指定条数的数据
values = db.person.find().limit(4)
for value in values:
	print(value)
print('-------------------------------')
# 分页查询3当前页显示几条数据 2从第几条数据开始
values = db.person.find().limit(3).skip(2)
for value in values:
	print(value)
print('-------------------------------')
# 更新数据 #无反应
db.person.update({'name': 'kaka'}, {'$set': {'name': 'momo'}})
for result in results:
	print(result)
