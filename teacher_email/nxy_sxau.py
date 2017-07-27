import base_spider_new

URL = ''


class Spider(base_spider_new.Spider):

    def __init__(self, school, department, out_dir):
        super().__init__(school, department, out_dir)
        self.url = URL

    def get_name_list(self, soup):
        name_list_raw = soup.find_all('p', class_='MsoNormal')
        name_list_filter = []
        for each_s in name_list_raw:
            name_list_filter.extend(each_s.find_all('a'))
        return name_list_filter
