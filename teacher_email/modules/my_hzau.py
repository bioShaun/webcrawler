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
        name_region = soup.find('div', {'class': 'teacherList'})
        return name_region.findAll('a', {'target': "_blank"})[:-45]


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
