# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy.conf import settings
import pymongo

class MongoPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        bookInfo = dict(item)
        self.post.insert(bookInfo)
        return item

class OnionPipeline(object):
    def process_item(self, item, spider):
        return item

class SQLitePipe(object): 

    def open_spider(self,spider):
        #db_name = spider.settings.get('SQLITE_DB_NAME')
        self.con = sqlite3.connect('sqlite.db')
        self.cur = self.con.cursor() 

    def close_spider(self,spider): 
        self.con.commit()
        self.con.close()
    
    def process_item(self, item, spider): 
        self.insert_db(item)
        return item

    def insert_db(self, item):
        #db_table = spider.settings.get('SQLITE_CATEGORY')
        values = (
            item['item_name'],
            item['item_link'],
            item['item_price'],
            item['item_seller'],
            item['item_delivery'],
            item['item_sales'],
            )
        sql = 'INSERT INTO ' + 'hush' + ' (item_name, item_link, item_price, item_seller, item_delivery, item_sales) VALUES(?,?,?,?,?,?)'
        self.cur.execute(sql, values)

