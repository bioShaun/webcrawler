#coding=utf-8

import re
import urllib
import sys
from operator import itemgetter

reload(sys)
sys.setdefaultencoding('utf8')


def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def get_onplaying_inf(html):
    html_list = html.split('\n')
    onplaying_list = []
    for eachline in html_list:
        eachline = eachline.strip()
        if eachline[0:10] == 'data-title':
            each_file_list = []
            name = re.search(r'data-title="(.*?)"', eachline).groups()[0]
            each_file_list.append(name)
        if eachline[0:10] == 'data-score':
            score = re.search(r'data-score="(.*?)"', eachline).groups()[0]
            each_file_list.append(float(score))
        if eachline[0:14] == 'data-votecount':
            votecount = re.search(r'data-votecount="(\w+)"', eachline).groups()[0]
            each_file_list.append(int(votecount))
            onplaying_list.append(each_file_list)
    return onplaying_list

def output_onplaying_inf(onplaying_list):
    ## print best rate
    best_rate = sorted(onplaying_list, key = itemgetter(1), reverse = True)
    print "正在上映评论最好10部"
    print "名称\t评分\t评论条数"
    for each in best_rate[0:10]:
        print '{0}\t{1}\t{2}'.format(each[0], each[1], each[2])
    print '\n====================\n'
    ## print most vote
    print "正在上映评论最多10部"
    print "名称\t评分\t评论条数"
    most_vote = sorted(onplaying_list, key = itemgetter(2), reverse = True)
    for each in most_vote[0:10]:
        print '{0}\t{1}\t{2}'.format(each[0], each[1], each[2])
    

my_html = get_html("https://movie.douban.com/nowplaying/chengdu/")

onplaying_list = get_onplaying_inf(my_html)

output_onplaying_inf(onplaying_list)
