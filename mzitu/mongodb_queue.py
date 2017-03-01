import datetime
from pymongo import MongoClient, errors

class MogoQueue():

    OUTSTANDING = 1
    PROCESSING = 2
    COMPLETE = 3

    def __init__(self, db, collection, timeout=30):
        self.client = MongoClient()
        self.Client = self.client[db]
        self.db = self.Client[collection]
        self.timeout = timeout

    def __bool__(self):
        # $ne的意思是不匹配
        record = self.db.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url, title):
        try:
            self.db.insert({'_id':url, 'status':self.OUTSTANDING, '主题':title})
            print(url, '插入队列成功')
        except errors.DuplicateKeyError as e:
            print(url, '已经存在')
            pass

    def push_imgurl(self, title, url):
        try:
            self.db.insert({'_id': title, 'status': self.OUTSTANDING, 'url': url})
            print('图片插入成功')
        except errors.DuplicateKeyError as e:
            print('地址已经存在')
            pass

    def pop(self):
        """
        $set是设置的意思，和MySQL的set语法一个意思
        """
        record = self.db.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        record = self.db.find_one({'_id': url})
        return record['主题']

    def peek(self):
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        record = self.db.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.datetime.now() - datetime.timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('重置url状态', record['_id'])

    def clear(self):
        """这个函数只有第一次采用、后续不要调用、因为这是删库"""
        self.db.drop()