# encoding : utf-8

import requests
from lxml import etree


BASE_DOMAIN = 'https://www.dytt8.net'

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

def get_detail_urls(url):
    response = requests.get(url, headers=HEADERS)
    # print(response.content.decode('gbk'))
    # text = response.content.decode('gbk')
    text = response.text
    # response.text
    # response.content
    # requests库, 默认会使用自己猜测的编码方式将
    # 抓取下来的网页进行解码，然后存储到text属性上去,
    # 在这里如果用response.text会出现乱码，是因为requests库猜错编码方式，所以产生乱码
    # 可以查看网页源代码知道该编码方式

    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    # for detial_url in detail_urls:
    #     print(BASE_DOMAIN + detial_url)

    detail_urls = map(lambda url:BASE_DOMAIN + url, detail_urls)
    # detail_urls是个列表，map返回的是个列表
    return detail_urls


def parse_detail_page(url):
    movie = {}
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath(".//font[@color='#07519a']/text()")[0]
    movie['title'] = title
    zoomE = html.xpath("//div[@id='Zoom']")[0]
    imgs = zoomE.xpath(".//img/@src")
    cover = imgs[0]
    movie['cover'] = cover
    screenshot = imgs[1]
    infos = zoomE.xpath(".//text()")

    def parse_info(info, rule):
        return info.replace(rule, "").strip()

    for index, info in enumerate(infos):
        if info.startswith("◎年　　代"):
            info = parse_info(info, "◎年　　代")
            movie["year"] = info
        elif info.startswith("◎产　　地"):
            info = parse_info(info, "◎产　　地")
            movie["country"] = info
        elif info.startswith("◎类　　别"):
            info = parse_info(info, "◎类　　别")
            movie["category"] = info
        elif info.startswith("◎IMDb评分"):
            info = parse_info(info, "◎IMDb评分")
            movie["IMBd_Score"] = info
        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info, "◎豆瓣评分")
            movie["doban_Score"] = info
        elif info.startswith("◎语　　言"):
            info = parse_info(info, "◎语　　言")
            movie["lanuage"] = info
        elif info.startswith("◎字　　幕"):
            info = parse_info(info, "◎字　　幕")
            movie["subtitile"] = info
        elif info.startswith("◎片　　长"):
            info = parse_info(info, "◎片　　长")
            movie["duration"] = info
        elif info.startswith("◎导　　演"):
            info = parse_info(info, "◎导　　演")
            movie["director"] = info
        elif info.startswith("◎主　　演"):
            info = parse_info(info, "◎主　　演")
            actors = [info]
            for x in range(index+1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            #print(actors)
            movie["actors"] = actors
        elif info.startswith("◎简　　介"):
            info = parse_info(info, "◎简　　介")
            for x in range (index+1, len(infos)):
                abstract = infos[x].strip()
                if abstract.startswith("◎"):
                    break
                #print(abstract)
                movie['abstract'] = abstract

    movie["screenshot"] = screenshot
    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie['download_url'] = download_url
    return movie



def spider():
    movies = []
    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for i in range (1,8):
        # 第一个for循环, 是用来控制总共有7页的
        # print("=" * 30)
        # print(i)
        # print("=" * 30)
        url = base_url.format(i)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            # 第二个for循环，是用来遍历一页中所有电影详情的url
            #print(detail_url)
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            #print(movies)
    print(movies)


if __name__ == '__main__':
    spider()