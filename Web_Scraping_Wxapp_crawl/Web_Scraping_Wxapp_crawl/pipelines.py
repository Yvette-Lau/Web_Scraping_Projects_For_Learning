# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter

class WebScrapingWxappCrawlPipeline(object):
    def __init__(self):
        self.fp = open('wxjc.json','wb')
        self.expoter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')

    def open_spider(self,spider):
        print("Web Scraping is starting...")

    def process_item(self, item, spider):
        self.expoter.export_item(item)
        return item


    def close_spider(self,spider):
        print("Web Scraping is closing....")
        self.fp.close()