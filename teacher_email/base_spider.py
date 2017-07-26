#! /usr/bin/env python3
# coding=utf-8

from collections import OrderedDict
import tablib
import urllib


HEADER = ['学校', '院系', '职称/部门', '姓名', '简介', '邮箱']


def abs_url_path(base_url, rel_path):
    if not rel_path.startswith('http:'):
        return urllib.parse.urljoin(
            base_url, rel_path)
    else:
        return rel_path


class Teacher(object):

    def __init__(self, school, department, title, name, website, email):
        self.school = school
        self.department = department
        self.title = title
        self.name = name
        self.website = website
        self.email = email

    def __str__(self):
        return '{t.school}\t{title}\t{t.name}\t\
        {website}\t{t.email}'.format(
            t=self, title=','.join(self.title), website=self.website[0])

    @property
    def out(self):
        return [self.school, self.department, self.title,
                self.name, self.website, self.email]

    def merge(self, other):
        self.title.extend(other.title)
        self.website.extend(other.website)


class Spider(object):

    def __init__(self, school, department, url, out_file):
        self.school = school
        self.department = department
        self.url = url
        self.out_file = out_file
        self.teacher_dict = OrderedDict()
        self.teacher_email_dict = OrderedDict()

    def get_name_title(self):
        pass

    def get_mail(url):
        pass

    def add_email(self):
        self.get_name_title()
        for each_url in self.teacher_dict:
            email = self.get_mail(each_url)
            name = self.teacher_dict[each_url].name
            self.teacher_dict[each_url].email = email
            if email:
                if email in self.teacher_email_dict and name in self.teacher_email_dict[email]:
                    self.teacher_email_dict[email][name].merge(
                        self.teacher_dict[each_url])
                else:
                    self.teacher_email_dict.setdefault(
                        email, {})[name] = self.teacher_dict[each_url]

    @property
    def output(self):
        self.add_email()
        out_data = tablib.Dataset(headers=HEADER)
        for each_email in self.teacher_email_dict:
            for each_name in self.teacher_email_dict[each_email]:
                out_data.append(
                    self.teacher_email_dict[each_email][each_name].out)

        with open(self.out_file, 'wb') as f:
            f.write(out_data.xls)


def main():
    pass


if __name__ == '__main__':
    main()
