#! /usr/bin/env python
# coding=utf-8

import urllib2
import requests
from bs4 import BeautifulSoup
import os
import time

DOUBAN_URL = 'https://movie.douban.com/'
DOUBAN_DL_REF = 'https://movie.douban.com/photos/photo/'


def get_cookie(cookie_file, name='Cookie'):
    with open(cookie_file) as cookie_file_inf:
        cookie_inf = cookie_file_inf.read().strip()
        return {name: cookie_inf}


headers_search = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/59.0.3071.115 Safari/537.36'}
cookies_search = get_cookie('cookie_search.txt')
headers_download = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                     AppleWebKit/537.36 (KHTML, like Gecko) \
                     Chrome/59.0.3071.115 Safari/537.36'}
cookies_download = get_cookie('cookie_download.txt', 'cookie')


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
        url_num = len(self.wallpaper_url_list)
        for n, url in enumerate(self.wallpaper_url_list):
            print 'collection wallpaper url [{n}/{total}].'.format(
                n=n+1, total=url_num)
            r = requests.get(url, cookies=cookies_search,
                             headers=headers_search)
            time.sleep(30)
            soup = BeautifulSoup(r.content, 'html5lib')
            tags = soup.find_all('a', class_="photo-zoom")
            self.wallpaper_file_list.append(tags[0]['href'])

    def get_movie_name(self):
        movie_site = '{main}/subject/{t.sub_id}'.format(
            main=DOUBAN_URL, t=self
        )
        movie_site_r = requests.get(movie_site)
        movie_site_soup = BeautifulSoup(movie_site_r.content, 'html5lib')
        movie_site_tag = movie_site_soup.find_all('h1')
        movie_name = movie_site_tag[0].span.string
        return movie_name

    def saveImg(self, imageURL):
        each_file_name = os.path.basename(imageURL)
        each_file_path = os.path.join(
            self.out_dir, self.movie_name, each_file_name)
        each_file_name_id = os.path.splitext(each_file_name)[0].lstrip('p')
        reffer = {'referer': '{url}/{p_id}/'.format(
            url=DOUBAN_DL_REF, p_id=each_file_name_id
        )}
        headers_download.update(reffer)
        r = requests.get(imageURL, cookies=cookies_download,
                         headers=headers_download)
        data = r.content
        with open(each_file_path, 'wb') as file_inf:
            file_inf.write(data)
        return 1

    def download_wallpaper(self):
        self.get_wallpaper_url()
        self.get_wallpaper_pic_url()
        self.movie_name = self.get_movie_name()
        if not self.wallpaper_file_list:
            print 'No wallpaper for [{t.movie_name}].'.format(
                t=self
            )
            return 0
        else:
            movie_dir = os.path.join(self.out_dir, self.movie_name)
            try:
                os.makedirs(movie_dir)
            except OSError:
                print '[{t.movie_name}] is downloaded before.'.format(
                    t=self
                )
            else:
                for n, each_file in enumerate(self.wallpaper_file_list):
                    print 'downloading wallpaper [{n}/{total}].'.format(
                        n=n+1, total=len(self.wallpaper_file_list)
                    )
                    self.saveImg(each_file)
                    time.sleep(60)
