# encoding:  utf-8

# 正则表达式   .不能匹配\n
import re
import requests

def parse_page(url):
    headers = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    response = requests.get(url,headers=headers)
    text = response.text
    # 正则表达式注释
    # <div\sclass="cont">  表示得到名为cont这个div下的内容，\s表示空格
    # <b>(.*?)</b> 表示所有b标签下的内容，（）可以进行过滤，找出只满足条件的分组
    # ？进行非贪婪模式
    # re.DOTALL 由于.不能匹配\n， 所以让其匹配所有
    titles = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text, re.DOTALL)
    dynasties = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    content_tags = re.findall(r'<div\sclass="contson".*?>(.*?)</div>', text, re.DOTALL)
    contents = []
    for content_tag in content_tags:
        x = re.sub(r'<.*?>', '', content_tag)
        contents.append(x.strip())

    poems = []
    for value in zip(titles,dynasties,authors,contents):
        title,dynasty,author,content = value
        poem = {
            'title':title,
            'dynasty':dynasty,
            'author':author,
            'content':content
        }
        poems.append(poem)

    for poem in poems:
        print(poem)
        print("*"*30)

def main():
    base_url = 'https://www.gushiwen.org/default_{}.aspx'
    for i in range(1,8):
        url = base_url.format(i)
        parse_page(url)


if __name__ == '__main__':
    main()