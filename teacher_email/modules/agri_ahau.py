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
        name_tb_inf = soup.find('ul', {'class': 'data-list'})
        if name_tb_inf:
            return name_tb_inf.findAll('a')
        else:
            return []

    def get_p_inf(self, soup):
        email_list = list(set(base_spider_v3.get_email_list(soup.__str__())))
        if '11_ahau@ahau.edu.cn' in email_list:
            email_list.remove('11_ahau@ahau.edu.cn')
        if 'mchx@163.com' in email_list:
            email_list.remove('mchx@163.com')
        email = ','.join(email_list)
        if not email:
            p_inf = soup.findAll('div', {'align': 'left'})
            for each_inf in p_inf:
                if each_inf.img and each_inf.img['src'] == 'images/at.jpg':
                    email = '{n}@{s}'.format(n=each_inf.contents[0],
                                             s=each_inf.contents[-1])
        # print(self.title, email)
        return self.title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)

    def get_department_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        dep_inf = soup.findAll('td', {'class': 'lnav'})
        return [(each.a.get_text(), base_spider_v3.abs_url_path(self.url, each.a['href']))
                for each in dep_inf]
