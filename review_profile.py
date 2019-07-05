# -*- coding:utf8 -*-

import json
import os
import re
import pandas

N = 50

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
pos_max_shop = pandas.DataFrame({       # 好评率最高的商店
    "name": [],
    "id": [],
    "total_num": [],
    "pos_num": [],
    "neg_num": [],
    "pos_rate": [],
    "neg_rate": []
})
neg_max_shop = pandas.DataFrame({       # 差评率最高的商店
    "name": [],
    "id": [],
    "total_num": [],
    "pos_num": [],
    "neg_num": [],
    "pos_rate": [],
    "neg_rate": []
})   

files = os.listdir(r"./res/item_rate")
file_num = len(files)

for file_id in files:
    file_path = r"./data/" + file_id
    shop_df = pandas.read_csv(file_path)

review_data.nlargest(N)