from . import base_spider_v3
import time
from bs4 import element
from bs4 import BeautifulSoup
import requests


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, url, title):
        super().__init__(school, department, url, title)

    def get_name_list(self, soup):
        r = requests.get(self.url, headers=base_spider_v3.headers_search)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        name_region = soup.find('div', {'class': 'list_inner'})
        names = name_region.findAll('li')[:-9]
        return [each.a for each in names]

    def get_p_inf(self, soup):
        p_inf = soup.findAll('div', {'align': 'left'})
        email = ''
        for each_inf in p_inf:
            if each_inf.img and each_inf.img['src'] == 'images/at.jpg':
                email_inf = each_inf.contents
                for n, each in enumerate(email_inf):
                    if isinstance(each, element.Tag):
                        email_inf[n] = '@'
                email = ''.join(email_inf)
        return self.title, email


class DepartmentSpider(base_spider_v3.DepartmentSpider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
