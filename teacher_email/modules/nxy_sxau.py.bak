import base_spider_v2

URL = 'http://nxy.sxau.edu.cn/info/1238/1699.htm'


class Spider(base_spider_v2.Spider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_name_list(self, soup):
        name_list_raw = soup.find_all('p', class_='MsoNormal')
        name_list_filter = []
        for each_s in name_list_raw:
            name_list_filter.extend(each_s.find_all('a'))
        return name_list_filter

    def get_p_inf(self, soup):
        p_inf1 = soup.find_all('span', class_='fontstyle40217')
        try:
            title = p_inf1[-2].get_text()
        except IndexError:
            title = ''
        email = ''
        p_inf = soup.find_all('p', class_="MsoNormal")
        try:
            for n, each_inf in enumerate(p_inf):
                if '学\u3000\u3000科' in each_inf.get_text():
                    title = p_inf[n+1].get_text()
                    continue
                if '电子邮件:' in each_inf.get_text():
                    email = p_inf[n+1].get_text()
        except:
            email = ','.join(set(base_spider_v2.get_email_list(soup.__str__())))
        return title, email
