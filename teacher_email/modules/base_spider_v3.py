#! /usr/bin/env python3
# coding=utf-8

import os
import urllib
import requests
from bs4 import BeautifulSoup
import time
import tablib
import re

headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}


HEADER = ['学校', '院系', '职称/部门', '姓名', '简介', '邮箱']


def abs_url_path(base_url, rel_path):
    if not rel_path.startswith('http:'):
        return urllib.parse.urljoin(
            base_url, rel_path)
    else:
        return rel_path


def get_email_list(text):
    pattern = re.compile(
        r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
    email_list = re.findall(pattern, text)
    return email_list


def get_soup(url):
    r = requests.get(url, headers=headers_search)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup


class Spider(object):

    def __init__(self, school, department, url, title):
        self.school = school
        self.department = department
        self.url = url
        self.title = title
        self.data = tablib.Dataset(headers=HEADER)
        self.public_email = set()

    def get_p_inf(self, soup):
        email_set = set(get_email_list(soup.__str__()))
        p_email_set = email_set.difference(self.public_email)
        email = ','.join(p_email_set)
        return self.title, email

    def get_teacher_inf(self, url):
        r = requests.get(url, headers=headers_search)
        time.sleep(10)
        soup = BeautifulSoup(r.content, 'html5lib')
        return self.get_p_inf(soup)

    def get_name_list(self, soup):
        return 'hh'

    def get_name_inf(self, soup):
        teacher_url = abs_url_path(self.url, soup['href'])
        teacher_name = soup.get_text().strip()
        if 'teacher_title' in soup:
            self.title = soup['teacher_title']
        # print(teacher_url, teacher_name)
        return teacher_url, teacher_name

    @property
    def get_name_title(self):
        r = requests.get(self.url, headers=headers_search)
        time.sleep(60)
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
        # return self.data
        # with open(self.out_file, 'wb') as f:
        #     f.write(self.data.xls)


class DepartmentSpider(object):

    def __init__(self, school, department, url):
        self.school = school
        self.url = url
        self.department = department

    def get_department_url(self):
        return [(self.department, self.url)]


if __name__ == '__main__':
    my_spider = Spider('云南农业大学', '动物科学技术学院', 'ynau_dky.xls')
    my_spider.get_name_title()
