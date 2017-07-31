import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://cast.zafu.edu.cn/sub/0105/7/'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title, out_file):
        super().__init__(school, department, url, title, out_file)

    def get_name_list(self, soup):
        names_raw = soup.findAll('a', {'href': re.compile('cast.zafu')})
        return names_raw

    def get_p_inf(self, soup):
        name_inf = soup.find('h1', {'class': 'title'})
        name = name_inf.get_text().split('>')[-1].strip()
        email = ','.join(set(base_spider_v3.get_email_list(soup.__str__())))
        return name, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL
