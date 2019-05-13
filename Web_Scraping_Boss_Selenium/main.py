# encoding: utf-8


from lxml import etree
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv


class BossSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://www.zhipin.com/'
        self.domain = 'https://www.zhipin.com'
        self.positions = []
        fp = open('boss.csv','a',newline='',encoding='utf-8')
        self.writer = csv.DictWriter(fp,['name','company_name','salary','city','experience','education','job_desc'])
        self.writer.writeheader()


    def run(self):
        self.driver.get(self.url)
        inputTag  = self.driver.find_element_by_class_name('ipt-search')
        inputTag.send_keys('python')
        submitBtn = self.driver.find_element_by_xpath("//button[@class='btn btn-search']")
        submitBtn.click()
        self.driver.implicitly_wait(3)
        citySelect = self.driver.find_element_by_link_text('深圳')
        citySelect.click()
        self.driver.implicitly_wait(3)
        while True:
            source = self.driver.page_source
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath("//a[@ka='page-next']")
            if 'next disabled' in next_btn.get_attribute('class'):
                break
            else:
                next_btn.click()


    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//div[@class='info-primary']/h3/a/@href")
        for base_link in links:
            link = self.domain + base_link
            self.request_detail_page(link)
            time.sleep(1)



    def request_detail_page(self,url):
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to_window(self.driver.window_handles[1])
        WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='name']/h1")
            )
        )
        source = self.driver.page_source
        self.parse_detail_page(source)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])


    def parse_detail_page(self,source):
        html = etree.HTML(source)
        name = html.xpath("//div[@class='name']/h1/text()")[0]
        salary = html.xpath("//span[@class='salary']/text()")[0].strip()
        position_info = html.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/p//text()")
        city = position_info[0]
        experience = position_info[1]
        education = position_info[2]
        company_name = html.xpath("//a[@ka='job-detail-company']/text()")[2].strip()

        # 这个时候的 job_desc 是个带有\n的列表
        job_desc = html.xpath("//div[@class='job-sec']/div[@class='text']/text()")
        # way 1 return list
        # job_desc = list(map(str.strip,job_desc))

        # way 2  return list
        # job_desc = [i.strip() for i in job_desc]

        # way 3 return str
        # 这个时候，是个带有\n的str
        # job_desc = '\n'.join(job_desc)
        job_desc = '\n'.join(job_desc).strip()

        position = {
            'name':name,
            'company_name':company_name,
            'salary':salary,
            'city':city,
            'experience':experience,
            'education':education,
            'job_desc': job_desc,
        }
        self.write_position(position)


    def write_position(self,position):
        self.writer.writerow(position)
        print(position)
        print('='*80)







if __name__ == '__main__':
    spider = BossSpider()
    spider.run()