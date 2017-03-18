# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class W3School1Pipeline(object):

    def __init__(self):
        self.file = open('w3school.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),  ensure_ascii=False) + '\n'
        print(line)
        self.file.write(line.encode('utf-8'))
        return item
