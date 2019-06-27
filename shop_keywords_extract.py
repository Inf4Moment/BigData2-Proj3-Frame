from pyhanlp import *
import os

CoreStopWordDictionary = JClass("com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary")
# NLPTokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
Nature = JClass("com.hankcs.hanlp.corpus.tag.Nature")
reserve_words_feature = [Nature.ns, Nature.n, Nature.vn, Nature.nr]

files = os.listdir(r"../text")
for file_name in files:
    file_path = r"../text/" + file_name
    all_the_text = open(file_path, "r", encoding="utf-8").read()

    print('Extracting\t' + file_name + '\tKeyword...')

    filter_text = ""
    text_seg = HanLP.segment(all_the_text)
    CoreStopWordDictionary.apply(text_seg)
    for word in text_seg:
        if word.nature in reserve_words_feature:
            filter_text += word.word + '\n'

    keyword_list = HanLP.extractKeyword(filter_text, 5)

    output_path = r"../text_keyword/" + file_name.split('.')[0] + '_keyword.txt'
    out = open(output_path, 'w', encoding='utf-8')
    for keyword in keyword_list:
        out.write(keyword + '\n')
    out.close()
