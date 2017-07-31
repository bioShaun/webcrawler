import base_spider_v3
import time
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://skxy.fafu.edu.cn/1071/list.htm'


class Spider(base_spider_v3.Spider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_name_list(self, soup):
        return soup.findAll('a', {'href': re.compile("http:\/\/skxy.fafu.edu.cn")})

    def get_p_inf(self, soup):
        title = ''
        email = ','.join(set(base_spider_v3.get_email_list(soup.__str__())))
        return title, email




