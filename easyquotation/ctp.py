# coding:utf8
import re

from .basequotation import BaseQuotation


class Ctp(BaseQuotation):
    """新浪传统期货免费行情获取"""
    max_num = 800
    grep_detail = re.compile(r'(\w{1,2}\d+)=([^\s][^,]+?)%s%s' % (r',([\.\d]+)' * 14, r',([^\s]+?)' * 13))
    stock_api = 'http://hq.sinajs.cn/?format=text&list='

    def _gen_stock_prefix(self, stock_codes):
        return stock_codes

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        grep_str = self.grep_detail
        result = grep_str.finditer(stocks_detail)
        stock_dict = dict()
        for stock_match_object in result:
            stock = stock_match_object.groups()
            stock_dict[stock[0]] = dict(
                name=stock[1],
                open=float(stock[3]),
                high=float(stock[4]),
                low=float(stock[5]),
                buy=float(stock[8]),
                sell=float(stock[9]),
                settlement=float(stock[10]),
                ystd_settlement=float(stock[11]),
                buy_volume=int(stock[12]),
                sell_volume=int(stock[13]),
                holding_volume=int(stock[14]),
                volume=int(stock[15]),
                exchange=str(stock[16]),
                commodity_name=str(stock[17]),
                date=str(stock[18]),
            )
        return stock_dict
