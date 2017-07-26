#! /usr/bin/env python3
# coding=utf-8

import base_spider
import requests
from bs4 import BeautifulSoup
import time


headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}

class Spider(base_spider.Spider):

    def __init__(self, school, department, url, out_file):
        super().__init__(school, department, url, out_file)

    def get_name_title(self):
        r = requests.get(self.url, headers=headers_search)
        time.sleep(20)
        soup = BeautifulSoup(r.content, 'html5lib')
        _title_inf = soup.find_all('b', class_='green14')
        _title_list = [each.string for each in _title_inf]
        _teacher_inf = soup.find_all('ul', class_='cList3')
        for n, each_t in enumerate(_teacher_inf):
            for child in each_t.children:
                if hasattr(child, 'span') and child.span:
                    teacher_url = base_spider.abs_url_path(self.url, child.a['href'])
                    teacher_name = child.string
                    if teacher_url in self.teacher_dict:
                        self.teacher_dict[teacher_url].title.append(
                            _title_list[n])
                    else:
                        self.teacher_dict[teacher_url] = base_spider.Teacher(school=self.school,
                                                                             department=self.department,
                                                                             title=[
                                                                                 _title_list[n]],
                                                                             name=teacher_name,
                                                                             website=[
                                                                                 teacher_url],
                                                                             email='')

    def get_mail(self, url):
        time.sleep(20)
        r = requests.get(url, headers=headers_search)
        soup = BeautifulSoup(r.content, 'html5lib')
        _mail_inf = soup.find_all('a', href=True)
        for each in _mail_inf:
            if 'mailto' in each['href']:
                return each.string
        else:
            _mail_inf = soup.find_all('p', class_='vsbcontent_end')
            if _mail_inf:
                p_mail_str = _mail_inf[0].string
                if isinstance(p_mail_str, str) and '@' in p_mail_str:
                    return p_mail_str.strip()
        return ''
