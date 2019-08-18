# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json

class PronhubPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def open_spider(self,spider):
        self.file = open('seeds.json', 'w')

    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        # 我需要过滤掉相同的种子
        if item['seed'][0] in self.ids_seen:
            raise DropItem('Duplicate item found : %s'%item)
        else:
            # self.ids_seen.add(item['seed'])
            line=json.dumps(dict(item))+',\n'
            self.file.write(line)
            return item


