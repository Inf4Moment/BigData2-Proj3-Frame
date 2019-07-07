from pyhanlp import *
import os
import json
from operator import itemgetter

CoreStopWordDictionary = SafeJClass("com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary")
# NLPTokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
Nature = SafeJClass("com.hankcs.hanlp.corpus.tag.Nature")
ClusterAnalyzer = SafeJClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
reserve_words_feature = [Nature.ns, Nature.n, Nature.vn, Nature.nr]

analyzer_item = ClusterAnalyzer()
analyzer_shop = ClusterAnalyzer()
shop_set = {}
item_set = {}
key_set = {}
key_count = {}

files = os.listdir(r"../text")
for file_name in files:
    file_path = r"../text/" + file_name
    shop_id = file_name.split('.')[0]
    shop_sales = 0
    key_text = ''
    shop_text = ''
    item_text = ''
    item_flag = False
    shop_flag = False
    for line in open(file_path, "r", encoding="utf-8"):
        if '-------' in line:
            item_text = ''
            shop_text = ''
            item_flag = True
            shop_flag = True
        elif '+++++++' in line:
            item_text += shop_text
            shop_flag = False
        elif '=======' in line:
            key_text += item_text
            item_sales = int(item_text.split(',')[1])
            shop_sales += item_sales
            item_set[item_text.split(',')[0]] = (item_text, item_sales, shop_id)
            analyzer_item.addDocument(item_text.split(',')[0], item_text)
            item_flag = False
        else:
            if shop_flag:
                shop_text += line[:-1] + ','
            elif item_flag:
                item_text += line[:-1] + ','
            else:
                key_text += line[:-1] + ','

    shop_name = key_text.split(',')[0]
    shop_text += shop_name + ','

    print('Extracting\t' + shop_id + '\tKeyword...')

    filter_text = ''
    text_seg = HanLP.segment(key_text)
    CoreStopWordDictionary.apply(text_seg)
    for word in text_seg:
        if word.nature in reserve_words_feature:
            filter_text += word.word + '\n'
    keyword_list = HanLP.extractKeyword(filter_text, 100)

    py_key_list = []
    py_key_list.extend(keyword_list)
    for key in keyword_list:
        key_count[key] = key_count.setdefault(key, 0) + 1
    key_set[shop_name] = py_key_list[:5]

    shop_text += ','.join(py_key_list[:9]*5)
    shop_set[shop_name] = (shop_text, shop_sales)
    analyzer_shop.addDocument(shop_name, shop_text)

print('Reloading\tShop\tKeyword...')

shop_sale_path = './res/shop_sale.json'

with open(shop_sale_path, 'r', encoding='utf-8') as load_f:
    shop_sale = json.load(load_f)
    load_f.close()
for item in shop_sale:
    item['keyword'] = key_set.get(item['name'], [])

out = open(shop_sale_path, 'w', encoding='utf-8')
# out.write('\n'.join(keyword_list))
json.dump(shop_sale, out, indent=2, ensure_ascii=False)
out.close()

print('Reloading\tShop\tKeyword\tOK...')
print('Computing\tLabel\tCloud...')

N = 100
key_out = []
for item in sorted(key_count.items(), key=itemgetter(1), reverse=True):
    key_out.append({
        'name': item[0],
        'value': item[1],
    })
    N -= 1
    if N == 0:
        break

output_path = './res/label_cloud.json'
out = open(output_path, 'w', encoding='utf-8')
json.dump(key_out, out, indent=2, ensure_ascii=False)
out.close()

print('Computing\tLabel\tCloud\tOK...')
print('Clustering\tShops...')

clusters = analyzer_shop.repeatedBisection(9, 6.0)
cluster_list = []
for cluster in clusters:
    py_cluster = []
    cluster_text = ''
    for item in cluster:
        py_cluster.append((item, shop_set[item][1]))
        cluster_text += shop_set[item][0]

    filter_text = ''
    text_seg = HanLP.segment(cluster_text)
    CoreStopWordDictionary.apply(text_seg)
    for word in text_seg:
        if word.nature in reserve_words_feature:
            filter_text += word.word + '\n'

    keyword_list = HanLP.extractKeyword(filter_text, 6)
    py_key_list = []
    py_key_list.extend(keyword_list)
    # for key in keyword_list:
    #     py_key_list.append(key)

    cluster_set = []
    for item in sorted(py_cluster, key=itemgetter(1), reverse=True)[:10]:
        cluster_set.append({
            'name': item[0],
            'sale': item[1],
        })
    cluster_list.append({
        'category': py_key_list,
        'items': cluster_set,
    })

output_path = './res/shop_cluster.json'
out = open(output_path, 'w', encoding='utf-8')
json.dump(cluster_list, out, indent=2, ensure_ascii=False)
out.close()

print('Clusters\tNum\tIs\t' + str(len(cluster_list)))
print('Clustering\tShops\tOK...')

print('Clustering\tItems...')

clusters = analyzer_item.repeatedBisection(6.0)
cluster_list = []
for cluster in clusters:
    py_cluster = []
    cluster_text = ''
    for item in cluster:
        py_cluster.append((item, item_set[item][1], item_set[item][2]))
        cluster_text += item_set[item][0]

    filter_text = ''
    text_seg = HanLP.segment(cluster_text)
    CoreStopWordDictionary.apply(text_seg)
    for word in text_seg:
        if word.nature in reserve_words_feature:
            filter_text += word.word + '\n'

    keyword_list = HanLP.extractKeyword(filter_text, 6)
    py_key_list = []
    py_key_list.extend(keyword_list)

    # cluster_set = []
    # for item in sorted(py_cluster, key=itemgetter(1), reverse=True):
    #     cluster_set.append({
    #         'name': item[0],
    #         'shop_id': item[2],
    #     })
    # cluster_list.append({
    #     'category': py_key_list,
    #     'items': cluster_set,
    # })

    cluster_set = []
    for item in sorted(py_cluster, key=itemgetter(1), reverse=True)[:10]:
        cluster_set.append({
            'name': item[0],
            'sale': item[1],
        })
    cluster_list.append({
        'category': py_key_list,
        'items': cluster_set,
    })

# output_path = './res/item_cluster.json'
output_path = './res/item_cluster_for_rec.json'
out = open(output_path, 'w', encoding='utf-8')
json.dump(cluster_list, out, indent=2, ensure_ascii=False)
out.close()

print('Clusters\tNum\tIs\t' + str(len(cluster_list)))
print('Clustering\tItems\tOK...')
