#! /usr/bin/env python3
# coding=utf-8

import click
import os

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
    my_spider = S_spider.Spider(school, department, out_dir)
    my_spider.get_name_title


if __name__ == '__main__':
    main()
