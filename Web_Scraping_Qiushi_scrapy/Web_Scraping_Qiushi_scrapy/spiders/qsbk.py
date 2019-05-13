# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList
from Web_Scraping_Qiushi_scrapy.items import WebScrapingQiushiScrapyItem

class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = 'https://www.qiushibaike.com'

    def parse(self, response):
        # type(response): 返回的是scrapy.http.response.html.HtmlResponse
        # 根据获取回来的信息，我们可以去HtmlResponse里面看看这个response有什么方法属性可以用，发现它具有xpath属性
        # print(type(response))

        duanziDivs = response.xpath("//div[@id='content-left']/div")
        # 发现type(contentLeft)返回来的是scrapy.selector.unified.SelectorList, 所以duanziDivs是一个list
        # deprecated: 抛弃，不赞成

        # duanziDiv 则是selector
        for duanziDiv in duanziDivs:
            # selector的get()会返回
            # Return the result of ``.get()`` for the first element in this list.
            # If the list is empty, return the default value
            author = duanziDiv.xpath(".//h2/text()").get().strip()



            # getall()等于extract,请查看文档，在scrapy.selector.unified.SelectorList的下一层
            # Call the ``.get()`` method for each element is this list and return
            # their results flattened, as a list of unicode strings
            content = duanziDiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = WebScrapingQiushiScrapyItem(author=author,content=content)
            yield item

            next_url = self.base_domain + response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
            if not next_url:
                return
            else:
                yield scrapy.Request(next_url,callback=self.parse)
