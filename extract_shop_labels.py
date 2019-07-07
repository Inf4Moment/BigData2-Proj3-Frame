# -*- coding:utf8 -*-

import json
import os
import re

attr_jump = re.compile(r'��Ʒ��Ϣ|����|�ɷ�|�ʵ�|����|���|ͬ��|(����|��|��)|����|���|����|ȹ��|����ͼ|����|��|��ʽ|����|����|���մ���|�鿴����|���|����|����|���ι���|��ȫ�ȼ�|Ʒ��|����|������|��Ʒ|��װ��ʽ|������|��״|��Ч|������|������ҵ|�Ƽ۵�λ|��ζ|��ζ|���|����|����װ|����|�պϷ�ʽ|����|Ь��߶�')
sub_jump = re.compile(r'�Ż�|����|�۸�|��ȯ|����|�')

files = os.listdir(r"./data")
for file_name in files:
    file_path = r"./data/" + file_name
    with open(file_path, "r", encoding="utf-8") as load_f:
        load_data = json.load(load_f)
    # shop id
    shop_id = load_data["shopUserId"]
    print('Extracting\t' + shop_id + '...')
    # shop name
    shop_info = ''
    if 'shopName' in load_data:
        shop_info += load_data['shopName'] + '\n'
    items = load_data["items"]
    # collect info of items
    for item in items:
        # ��Ʒ����
        if 'name' in item:
            shop_info += '-------' + '\n'
            shop_info += ' '.join(re.split(r'[\n,]', item['name'])) + '\n'
        if 'sales' in item:
            shop_info += item['sales'][4:-1] + '\n'
        else:
            shop_info += '0\n'
        if 'desc' in item:
            desc = item['desc']
            if 'subtitle' in desc and desc['subtitle'] != '\"��\"' \
                    and sub_jump.search(desc['subtitle']) is None:
                shop_info += desc['subtitle'] + '\n'
            shop_info += '+++++++' + '\n'
            for module in desc['modules']:
                if module['title'] == '��Ʒ��Ϣ':
                    texts = module['texts']
                    if texts[0] == '��Ʒ��Ϣ':
                        del texts[0]
                    if len(texts) != 0 and texts[-1] == '�鿴����':
                        texts.pop()
                    for text in texts:
                        if attr_jump.search(text) is None:
                            shop_info += text + '\n'
        shop_info += '=======' + '\n'
        # if 'reviewTags' in item:
        #     for tag in item['reviewTags']:
        #         shop_info += tag + '\n'
        # if 'firstNReviews' in item:
        #     for review in item['firstNReviews']:
        #         if 'add' in review:
        #             shop_info += '\n'.join(review['add'].split('\n')[1:]) + '\n'
        #         if 'content' in review:
        #             if review['content'] != '���û�û����д����!':
        #                 shop_info += review['content'] + '\n'
    # write
    output_path = r"./res/text/" + shop_id + ".txt"
    out = open(output_path, 'w', encoding='utf-8')
    out.write(shop_info)
    out.close()
