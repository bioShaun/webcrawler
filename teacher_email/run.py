#! /usr/bin/env python3
# coding=utf-8

import click
import os

TEST_URL = 'http://linxue.imau.edu.cn/szdw/jsjj.htm'
CURRENT_DIR = os.getcwd()


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
    output_file = os.path.join(out_dir, '{s}_{d}.xls'.format(
        s=school, d=department
    ))
    my_spider = S_spider.Spider(school, department, output_file)
    my_spider.output


if __name__ == '__main__':
    main()
