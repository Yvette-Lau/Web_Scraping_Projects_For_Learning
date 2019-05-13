# encoding: utf-8

import requests
from bs4 import BeautifulSoup
from pyecharts import Bar


ALL_DATA = []

def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode('utf-8')
    # html5lib 解析器，浏览器的解析器，容错性较强
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div', class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_min_td = tds[-2]
            temp_min = list(temp_min_td.stripped_strings)[0]
            ALL_DATA.append({"city":city, "temp_min":int(temp_min)})
            # print(ALL_DATA)



def main():
    base_url = 'http://www.weather.com.cn/textFC/{}.shtml'
    url_list = ['hb','db','hd','hz','hn','xb','xn','gat']
    for i in url_list:
        url = base_url.format(i)
        parse_page(url)

    ALL_DATA.sort(key=lambda data:data['temp_min'])
    # print(ALL_DATA)
    min_temp_city = ALL_DATA[0:10]
    # pyecharts可视化的库
    chart = Bar("The list of the lowest temperatures in China")
    cities = list(map(lambda x:x['city'],min_temp_city))
    temps = list(map(lambda x:x['temp_min'], min_temp_city))
    chart.add('',cities,temps)
    chart.render('China_min_temperature.html')

if __name__ == '__main__':
    main()