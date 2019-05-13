# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json





# Method 1

# class WebScrapingQiushiScrapyPipeline(object):
#     def __init__(self):
#         self.fp = open('duanzi.json','w',encoding='utf-8')
#
#
#     def open_spider(self,spider):
#         print('Web Scraping is starting...')
#
#
#     def process_item(self, item, spider):
#         item_json = json.dumps(dict(item),ensure_ascii=False)
#         self.fp.write(item_json + '\n')
#         return item
#
#
#
#
#     def close_spider(self,spider):
#         self.fp.close()
#         print('Web Scraping is closing...')

from scrapy.exporters import JsonItemExporter

# Method 2
# 这种方式是相当于把所有的内容先存到内存中，最要finish_exporting的时候再写入列表中。
# 若数据过大，比较好内存，不太合适
# 返回的是一个列表，装了一个字典，字典里面就有全部内容
# class WebScrapingQiushiScrapyPipeline(object):
#     def __init__(self):
#         self.fp = open('duanzi.json','wb')
#         self.exporter = JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#         self.exporter.start_exporting()
#
#
#     def open_spider(self,spider):
#         print('Web Scraping is starting...')
#
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#
#
#
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()
#         self.fp.close()
#         print('Web Scraping is closing...')
#



from scrapy.exporters import JsonLinesItemExporter

class WebScrapingQiushiScrapyPipeline(object):
    def __init__(self):
        self.fp = open('duanzi.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False,
                                         encoding='utf-8')


    def open_spider(self, spider):
        print('Web Scraping is starting...')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        print('Web Scraping is closing...')
