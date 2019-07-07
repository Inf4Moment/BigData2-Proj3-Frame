# -*- coding:utf8 -*-

import json
import os
import re
import pandas
from snownlp import SnowNLP

N = 20

pos_max_item = pandas.DataFrame({       # 好评率最高的商品
    "name": [],
    "total_num": [],
    "pos_num": [],
    "neg_num": [],
    "pos_rate": [],
    "neg_rate": []
})
neg_max_item = pandas.DataFrame({       # 差评率最高的商品
    "name": [],
    "total_num": [],
    "pos_num": [],
    "neg_num": [],
    "pos_rate": [],
    "neg_rate": []
})

files = os.listdir(r"./data")
file_num = len(files)
shop_name = [""] * file_num         # 商店名称
shop_id = [""] * file_num           # 商店 ID
shop_pos_rate = [-1.0] * file_num   # 商店好评率
shop_neg_rate = [-1.0] * file_num   # 商店差评率

for k in range(0, 50):
    file_path = r"./data/" + files[k]
    with open(file_path, "r", encoding = "utf-8") as load_f:
        load_data = json.load(load_f)
    if "shopUserId" in load_data:
        shop_id[k] = load_data["shopUserId"]
    if "shopName" in load_data:    
        shop_name[k] = load_data["shopName"]

    items = load_data["items"]
    item_num = len(items)
    item_name = [""] * item_num         # 商品名称
    item_review_num = [0] * item_num    # 商品评论总量
    item_pos_num = [0] * item_num       # 商品好评数量
    item_neg_num = [0] * item_num       # 商品差评数量
    item_pos_rate = [-1.0] * item_num   # 商品好评率
    item_neg_rate = [-1.0] * item_num   # 商品差评率

    for i in range(0, item_num):
        # 商品名称
        if "name" in items[i]:
            item_name[i] = items[i]["name"]
        # 商品评论
        if "firstNReviews" in items[i]:
            for review in items[i]["firstNReviews"]:
                if "content" in review:
                    aly_review = SnowNLP(review["content"])     # 情感分析
                    review_score = aly_review.sentiments        # 为好评的概率
                    if review_score >= 0.7:            # 好评
                        item_pos_num[i] += 1
                    elif review_score < 0.3:          # 差评
                        item_neg_num[i] += 1
                    item_review_num[i] += 1
        # 计算
        if item_review_num[i] > 0:
            item_pos_rate[i] = item_pos_num[i] / item_review_num[i]
            item_neg_rate[i] = item_neg_num[i] / item_review_num[i]
        
    # 将商店中商品的评论信息保存到文件中
    review_data = pandas.DataFrame({
        "name": item_name,
        "total_num": item_review_num,
        "pos_num": item_pos_num,
        "neg_num": item_neg_num,
        "pos_rate": item_pos_rate,
        "neg_rate": item_neg_rate
    })

    pos_topN_item = review_data.nlargest(max(N, item_num), "pos_rate")
    pos_max_item = pandas.concat([pos_max_item, pos_topN_item])
    neg_topN_item = review_data.nlargest(max(N, item_num), "neg_rate")
    neg_max_item = pandas.concat([neg_max_item, neg_topN_item])
    # 
    shop_review_num = review_data["total_num"].sum()
    if shop_review_num > 0:
        shop_pos_rate[k] = review_data["pos_num"].sum() / shop_review_num   # 商品好评率
        shop_neg_rate[k] = review_data["neg_num"].sum() / shop_review_num   # 商品差评率
    # 
    print(k)

pos_topN_item = pos_topN_item.nlargest(N, "pos_rate")
neg_topN_item = neg_topN_item.nlargest(N, "neg_rate")

# 将商店的评论信息保存到文件中
review_data = pandas.DataFrame({
    "name": shop_name,
    "id": shop_id,
    "pos_rate": shop_pos_rate,
    "neg_rate": shop_neg_rate
})
pos_topN_shop = review_data.nlargest(N, "pos_rate")
neg_topN_shop = review_data.nlargest(N, "neg_rate")

pos_topN_item.to_json(orient = "records", force_ascii = False, path_or_buf = "./res/pos_topN_item.json")
neg_topN_item.to_json(orient = "records", force_ascii = False, path_or_buf = "./res/neg_topN_item.json")
pos_topN_shop.to_json(orient = "records", force_ascii = False, path_or_buf = "./res/pos_topN_shop.json")
neg_topN_shop.to_json(orient = "records", force_ascii = False, path_or_buf = "./res/neg_topN_shop.json")
