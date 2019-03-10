#!/usr/bin/bash

LIST=""
LIST="$LIST,sh000001"  # 上证指数
LIST="$LIST,sz002157"  # 正邦科技
LIST="$LIST,sz002124"  # 天邦股份
LIST="$LIST,sz002714"  # 牧原股份
LIST="$LIST,sz002477"  # 雏鹰农牧
LIST="$LIST,sz002385"  # 大北农
LIST="$LIST,sz002567"  # 唐人神
LIST="$LIST,sz000876"  # 新希望
LIST="$LIST,sh600975"  # 新五丰
LIST="$LIST,sz002234"  # 民和股份


FIELD="名称,今开,昨收,当前,最高,最低,竞买价,竞卖价,成交数,成交金额,时间"

DATA=`curl "http://hq.sinajs.cn/?format=text&list=$LIST" 2>/dev/null | iconv -f "gb2312" -t "utf8" | tr '=' ',' | cut -d ',' -f '2-11,32-33'`

echo -e "$FIELD \n$DATA" | column -s "," -t

