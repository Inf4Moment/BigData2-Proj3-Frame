# -*- coding:utf8 -*-

import json
import os
import re
import pandas
from snownlp import SnowNLP

# 统计各商店好评率、差评率
pos_max_item = {"rate": -1.0}   # 好评率最高的商品
neg_max_item = {"rate": -1.0}   # 差评率最高的商品
pos_max_shop = {"rate": -1.0}   # 好评率最高的商店
neg_max_shop = {"rate": -1.0}   # 差评率最高的商店

files = os.listdir(r"./data")
file_num = len(files)
shop_name = [""] * file_num         # 商店名称
shop_id = [""] * file_num           # 商店 ID
shop_pos_rate = [-1.0] * file_num   # 商店好评率
shop_neg_rate = [-1.0] * file_num   # 商店差评率

for k in range(0, file_num):
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

        '''
        output_path = r"./res/item_rate/" + shop_id[k] + ".csv"
        review_data.to_csv(output_path, index = False, encoding = "utf-8")
        '''

        pos_max_index = review_data["pos_rate"].argmax()     # 好评率最高商品
        if review_data["pos_rate"][pos_max_index] > pos_max_item["rate"]:
            pos_max_item["rate"] = review_data["pos_rate"][pos_max_index]
            pos_max_item["item"] = review_data["name"][pos_max_index]
            pos_max_item["shop_id"] = shop_id[k]
            pos_max_item["shop_name"] = shop_name[k]
        neg_max_index = review_data["neg_rate"].argmax()     # 差评率最高商品
        if review_data["neg_rate"][neg_max_index] > neg_max_item["rate"]:
            neg_max_item["rate"] = review_data["neg_rate"][neg_max_index]
            neg_max_item["item"] = shop_id[k]
            pos_max_item["shop_id"] = shop_id[k]
            pos_max_item["shop_name"] = shop_name[k]
        
        shop_review_num = review_data["total_num"].sum()
        if shop_review_num > 0:
            shop_pos_rate[k] = review_data["pos_num"].sum() / shop_review_num   # 商品好评率
            shop_neg_rate[k] = review_data["neg_num"].sum() / shop_review_num   # 商品差评率

    print(shop_id[k])

# 将商店的评论信息保存到文件中
review_data = pandas.DataFrame({
    "name": shop_name,
    "id": shop_id,
    "pos_rate": shop_pos_rate,
    "neg_rate": shop_neg_rate
})
review_data.to_csv(r"./res/shop_rate.csv", index = False, encoding = "utf-8")

pos_max_index = review_data["pos_rate"].argmax()     # 好评率最高商品
pos_max_shop["name"] = review_data["name"][pos_max_index]
pos_max_shop["rate"] = review_data["pos_rate"][pos_max_index]
neg_max_index = review_data["neg_rate"].argmax()     # 差评率最高商品
neg_max_shop["name"] = review_data["name"][neg_max_index]
neg_max_shop["rate"] = review_data["neg_rate"][neg_max_index]

# 好评率、差评率最高的相关信息
review_info = {
    "item_max_pos_review_rate": pos_max_item,
    "item_max_neg_review_rate": neg_max_item,
    "shop_max_pos_review_rate": pos_max_shop,
    "shop_max_neg_review_rate": neg_max_shop,
}
review_profile = open(r"./res/review_profile.json", "w", encoding = "utf-8")
json.dump(review_info, review_profile, indent = 4, ensure_ascii = False)
review_profile.close()
