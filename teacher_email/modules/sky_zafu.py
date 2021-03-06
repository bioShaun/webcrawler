import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://sky.zafu.edu.cn/teachers/0104/16/list_teachers/'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title, out_file):
        super().__init__(school, department, url, title, out_file)

    def get_name_list(self, soup):
        names_raw = soup.findAll(
            'a', {'href': re.compile('teachers'), 'target': '_blank'})
        return names_raw

    def get_p_inf(self, soup):
        email = ','.join(set(base_spider_v3.get_email_list(soup.__str__())))
        return self.title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL
