# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Web_Scraping_JianShu_scrapy.items import ArticleItem

class JianshuSpiderSpider(CrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        # the Rule, why there is *, not +, coz if you go the the jianshu one of detailed page link,
        # in the bottom, inspect other article, you will find the tag a,
        # the link, there is no wwww.jianshu.com
        # it start with /p/.....
        # so it can use *, means can have or no
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        avatar = response.xpath("//a[@class='avatar']/img/@src").get()
        author = response.xpath("//span[@class='name']/a/text()").get()
        pub_time = response.xpath("//span[@class='publish-time']/text()").get().replace("*","")

        # https://www.jianshu.com/p/cf3f6006edbe?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
        # https://www.jianshu.com/p/17c104560971

        # we need to get article_id, there has only two kind of url, and we can get id from the url
        article_id = response.url.split("?")[0].split("/")[-1]
        origin_url = response.url

        content = response.xpath("//div[@class='show-content']").get()
        word_count = response.xpath("//span[@class='wordage']/text()").get()
        comment_count = response.xpath("//span[@class='comments-count']/text()").get()
        like_count = response.xpath("//span[@class='likes-count']/text()").get()
        read_count = response.xpath("//span[@class='views-count']/text()").get()

        subjects = response.xpath("//div[@class='include-collection']/a/div/text()").getall()
        subjects = ",".join(subjects)


        item = ArticleItem(
            title=title,
            avatar=avatar,
            author=author,
            pub_time=pub_time,
            article_id=article_id,
            origin_url=origin_url,
            content=content,
            subjects=subjects,
            word_count=word_count,
            comment_count=comment_count,
            like_count=like_count,
            read_count=read_count,

        )
        print(item)

        yield item