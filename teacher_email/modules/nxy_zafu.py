import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re


URL = 'http://nxy.zafu.edu.cn/l_sz/jsml.htm'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title, out_file):
        super().__init__(school, department, url, title, out_file)

    def get_name_list(self, soup):
        names_raw = soup.findAll('a', {'class': 'c131180'})
        names_filter = []
        for each in names_raw:
            if '查看详情' not in each['title']:
                names_filter.append(each)
        return names_filter

    def get_p_inf(self, soup):
        email = ','.join(set(base_spider_v3.get_email_list(soup.__str__())))
        return self.title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_department_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        dep_inf = soup.findAll('a', {'href': re.compile("jsml\/")})
        return [(each.get_text(), base_spider_v3.abs_url_path(self.url, each['href']))
                for each in dep_inf]
