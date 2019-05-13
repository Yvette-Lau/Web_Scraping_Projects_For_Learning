# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class WebScrapingJianshuScrapyPipeline(object):
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'etmdZJu58',
            'database':'JianShu_crawl',
            'charset':'utf8',

        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        print("登录成功")
        print("+"*100)
        self._sql = None


    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['content'],item['author'],
                                      item['pub_time'],item['article_id'],
                                      item['origin_url'],item['avatar'],
                                      item['read_count'],item['like_count'],
                                 item['word_count'],item['subjects'],
                                 item['comment_count']))
        self.conn.commit()
        return item



    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            INSERT INTO article (id,title,content,author,pubtime,article_id,origin_url,avatar)
            VALUES (null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql




class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'etmdZJu58',
            'database': 'JianShu_crawl',
            'charset': 'utf8',
            'cursorclass':cursors.DictCursor,

        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        print("="*100)
        print("登录成功")
        self._sql = None



    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                INSERT INTO article (id,title,content,author,pubtime,article_id,origin_url,avatar,
                read_count,like_count,word_count,subjects,comment_count)
                VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # adbapi.ConnectionPool.runInteraction这个方法，参数放入需要执行的参数，就可以
        # 实现异步操作
        defer = self.dbpool.runInteraction(self.insert_item,item)
        # 捕捉错误
        defer.addErrback(self.handle_error, item, spider)



    def insert_item(self,cursor,item):
        cursor.execute(self.sql,(item['title'],item['content'],item['author'],
                                      item['pub_time'],item['article_id'],
                                      item['origin_url'],item['avatar'],
                                 item['read_count'],item['like_count'],
                                 item['word_count'],item['subjects'],
                                 item['comment_count']))


    def handle_error(self,error, item, spider):
        print('=' * 10 + "error" + '=' * 10)
        print(error)
        print('=' * 10 + "error" + '=' * 10)