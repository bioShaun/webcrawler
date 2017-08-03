import base_spider_v2

URL = 'http://lxy.fafu.edu.cn/1521/list.htm'


class Spider(base_spider_v2.Spider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_name_list(self, soup):
        title_inf_raw = soup.find_all('td', align='left')
        title_inf_filter = [each.a for each in title_inf_raw if each.a]
        return title_inf_filter

    def get_p_inf(self, soup):
        title = ''
        email = ','.join(set(base_spider_v2.get_email_list(soup.__str__())))
        return title, email
