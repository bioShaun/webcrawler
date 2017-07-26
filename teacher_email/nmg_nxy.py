#! /usr/bin/env python3
# coding=utf-8

import base_spider
import requests
from bs4 import BeautifulSoup
import urllib
import time

headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}


URL = 'http://nxy.imau.edu.cn/szxx.htm'


class Spider(base_spider.Spider):

    def __init__(self, school, department, url, out_file):
        super().__init__(school, department, url, out_file)
        self.url = URL

    def get_name_title(self):
        r = requests.get(self.url, headers=headers_search)
        self.get_one_page(r.content)
        time.sleep(60)
        soup = BeautifulSoup(r.content, 'html5lib')
        next_url = soup.find_all('a', class_='Next')
        if next_url:
            self.url = base_spider.abs_url_path(self.url, next_url[0]['href'])
            return self.get_name_title()
        return self.url

    def get_one_page(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        name_inf = soup.find_all('a', target='_blank')
        for each in name_inf:
            if each.img:
                teacher_url = each['href']
                teacher_name = each.get_text()
                if not teacher_url.startswith('http:'):
                    teacher_url = urllib.parse.urljoin(
                        self.url, teacher_url)
                self.teacher_dict[teacher_url] = base_spider.Teacher(school=self.school,
                                                                     department=self.department,
                                                                     title=[
                                                                         '--'],
                                                                     name=teacher_name,
                                                                     website=[
                                                                         teacher_url],
                                                                     email='')

    def get_mail(self, url):
        r = requests.get(url, headers=headers_search)
        time.sleep(60)
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
