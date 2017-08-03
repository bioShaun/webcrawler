#! /usr/bin/env python3
# coding=utf-8

import click
import os
import tablib
import pandas as pd


CURRENT_DIR = os.getcwd()
STATUS_INI = os.path.join(CURRENT_DIR, 'url.csv')
HEADER = ['学校', '院系', '职称/部门', '姓名', '简介', '邮箱']
SCRIPT_DIR, script_name = os.path.split(os.path.abspath(__file__))


def get_module(url):
    url = url.strip('http://')
    module_pfx = '_'.join(url.split('.')[:2])
    module_path = os.path.join(SCRIPT_DIR, 'modules',
                               '{s}.py'.format(s=module_pfx))
    return module_pfx, module_path


@click.command()
@click.option('-o', '--out_dir', type=click.Path(exists=True),
              default=CURRENT_DIR, help='output directory.')
def main(out_dir):
    status_df = pd.read_csv(STATUS_INI, header=None)
    for each_index in status_df.index:
        school, department, url, status, _ = status_df.loc[each_index, :]
        module_pfx, module_path = get_module(url)
        if status == 'todo' and os.path.exists(module_path):
            print('Scraping {s} {d}.'.format(s=school, d=department))
            S_module = __import__('modules', fromlist=[module_pfx])
            S_spider = getattr(S_module, module_pfx)
            my_dep_inf = S_spider.DepartmentSpider(
                school, department, url)
            teacher_inf_list = []
            for each_title, each_url in my_dep_inf.get_department_url():
                my_spider = S_spider.Spider(my_dep_inf.school,
                                            my_dep_inf.department,
                                            each_url, each_title)
                my_spider.get_name_title
                teacher_inf_list.extend(my_spider.data[:])
            teacher_inf_data = tablib.Dataset(
                *teacher_inf_list, headers=HEADER)
            out_file = os.path.join(out_dir, 'out_table', '{s}_{d}.xls'.format(
                s=school, d=department))
            with open(out_file, 'wb') as f:
                f.write(teacher_inf_data.xls)
            status_df.loc[each_index, 3] = 'done'
    else:
        print('no spiders available')
    status_df.to_csv(STATUS_INI, header=None, index=False)


if __name__ == '__main__':
    main()
