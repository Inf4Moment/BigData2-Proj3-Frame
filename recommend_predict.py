# -*- coding:utf8 -*-

import json

with open(r"./res/item_cluster_for_rec.json", "r", encoding = "utf-8") as load_f:
    item_cluster = json.load(load_f)



with open(file_path, "r", encoding = "utf-8") as load_f:
        load_data = json.load(load_f)