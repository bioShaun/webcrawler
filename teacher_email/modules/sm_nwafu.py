import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re


URL = 'http://sm.nwafu.edu.cn/szdw/gjzc/index.htm'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title, out_file):
        super().__init__(school, department, url, title, out_file)

    def get_name_list(self, soup):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        name_tb_inf = soup.find('table', {'align': 'center'})
        if name_tb_inf:
            return name_tb_inf.findAll(
                'a', {'href': re.compile('sm.nwsuaf.edu.cn')})
        else:
            return []

    def get_p_inf(self, soup):
        email_list = list(set(base_spider_v3.get_email_list(soup.__str__())))
        email = ','.join(email_list)
        return self.title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_department_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        dep_inf = soup.find('div', {'class': 'sort_leftcont'}).findAll('a')
        return [(each.get_text(), base_spider_v3.abs_url_path(self.url, each['href']))
                for each in dep_inf]
