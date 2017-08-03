import base_spider_v2
import time
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://nxy.zafu.edu.cn/l_sz/jsml/yyxxk.htm'


def get_email_list(text):
    pattern = re.compile(
        r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
    email_list = re.findall(pattern, text)
    return email_list


class Spider(base_spider_v2.Spider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_name_list(self, soup):
        names_raw = soup.findAll('a', {'class': 'c131180'})
        names_filter = []
        for each in names_raw:
            if '查看详情' not in each['title']:
                names_filter.append(each)
        return names_filter

    def get_p_inf(self, soup):
        title = ''
        email = ','.join(set(get_email_list(soup.__str__())))
        return title, email
