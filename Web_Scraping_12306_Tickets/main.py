# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TicketsGrabbing(object):

    def __init__(self):
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initmy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.search_tickets_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.passengers_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

        self.driver = webdriver.Chrome()

    def wait_input(self):
        self.from_station = input('起始站:')
        self.to_station = input('目的地:')
        # 出发时间的输入格式必须满足:   YYYY-MM-dd的方式
        self.depart_time = input('出发时间:')
        self.passengers = input("乘客姓名(如有多个乘客,用英文逗号隔开):").split(',')
        self.trains = input("车次(如有多个车次，用英文逗号隔开):").split(',')


    #   _login()有一个_下划线代表这个方法仅可以在类里面被调用，不希望被外面调用

    def _login(self):
        self.driver.get(self.login_url)
        # 隐示等待，implicity,不管有没有等待到想要的页面，都会等待到指定的时间结束
        # 显示等待，
        WebDriverWait(driver=self.driver,timeout=10000).until(
            # url_to_be function 可以判断指定的url是否是你想要的url
            EC.url_to_be(self.initmy_url)
        )
        print('登陆成功!')


    def _order_ticket(self):
        # 1. 跳转到查余票的界面
        self.driver.get(self.search_tickets_url)

        # 2. 等待在控制台和浏览器输入的出发地等信息是否比对正确
        WebDriverWait(driver=self.driver,timeout=10000).until(
            EC.text_to_be_present_in_element_value(
                (By.ID,"fromStationText"),self.from_station
            )
        )

        WebDriverWait(driver=self.driver, timeout=10000).until(
            EC.text_to_be_present_in_element_value(
                (By.ID, "toStationText"), self.to_station
            )
        )

        WebDriverWait(driver=self.driver, timeout=10000).until(
            EC.text_to_be_present_in_element_value(
                (By.ID, "train_date"), self.depart_time
            )
        )


        # 3. 等待查询按钮是否可以被点击
        WebDriverWait(driver=self.driver,timeout=10000).until(
            EC.element_to_be_clickable(
                (By.ID, "query_ticket")
            )
        )

        # 4. 如果能够被点击,那么就找到这个查询按钮,执行点击事件
        searchBtn = self.driver.find_element_by_id('query_ticket')
        searchBtn.click()


        # 5. 在点击了查询按钮以后,等待车次信息是否显示出来了
        WebDriverWait(driver=self.driver,timeout=10000).until(
            EC.presence_of_element_located(
                (By.XPATH,".//tbody[@id='queryLeftTable']/tr")
            )
        )

        # 6. 找到所有没有datatrain属性的tr标签,这些是存储了车次信息的
        tr_list = self.driver.find_element_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")


        # 7. 遍历所有满足条件的tr标签
        for tr in tr_list:
            train_number = tr.find_element_by_class_name("number").text
            if train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[4]").text
                if left_ticket == '有' or left_ticket.isdigit:
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()

                    # 等待是否来到了确认乘客的页面
                    WebDriverWait(self.driver,10000).until(
                        EC.url_to_be(self.passengers_url)
                    )





    # 如果要调用就调用run方法，这样可以保证_下划线的函数保持不被调用，保持类的封装性
    def run(self):
        self.wait_input()
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = TicketsGrabbing()
    spider.run()