#! /usr/bin/env python3
# coding=utf-8

import requests
from bs4 import BeautifulSoup
import urllib
import time

'''
get mail

test = soup.find_all('a', href=True)
for each in test:
    if 'mailto' in each['href']:
        mail = each.string

'''


class Teacher(object):

    def __init__(self, school, department, title, name, website, email):
        self.school = school
        self.department = department
        self.title = title
        self.name = name
        self.website = website
        self.email = email

    def __str__(self):
        return '{t.school}\t{t.title}\t{t.name}\t{t.website}\t{t.email}'.format(t=self)


class Base_module(object):

    def __init__(self, school, department, url):
        self.school = school
        self.department = department
        self.url = url
        self.teacher_dict = dict()

    def get_name_title(self):
        r = requests.get(self.url)
        time.sleep(10)
        soup = BeautifulSoup(r.content, 'html5lib')
        _title_inf = soup.find_all('b', class_='green14')
        _title_list = [each.string for each in _title_inf]
        _teacher_inf = soup.find_all('ul', class_='cList3')
        for n, each_t in enumerate(_teacher_inf):
            for child in each_t.children:
                if hasattr(child, 'span') and child.span:
                    teacher_url = child.a['href']
                    teacher_name = child.string
                    if teacher_url not in self.teacher_dict:
                        if not teacher_url.startswith('http:'):
                            teacher_url = urllib.parse.urljoin(
                                self.url, teacher_url)
                        self.teacher_dict[teacher_url] = Teacher(school=self.school,
                                                                 department=self.department,
                                                                 title=[
                                                                     _title_list[n]],
                                                                 name=teacher_name,
                                                                 website=teacher_url,
                                                                 email='None')
                    else:
                        self.teacher_dict[teacher_url].title.append(
                            _title_list[n])

    @property
    def get_email(self):
        self.get_name_title()
        for each_url in self.teacher_dict:
            time.sleep(10)
            r = requests.get(each_url)
            soup = BeautifulSoup(r.content, 'html5lib')
            _mail_inf = soup.find_all('a', href=True)
            for each in _mail_inf:
                if 'mailto' in each['href']:
                    self.teacher_dict[each_url].email = each.string
                    print(self.teacher_dict[each_url])
                    break
            else:
                _mail_inf = soup.find_all('p', class_='vsbcontent_end')
                if _mail_inf:
                    p_mail_str = _mail_inf[0].string
                    if isinstance(p_mail_str, str) and '@' in p_mail_str:
                        self.teacher_dict[each_url].email = p_mail_str.strip()
                print(self.teacher_dict[each_url])
