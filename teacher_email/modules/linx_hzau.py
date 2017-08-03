from . import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title):
        super().__init__(school, department, url, title)
        # self.public_email = {'zkbg@mail.hzau.edu.cn'}

    def get_name_list(self, soup):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        name_region = soup.findAll('div', {'class': 'list_table'})
        name_list = []
        for each_region in name_region:
            t_title = each_region.find(
                'div', {'class': "ST1"}).get_text().split()[-1].strip()
            for each_tag in each_region.findAll('a', {'target': "_blank"}):
                each_tag['teacher_title'] = t_title
                name_list.append(each_tag)
        return name_list


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
