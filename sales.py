# -*- coding:utf8 -*-

import json
import os
from pandas import DataFrame

files = os.listdir(r"../data")
for file_name in files:
    file_path = r"../data/" + file_name
    with open(file_path, "r", encoding = "utf-8") as load_f:
        load_data = json.load(load_f)
    
    items = load_data["items"]
    item_num = len(items)
    item_name = [""] * item_num
    item_price = [0.0] * item_num
    item_priceSymbol = [""] * item_num
    item_postage = [0.0] * item_num
    item_sales = [0] * item_num

    for i in range(0, item_num):
        # 商品名称
        if "name" in items[i]:
            item_name[i] = items[i]["name"]
        # 商品价格
        if "price" in items[i]:
            item_price[i] = items[i]["price"]
        # 商品价格单位
        if "priceSymbol" in items[i]:
            item_priceSymbol[i] = items[i]["priceSymbol"]
        # 商品邮费
        if "postage" in items[i]:
            if r"包" in items[i]["postage"]:
                item_postage[i] = 0.0
            elif items[i]["postage"] == r"上门安装":
                item_postage[i] = 0.0
            else:
                item_postage[i] = float(items[i]["postage"][4:])
        # 商品销量
        if "sales" in items[i]:
            item_sales[i] = int(items[i]["sales"][4:-1])

    sales_data = DataFrame({
        "name": item_name,
        "price": item_price,
        "priceSymbol": item_priceSymbol,
        "postage": item_postage,
        "sales": item_sales
    })

    shop_id = load_data["shopUserId"]
    output_path = r"../csv/" + shop_id + ".csv"
    sales_data.to_csv(output_path, index = False)
    print(shop_id)