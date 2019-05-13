# -*- coding: utf-8 -*-
import scrapy
from Web_Scraping_bmw_scrapy.items import WebScrapingBmwScrapyItem

class BmwSpiderSpider(scrapy.Spider):
    name = 'bmw_spider'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
        # print(type(response))
        # return SelectorList
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # way 1

            # for url in urls:
            #     # url = "https:" + url
            #     url = response.urljoin(url)
            #     print(url)


            # way 2
            urls = list(map(lambda url:response.urljoin(url),urls))
            item = WebScrapingBmwScrapyItem(category=category,image_urls=urls)
            yield item