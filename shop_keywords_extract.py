# from pyhanlp import *
import os
import json

# CoreStopWordDictionary = SafeJClass("com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary")
# NLPTokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
# Nature = SafeJClass("com.hankcs.hanlp.corpus.tag.Nature")
# ClusterAnalyzer = SafeJClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
# reserve_words_feature = [Nature.ns, Nature.n, Nature.vn, Nature.nr]

# analyzer_item = ClusterAnalyzer()
# analyzer_shop = ClusterAnalyzer()
shop_set = {}
item_set = {}
key_set = {}

files = os.listdir(r"../text")
for file_name in files:
    file_path = r"../text/" + file_name
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
            item_set[item_text.split('\n')[0]] = item_text
            # analyzer_item.addDocument(item_text.split('\n')[0], item_text)
            item_flag = False
        else:
            if shop_flag:
                shop_text += line + ','
            elif item_flag:
                item_text += line + ','
            else:
                key_text += line + ','

    shop_text += key_text.split(',')[0] + ','

    print('Extracting\t' + file_name + '\tKeyword...')

    # filter_text = ''
    # text_seg = HanLP.segment(key_text)
    # CoreStopWordDictionary.apply(text_seg)
    # for word in text_seg:
    #     if word.nature in reserve_words_feature:
    #         filter_text += word.word + '\n'
    # keyword_list = HanLP.extractKeyword(filter_text, 5)
    #
    # py_key_list = []
    # for key in keyword_list:
    #     py_key_list.append(key)
    # key_set[file_name.split('.')[0]] = py_key_list
    #
    # shop_text += ','.join(py_key_list*5)
    # shop_set[file_name.split('.')[0]] = shop_text
    # analyzer_shop.addDocument(file_name.split('.')[0], shop_text)

output_path = './res/keyword.json'
out = open(output_path, 'w', encoding='utf-8')
# out.write('\n'.join(keyword_list))
json.dump(key_set, out, indent=4, ensure_ascii=False)
out.close()

print('Clustering\tShops...')

# clusters = analyzer_shop.repeatedBisection(16)
# cluster_list = []
# for cluster in clusters:
#     py_cluster = []
#     for item in cluster:
#         py_cluster.append(item)
#     cluster_text = ''
#     for item in py_cluster:
#         cluster_text += shop_set[item]
#
#     filter_text = ''
#     text_seg = HanLP.segment(cluster_text)
#     CoreStopWordDictionary.apply(text_seg)
#     for word in text_seg:
#         if word.nature in reserve_words_feature:
#             filter_text += word.word + '\n'
#
#     keyword_list = HanLP.extractKeyword(filter_text, 3)
#     py_key_list = []
#     for key in keyword_list:
#         py_key_list.append(key)
#
#     cluster_set = {
#         'key_word': py_key_list,
#         'shop_list': py_cluster,
#     }
#     cluster_list.append(cluster_set)
# output_path = './res/shop_cluster.json'
# out = open(output_path, 'w', encoding='utf-8')
# json.dump(cluster_list, out, indent=4, ensure_ascii=False)
# out.close()

print('Clustering\tShops\tOK...')

print('Clustering\tItems...')

# clusters = analyzer_item.repeatedBisection(16)
# cluster_list = []
# for cluster in clusters:
#     py_cluster = []
#     for item in cluster:
#         py_cluster.append(item)
#     cluster_text = ''
#     for item in py_cluster:
#         cluster_text += item_set[item]
#
#     filter_text = ''
#     text_seg = HanLP.segment(cluster_text)
#     CoreStopWordDictionary.apply(text_seg)
#     for word in text_seg:
#         if word.nature in reserve_words_feature:
#             filter_text += word.word + '\n'
#
#     keyword_list = HanLP.extractKeyword(filter_text, 3)
#     py_key_list = []
#     for key in keyword_list:
#         py_key_list.append(key)
#
#     cluster_set = {
#         'key_word': py_key_list,
#         'item_list': py_cluster,
#     }
#     cluster_list.append(cluster_set)
# output_path = './res/item_cluster.json'
# out = open(output_path, 'w', encoding='utf-8')
# json.dump(cluster_list, out, indent=4, ensure_ascii=False)
# out.close()

print('Clustering\tItems\tOK...')
