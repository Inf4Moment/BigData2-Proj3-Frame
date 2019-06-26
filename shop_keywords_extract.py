from pyhanlp import *
import os

files = os.listdir(r"../text")
for file_name in files:
    file_path = r"../text/" + file_name
    all_the_text = open(file_path, "r", encoding="utf-8").read()

    print('Extracting\t' + file_name + '\tKeyword...')

    keyword_list = HanLP.extractKeyword(all_the_text, 5)

    output_path = r"../text_keyword/" + file_name.split('.')[0] + '_keyword.txt'
    out = open(output_path, 'w', encoding='utf-8')
    for keyword in keyword_list:
        out.write(keyword + '\n')
    out.close()
