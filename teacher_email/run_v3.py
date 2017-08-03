#! /usr/bin/env python3
# coding=utf-8

import click
import os
import tablib


CURRENT_DIR = os.getcwd()
HEADER = ['学校', '院系', '职称/部门', '姓名', '简介', '邮箱']


@click.command()
@click.option('-s', '--school', type=str,
              help='school name.')
@click.option('-d', '--department', type=str,
              help='department name.')
@click.option('-m', '--module_name', type=str, default='nmg_lky',
              help='specific school spider module name.')
@click.option('-o', '--out_dir', type=click.Path(exists=True),
              default=CURRENT_DIR, help='output directory.')
def main(school, department, module_name, out_dir):
    S_spider = __import__(module_name)
    my_dep_inf = S_spider.DepartmentSpider(school, department, out_dir)
    teacher_inf_list = []
    for each_title, each_url in my_dep_inf.get_department_url():
        my_spider = S_spider.Spider(my_dep_inf.school, my_dep_inf.department,
                                    each_url, each_title, my_dep_inf.out_file)
        my_spider.get_name_title
        teacher_inf_list.extend(my_spider.data[:])
    teacher_inf_data = tablib.Dataset(*teacher_inf_list, headers=HEADER)
    out_file = os.path.join(out_dir, '{s}_{d}.xls'.format(
        s=school, d=department))
    with open(out_file, 'wb') as f:
        f.write(teacher_inf_data.xls)


if __name__ == '__main__':
    main()
