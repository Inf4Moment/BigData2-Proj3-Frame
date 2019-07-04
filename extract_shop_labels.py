# -*- coding:utf8 -*-

import json
import os
import re

attr_jump = re.compile(r'商品信息|材质|成分|弹力|年份季节|吊牌图|销售|厚薄|款式|版型|工艺处理|查看更多|风格|适用|面料|服饰工艺|安全等级|品牌|产地|净含量|产品|包装方式|条形码|形状|功效|保质期|生产企业|计价单位|口味|气味|规格|功能|量贩装|种类|闭合方式|货号|鞋帮高度')
sub_jump = re.compile(r'优惠|购物')

files = os.listdir(r"../data")
for file_name in files:
    file_path = r"../data/" + file_name
    with open(file_path, "r", encoding="utf-8") as load_f:
        load_data = json.load(load_f)

    shop_id = load_data["shopUserId"]
    print('Extracting\t' + shop_id + '...')

    shop_info = ''
    if 'shopName' in load_data:
        shop_info += load_data['shopName'] + '\n'
    items = load_data["items"]

    for item in items:
        # 商品名称
        if 'name' in item:
            shop_info += '-------' + '\n'
            shop_info += item['name'] + '\n'
        if 'desc' in item:
            desc = item['desc']
            if 'subtitle' in desc and desc['subtitle'] != '\"—\"' \
                    and sub_jump.search(desc['subtitle']) is None:
                shop_info += desc['subtitle'] + '\n'
            shop_info += '+++++++' + '\n'
            for module in desc['modules']:
                if module['title'] == '商品信息':
                    texts = module['texts']
                    if texts[0] == '商品信息':
                        del texts[0]
                    if len(texts) != 0 and texts[-1] == '查看更多':
                        texts.pop()
                    for text in texts:
                        if attr_jump.search(text) is None:
                            shop_info += text + '\n'
        shop_info += '=======' + '\n'
        if 'reviewTags' in item:
            for tag in item['reviewTags']:
                shop_info += tag + '\n'
        # if 'firstNReviews' in item:
        #     for review in item['firstNReviews']:
        #         if 'add' in review:
        #             shop_info += '\n'.join(review['add'].split('\n')[1:]) + '\n'
        #         if 'content' in review:
        #             if review['content'] != '此用户没有填写评论!':
        #                 shop_info += review['content'] + '\n'

    output_path = r"../text/" + shop_id + ".txt"
    out = open(output_path, 'w', encoding='utf-8')
    out.write(shop_info)
    out.close()
