#! /usr/bin/env python3
# coding=utf-8

import os
import urllib
import requests
from bs4 import BeautifulSoup
import time
import tablib

headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}


URL = 'http://dwkx.ynau.edu.cn/tealist.aspx'
HEADER = ['学校', '院系', '职称/部门', '姓名', '简介', '邮箱']


def abs_url_path(base_url, rel_path):
    if not rel_path.startswith('http:'):
        return urllib.parse.urljoin(
            base_url, rel_path)
    else:
        return rel_path


class Spider(object):

    def __init__(self, school, department, out_dir):
        self.school = school
        self.department = department
        self.out_file = os.path.join(out_dir, '{s}_{d}.xls'.format(
            s=school, d=department))
        self.url = URL
        self.data = tablib.Dataset(headers=HEADER)

    def get_p_inf(self, soup):
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

    def get_teacher_inf(self, url):
        r = requests.get(url, headers=headers_search)
        time.sleep(20)
        soup = BeautifulSoup(r.content, 'html5lib')
        return self.get_p_inf(soup)

    def get_name_list(self, soup):
        return soup.find_all('a', class_="px14hei")

    def get_name_inf(self, soup):
        teacher_url = abs_url_path(self.url, soup['href'])
        teacher_name = soup.get_text()
        return teacher_url, teacher_name

    def get_name_title(self):
        r = requests.get(self.url, headers=headers_search)
        time.sleep(20)
        soup = BeautifulSoup(r.content, 'html5lib')
        teacher_url_list = self.get_name_list(soup)
        for each_url in teacher_url_list:
            teacher_url, teacher_name = self.get_name_inf(each_url)
            if teacher_url in self.data['简介']:
                continue
            teacher_title, email = self.get_teacher_inf(teacher_url)
            if teacher_name in self.data['姓名']:
                same_name_row = self.data[self.data['姓名'].index(teacher_name)]
                if email == same_name_row[-1]:
                    continue
            self.data.append([self.school, self.department, teacher_title,
                              teacher_name, teacher_url, email])
            print(teacher_name, email)
        with open(self.out_file, 'wb') as f:
            f.write(self.data.xls)


if __name__ == '__main__':
    my_spider = Spider('云南农业大学', '动物科学技术学院', 'ynau_dky.xls')
    my_spider.get_name_title()
