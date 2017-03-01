# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CsdnblogPipeline(object):

    def __init__(self):
        self.file = open('csdnblog.json', 'wb')

    def process_item(self, item, spider):
        print(item)
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'  #避免输出中文乱码：ensure_ascii=False
        self.file.write(line.encode('utf-8'))
        return item


