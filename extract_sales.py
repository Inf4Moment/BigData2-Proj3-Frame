# -*- coding:utf8 -*-

import json
import os
import re
from pandas import DataFrame

tariff_pattern_1 = re.compile(r"进口税: 预计(?P<tariff>[0-9]+.[0-9]+)元")
tariff_pattern_2 = re.compile(r"进口税: 预计(?P<tariff_low>[0-9]+.[0-9]+) - (?P<tariff_high>[0-9]+.[0-9]+)元")
tariff_pattern_3 = re.compile(r"进口税: (?P<percent>[0-9]+.[0-9]+)% 如需征收买家承担")

files = os.listdir(r"./data")
for file_name in files:
    file_path = r"./data/" + file_name
    with open(file_path, "r", encoding = "utf-8") as load_f:
        load_data = json.load(load_f)
    
    items = load_data["items"]
    item_num = len(items)
    item_name = [""] * item_num
    item_price = [0.0] * item_num
    item_postage = [0.0] * item_num
    item_sales = [0] * item_num
    item_tariff = [0.0] * item_num

    for i in range(0, item_num):
        # 商品名称
        if "name" in items[i]:
            item_name[i] = items[i]["name"]
        # 商品价格
        if "price" in items[i]:
            if items[i]["price"] is not None:
                item_price[i] = items[i]["price"]
        # 商品邮费
        if "postage" in items[i]:
            if r"包" in items[i]["postage"]:            # 包邮
                item_postage[i] = 0.0
            elif items[i]["postage"] == r"上门安装":    # 上门安装
                item_postage[i] = 0.0
            else:                                       # 邮费: xx.xx
                item_postage[i] = float(items[i]["postage"][4:])
        # 商品销量
        if "sales" in items[i]:
            # 月销量 xxxx件
            item_sales[i] = int(items[i]["sales"][4:-1])
        # 商品进口税
        if "tariff" in items[i]:
            # 进口税: 预计xx.xx元
            obj = tariff_pattern_1.search(items[i]["tariff"])
            if obj:
                item_tariff[i] = float(obj.group("tariff"))
            # 进口税: 预计xx.xx - xx.xx元
            obj = tariff_pattern_2.search(items[i]["tariff"])
            if obj:
                item_tariff[i] = (float(obj.group("tariff_low")) + float(obj.group("tariff_high"))) / 2
            # 进口税: xx% 如需征收买家承担
            obj = tariff_pattern_3.search(items[i]["tariff"])
            if obj and item_price[i] > 0:   # 价格不为空
                item_tariff[i] = item_price[i] * float(obj.group("percent")) / 100
            # 其余情形全部默认为 0
            # + 进口税: 买家自行承担
            # + 商家包税
            # + 商家承担

    sales_data = DataFrame({
        "name": item_name,
        "price": item_price,
        "postage": item_postage,
        "sales": item_sales,
        "tariff": item_tariff
    })

    shop_id = load_data["shopUserId"]
    output_path = r"./res/sales_info/" + shop_id + ".csv"
    sales_data.to_csv(output_path, index = False, encoding = "utf-8")
    print(shop_id)
