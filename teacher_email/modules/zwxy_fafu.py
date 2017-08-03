import base_spider_v2
import time
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://zwxy.fafu.edu.cn/1150/list.htm'


def get_email_list(text):
    pattern = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
    email_list = re.findall(pattern, text)
    return email_list


class Spider(base_spider_v2.Spider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_name_list(self, soup):
        title_inf_raw = soup.find_all('td', align='left')
        title_inf_filter = [each.a for each in title_inf_raw if each.a]
        name_list = []
        for each_t in title_inf_filter:
            each_t_url = base_spider_v2.abs_url_path(self.url, each_t['href'])
            r = requests.get(each_t_url, headers=base_spider_v2.headers_search)
            time.sleep(60)
            soup = BeautifulSoup(r.content, 'html5lib')
            each_name_inf = soup.find('div', class_='Article_Content')
            each_name_list = each_name_inf.find_all('a', target='_blank')
            for each_name in each_name_list:
                each_name['rs'] = each_t.get_text()
            name_list.extend(each_name_list)
        return name_list

    def get_name_inf(self, soup):
        teacher_url = base_spider_v2.abs_url_path(self.url, soup['href'])
        teacher_name = '{r}|{n}'.format(r=soup['rs'], n=soup.get_text())
        return teacher_url, teacher_name

    def get_p_inf(self, soup):
        title = ''
        email = ','.join(set(get_email_list(soup.__str__())))
        return title, email
