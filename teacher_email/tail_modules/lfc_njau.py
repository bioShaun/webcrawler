from . import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title):
        super().__init__(school, department, url, title)
        # self.public_email = {'zkbg@mail.hzau.edu.cn'}

    def get_name_list(self, soup):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        name_region = soup.find('div', {'class': 'view-content'})
        return name_region.findAll('a', {'class': re.compile('colorbox-node')})


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)

    def get_department_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        dep_inf = soup.find('nav', {'id': 'scrollspynav'}).findAll('a')[1:]
        return [(each.get_text(), base_spider_v3.abs_url_path(self.url, each['href']))
                for each in dep_inf]
