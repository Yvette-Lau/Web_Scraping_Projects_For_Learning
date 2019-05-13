# encoding: utf-8

import requests
from lxml import etree

BASE_URL = 'https://hr.tencent.com/'

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Cookie':'pgv_pvi=3848046592; pgv_si=s5263127552; _ga=GA1.2.1155689560.1549414904; _gcl_au=1.1.157612292.1549414908; PHPSESSID=5u51vimjpuupl6j9cdlrtnd9d1',
    'Host':'hr.tencent.com',
    'Upgrade-Insecure-Requests':'1',
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    # print(response.text)
    text = response.text
    html = etree.HTML(text)
    return html



def parse_detail_job_page(url):
    position = {}
    html = get_html(url)
    title = html.xpath("//td[@id='sharetitle']/text()")[0]
    tds = html.xpath("//tr[@class='c bottomline']/td")
    address = tds[0].xpath(".//text()")[1]
    category = tds[1].xpath(".//text()")[1]
    nums = tds[2].xpath(".//text()")[1]
    more_infos = html.xpath("//ul[@class='squareli']")
    duty = more_infos[0].xpath(".//text()")
    requirement = more_infos[1].xpath(".//text()")
    position['title'] = title
    position['address'] = address
    position['category'] = category
    position['nums'] = nums
    position['duty'] = duty
    position ['requirement'] =requirement
    return position



def get_detail_urls(url):
    html = get_html(url)
    detail_urls = html.xpath("//tr[@class='even' or @class='odd']//a/@href")
    detail_urls = map(lambda url: BASE_URL + url, detail_urls)
    return detail_urls


def spider():
    positions = []
    base_url = 'https://hr.tencent.com/position.php?keywords=python&lid=0&tid=0&start={}#a'
    for i in range (0,8):
            # 然后i就是0，10，20 ...
            i *= 10
            url = base_url.format(i)
            # print(url)
            detail_urls = get_detail_urls(url)
            for detail_url in detail_urls:
                position = parse_detail_job_page(detail_url)
                positions.append(position)
            #print(positions)
    print(positions)


if __name__ == '__main__':
    spider()

