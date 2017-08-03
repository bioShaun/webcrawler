import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re


URL = 'http://nxy.nwafu.edu.cn/szdw/jsyjy/index.htm'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title, out_file):
        super().__init__(school, department, url, title, out_file)

    @property
    def get_name_title(self):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        name_tb_inf = soup.find('table', {'align': 'center'})
        if name_tb_inf:
            name_tb = name_tb_inf.findAll('tr')
            for n, each in enumerate(name_tb):
                if n == 0:
                    continue
                each_inf = each.findAll('td')
                teacher_title = each_inf[1].get_text()
                teacher_name = each_inf[0].get_text()
                try:
                    teacher_url = base_spider_v3.abs_url_path(
                        self.url, each_inf[0].a['href'])
                except:
                    teacher_url = ""
                email = each_inf[2].get_text()
                self.data.append([self.school, self.department, teacher_title,
                                  teacher_name, teacher_url, email])


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
