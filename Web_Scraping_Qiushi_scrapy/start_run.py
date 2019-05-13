# encoding:  utf-8


from scrapy import cmdline

# 返回的是个列表
args = "scrapy crawl qsbk".split()
cmdline.execute(args)