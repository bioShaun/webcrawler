import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://cab.cau.edu.cn/col/col23184/index.html'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title, out_file):
        super().__init__(school, department, url, title, out_file)

    def get_name_list(self, soup):
        names_raw = soup.findAll(
            'a', {'href': re.compile('http://cab.cau.edu.cn')})
        return names_raw

    def get_p_inf(self, soup):
        title = ''
        email = ''
        titles = soup.findAll('li')
        for each in titles:
            if '所在系别' in each.get_text():
                title = each.get_text().split('：')[-1]
            elif '电子邮箱' in each.get_text():
                email = each.get_text().split('：')[-1]
        if not email:
            email = ','.join(
                set(base_spider_v3.get_email_list(soup.__str__())))
        return title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL
