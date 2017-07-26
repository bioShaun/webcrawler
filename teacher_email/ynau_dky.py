#! /usr/bin/env python3
# coding=utf-8

import base_spider
import requests
from bs4 import BeautifulSoup
import time

headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}


URL='http://dwkx.ynau.edu.cn/tealist.aspx'

soup.find_all('table') # all list
test_list.find_all('a', class_="px14hei") # each people

class Spider(base_spider.Spider):

    def __init__(self, school, department, url, out_file):
        super().__init__(school, department, url, out_file)

    def get_name_title(self):
        r = requests.get(self.url, headers=headers_search)
        time.sleep(20)
        soup = BeautifulSoup(r.content, 'html5lib')
