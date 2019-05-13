# encoding: utf-8


import requests
from lxml import etree
from urllib import request
import os
# import re
from queue import Queue
import threading


class Producer(threading.Thread):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'cookie': '__cfduid=dae564201b37a42da5d5b50180317597d1551895821; is_human=1; _ga=GA1.2.1879178035.1551895822; _gid=GA1.2.535364149.1551895822; client_width=1440',
    }

    # *args任意的位置参数， **kwargs任意关键字参数
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        # 重写init函数
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue


    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        opener = request.build_opener()
        opener.addheaders=[('user-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36')]
        request.install_opener(opener)
        response = requests.get(url,headers=self.headers)
        # print(response.text)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='flex_grid credits search_results']//a/img")
        for img in imgs:
            if img.get('data-lazy') != None:
                img_url = img.get('data-lazy')
            else:
                img_url = img.get('src')
            alt = img.get('alt')
            alt = alt.replace(', ','_')
            # alt = re.sub(r'[\?？\.。，,!！\*]','',alt)
            # split extention(ext)
            suffix = os.path.splitext(img_url)[1]
            filename = alt + suffix
            # 队列放入元组
            self.img_queue.put((img_url,filename))
            # 某些网站不支持urllib的request,然后使用urlretrieve方法没办法添加头部，所以在上面需要创建一个opener



class Consumer(threading.Thread):
    # *args任意的位置参数， **kwargs任意关键字参数
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        # 重写init函数
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty()  and self.page_queue.empty():
                break
            # 对队列中放入的元组进行解包
            img_url,filename = self.img_queue.get()
            request.urlretrieve(img_url, 'images/' + filename)
            print(filename + 'Down!')



def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1,100):
        base_url = 'https://pixabay.com/images/search/funny/?pagi={}'
        url = base_url.format(x)
        page_queue.put(url)

    for x in range (5):
        t = Producer(page_queue,img_queue)
        t.start()

    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()



if __name__ == '__main__':
    main()