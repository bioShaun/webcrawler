#! /usr/bin/env python
# coding=utf-8

import urllib2
import requests
from bs4 import BeautifulSoup
import os


# LOGINURL = 'http://accounts.douban.com/login'
# DOUBAN_LOAD = {
#     "redir": DOUBAN_URL,
#     "form_email": "guilixuan@gmail.com",
#     "form_password": "glx198819",
#     "login": u'登录'
# }
DOUBAN_URL = 'https://movie.douban.com/'
HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1)\
           AppleWebKit/537.36 (KHTML, like Gecko) \
           Chrome/43.0.2357.134 Safari/537.36'}
COOKIE_FILE = 'cookie2.txt'
COOKIE_DICT = {}
with open(COOKIE_FILE) as raw_cookies:
    for eachline in raw_cookies:
        for line in eachline.split(';'):
            key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
            COOKIE_DICT[key.strip()] = value.strip()


def saveImg(imageURL, fileName):
    r = requests.get(imageURL, cookies=COOKIE_DICT, headers=HEADERS)
    data = r.content
    with open(fileName, 'wb') as file_inf:
        file_inf.write(data)
    return 1


class Spider(object):

    def __init__(self, sub_id, out_dir):
        self.sub_id = sub_id
        self.out_dir = out_dir
        self.wallpaper_url_list = []
        self.wallpaper_file_list = []

    def get_wallpaper_url(self):
        wall_parper_url = '{db}subject/{t.sub_id}/photos?type=W'.format(
            db=DOUBAN_URL, t=self
        )
        try:
            wall_parper_html = urllib2.urlopen(wall_parper_url)
        except urllib2.HTTPError, e:
            print e.message
        else:
            soup = BeautifulSoup(wall_parper_html, 'html5lib')
            tags = soup.find_all('div', class_="cover")
            if tags:
                for each_tag in tags:
                    self.wallpaper_url_list.append(each_tag.a['href'])

    def get_wallpaper_pic_url(self):
        for url in self.wallpaper_url_list:
            r = requests.get(url, cookies=COOKIE_DICT, headers=HEADERS)
            soup = BeautifulSoup(r.content, 'html5lib')
            tags = soup.find_all('a', class_="photo-zoom")
            self.wallpaper_file_list.append(tags[0]['href'])

    def download_wallpaper(self):
        self.get_wallpaper_url()
        self.get_wallpaper_pic_url()
        if not self.wallpaper_file_list:
            print 'No wallpaper for this film.'
            return 0
        else:
            for each_file in self.wallpaper_file_list:
                # TODO get movie name
                each_file_name = os.path.basename(each_file)
                each_file_path = os.path.join(self.out_dir, each_file_name)
                saveImg(each_file, each_file_path)
