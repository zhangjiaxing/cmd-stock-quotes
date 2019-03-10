#!/usr/bin/python3

import urllib.request

stock_list = [
    "sh000001",  # 上证指数
    "sz002157",  # 正邦科技
    "sz002124",  # 天邦股份
    "sz002714",  # 牧原股份
    "sz002477",  # 雏鹰农牧
    "sz002385",  # 大北农
    "sz002567",  # 唐人神
    "sz000876",  # 新希望
    "sh600975",  # 新五丰
    "sz002234",  # 民和股份
]

display_filed_list = "代码 涨幅 今开 昨收 当前 最高 最低 日期 时间".split(' ')

FIELD_INDEX_DICT = {
    "代码": 0,
    "名称": 1,
    "今开": 2,
    "昨收": 3,
    "当前": 4,
    "最高": 5, 
    "最低": 6,
    "竞买": 7,  # 买一
    "竞卖": 8,  # 卖一
    "成交数": 9,  # 通常把该值除以一百
    "成交金额": 10,  # 通常把该值除以一万
    "日期": -4,
    "时间": -3,
    "涨幅": -1
}


if __name__ == "__main__":
    for name in display_filed_list:
        print("%-10s" % name, end='')
    print()

    url = "http://hq.sinajs.cn/?format=text&list=" + ','.join(stock_list)

    with urllib.request.urlopen(url) as f:
        data = f.read().decode('gb18030')
        data = data.replace('=', ',')
        line_list = data.splitlines()
        for line in line_list:
            field_list = line.split(',')
            field_list.append(round((float(field_list[4])-float(field_list[3]))/float(field_list[3]) * 100, 2 )) # 涨幅
            for name in display_filed_list:
                print("%-12s" % field_list[FIELD_INDEX_DICT[name]], end='')
            print()

