# -*- coding:utf8 -*-

# 检查文件内容
import json
import os
import re

files = os.listdir(r"./data")
save_f = open("./check.csv", "w", encoding = "utf-8")

for file_name in files:
    file_path = r"./data/" + file_name
    with open(file_path, "r", encoding = "utf-8") as load_f:
        load_data = json.load(load_f)
    
    items = load_data["items"]
    item_num = len(items)
    item_price = [""] * item_num
    item_priceSymbol = [""] * item_num
    item_postage = [""] * item_num
    item_sales = [""] * item_num
    item_tariff = [""] * item_num

    for i in range(0, item_num):
        # 商品价格
        if "price" in items[i]:
            if isinstance(items[i]["price"], int) or isinstance(items[i]["price"], float):
                item_price[i] = ""
            else:
                item_price[i] = str(items[i]["price"])
        # 商品价格单位
        if "priceSymbol" in items[i]:
            item_priceSymbol[i] = items[i]["priceSymbol"]
        # 商品邮费
        if "postage" in items[i]:
            search_obj1 = re.match(r"快递: [0-9]+.[0-9]+", items[i]["postage"])
            search_obj2 = re.match(r"运费: [0-9]+.[0-9]+", items[i]["postage"])
            if not search_obj1 and not search_obj2:
                    item_postage[i] = items[i]["postage"]
        # 商品销量
        if "sales" in items[i]:
            search_obj = re.match(r"月销量 [0-9]+件", items[i]["sales"])
            if not search_obj:
                item_sales[i] = items[i]["sales"]
        # 商品进口税
        if "tariff" in items[i]:
            search_obj1 = re.match(r"进口税: 预计[0-9]+.[0-9]+元", items[i]["tariff"])
            search_obj2 = re.match(r"进口税: 预计[0-9]+.[0-9]+ - [0-9]+.[0-9]+元", items[i]["tariff"])
            if not search_obj1 and not search_obj2 and not "包税" in items[i]["tariff"] and not "商家承担" in items[i]["tariff"]:
                item_tariff[i] = items[i]["tariff"]

    save_f.write("/".join(set(item_price)))
    save_f.write(",")
    save_f.write("/".join(set(item_postage)))
    save_f.write(",")
    save_f.write("/".join(set(item_sales)))
    save_f.write(",")
    save_f.write("/".join(set(item_priceSymbol)))
    save_f.write(",")
    save_f.write("/".join(set(item_tariff)))
    save_f.write("\n")

save_f.close()
