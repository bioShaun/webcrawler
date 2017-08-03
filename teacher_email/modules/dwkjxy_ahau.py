from . import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title):
        super().__init__(school, department, url, title)

    def get_name_list(self, soup):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        return soup.findAll('a', {'href': re.compile('jsxx.ahau.edu.cn')})

    def get_p_inf(self, soup):
        p_inf = soup.findAll('div', {'align': 'left'})
        email = ''
        for each_inf in p_inf:
            if each_inf.img and each_inf.img['src'] == 'images/at.jpg':
                email = '{n}@{s}'.format(n=each_inf.contents[0],
                                         s=each_inf.contents[-1])
        return self.title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)

    def get_department_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        dep_inf = soup.find(
            'td', {'bgcolor': re.compile('FFFFF')}).findAll('a')
        return [(each.get_text(), base_spider_v3.abs_url_path(self.url, each['href']))
                for each in dep_inf]
