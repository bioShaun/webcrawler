from . import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title):
        super().__init__(school, department, url, title)

    def get_name_list(self, soup):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        name_region = soup.find('td', {'valign': 'top', 'align': 'left'})
        if name_region:
            return name_region.findAll('a')
        else:
            return []


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)

    def get_department_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        dep_inf = soup.find('div', {'id': 'vsb_content_2'}).findAll('a')
        return [(each.get_text().split('：')[0], base_spider_v3.abs_url_path(self.url, each['href']))
                for each in dep_inf][:-2]
