#! /usr/bin/env python3
# coding=utf-8

import base_spider
import requests
from bs4 import BeautifulSoup
import time
import tablib

headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}


URL = 'http://dwkx.ynau.edu.cn/tealist.aspx'


class Spider(base_spider.Spider):

    def __init__(self, school, department, out_file):
        super().__init__(school, department, out_file)
        self.url = URL
        self.data = tablib.Dataset(headers=base_spider.HEADER)

    def get_teacher_inf(self, url):
        r = requests.get(url, headers=headers_search)
        time.sleep(20)
        soup = BeautifulSoup(r.content, 'html5lib')
        p_inf = soup.find_all('td')

        def treat_strong(record):
            return record.get_text().strip().strip(each_inf.strong.string)

        for each_inf in p_inf:
            if '所在系' in each_inf.get_text():
                title1 = treat_strong(each_inf)
            elif '职务' in each_inf.get_text():
                title2 = treat_strong(each_inf)
            elif '电子邮件' in each_inf.get_text():
                email = treat_strong(each_inf)
        return '{t1}({t2})'.format(t1=title1, t2=title2), email

    def get_name_title(self):
        r = requests.get(self.url, headers=headers_search)
        time.sleep(20)
        soup = BeautifulSoup(r.content, 'html5lib')
        teacher_url_list = soup.find_all('a', class_="px14hei")
        for each_url in teacher_url_list:
            teacher_url = base_spider.abs_url_path(self.url, each_url['href'])
            teacher_name = each_url.get_text()
            teacher_title, email = self.get_teacher_inf(teacher_url)
            self.data.append([self.school, self.department, teacher_title,
                              teacher_name, teacher_url, email])
            print(teacher_name, email)
        with open(self.out_file, 'wb') as f:
            f.write(self.data.xls)


if __name__ == '__main__':
    my_spider = Spider('云南农业大学', '动物科学技术学院', 'ynau_dky.xls')
    my_spider.get_name_title()
