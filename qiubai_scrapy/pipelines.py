# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from qiubai_scrapy.items import QiubaiItem
from pymongo import IndexModel, ASCENDING
# 因为涉及到mongodb账户，需要自行创建my_sesttings.py文件，mongodb_url设为数据库地址
from qiubai_scrapy.my_settings import mongodb_url

class QiubaiMongoDBPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(mongodb_url)
        db = client['duanzi']
        self.qiubai = db['qiubai']
        idx = IndexModel([('uuid', ASCENDING)], unique=True)
        self.qiubai.create_indexes([idx])

    def process_item(self, item, spider):
        if isinstance(item, QiubaiItem):
            try:
                self.qiubai.update_one({'uuid': item['uuid']}, {'$set': dict(item)}, upsert=True)
            except Exception as e:
                print(e)

        return item


