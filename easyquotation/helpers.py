# coding:utf8
import json
import os
import re

import requests

STOCK_CODE_PATH = 'stock_codes.conf'
FUTURES_CODE_PATH = 'futures_codes.conf'


def update_stock_codes():
    """获取所有股票 ID 到 all_stock_code 目录下"""
    all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
    grep_stock_codes = re.compile('~(\d+)`')
    response = requests.get(all_stock_codes_url)
    all_stock_codes = grep_stock_codes.findall(response.text)
    with open(stock_code_path(), 'w') as f:
        f.write(json.dumps(dict(stock=all_stock_codes)))


def get_stock_codes(realtime=False):
    """获取所有股票 ID 到 all_stock_code 目录下"""
    if realtime:
        all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
        grep_stock_codes = re.compile('~(\d+)`')
        response = requests.get(all_stock_codes_url)
        stock_codes = grep_stock_codes.findall(response.text)
        with open(stock_code_path(), 'w') as f:
            f.write(json.dumps(dict(stock=stock_codes)))
        return stock_codes
    else:
        with open(stock_code_path()) as f:
            return json.load(f)['stock']


def stock_code_path():
    return os.path.join(os.path.dirname(__file__), STOCK_CODE_PATH)

def update_futures_codes():
    """获取所有期货 ID 到 all_futures_code 目录下"""
    all_futures_codes_url = 'http://finance.sina.com.cn/iframe/futuresIndex/fu_index_contract.js'
    grep_futures_codes = re.compile('fu_index_contract = ({.*})')
    response = requests.get(all_futures_codes_url)
    all_futures_codes = grep_futures_codes.findall(response.text)[0]
    with open(futures_code_path(), 'w') as f:
        f.write(json.dumps(dict(futures=all_futures_codes)))


def get_futures_codes(realtime=False):
    """获取所有期货 ID 到 all_futures_code 目录下"""
    if realtime:
        all_futures_codes_url = 'http://finance.sina.com.cn/iframe/futuresIndex/fu_index_contract.js'
        grep_futures_codes = re.compile('fu_index_contract = ({.*})')
        response = requests.get(all_futures_codes_url)
        futures_codes = grep_futures_codes.findall(response.text)[0]
        print(futures_codes)
        with open(futures_code_path(), 'w') as f:
            f.write(json.dumps(dict(futures=futures_codes)))
        return futures_codes
    else:
        with open(stock_code_path()) as f:
            return json.load(f)['futures']


def futures_code_path():
    return os.path.join(os.path.dirname(__file__), FUTURES_CODE_PATH)