import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import gensim.models
import numpy as np
import jieba

# 过滤 stop word
# tokenizer = RegexpTokenizer(r'\w+')
stop_words = [line.strip() for line in open(r"./src/stop_word_CN.txt", encoding='UTF-8').readlines()]

# 输入输出准备
dir = "./test_data"
# dir = "./res/item_label"
out_dir = "./res/model"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 过滤规则
def my_filter(str):
    return (str not in stop_words and len(str) <= 21)

# 迭代器，每次读入一个文本
class MyDocs(object):
    def __init__(self, dirname):
        self.dirname = dirname
    # 迭代器，一个文件一个商店，一行字符串一个商品
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            input_str = ""
            for line in open(os.path.join(self.dirname, fname), encoding="utf-8"):
                item_name = line[0:line.find("\t")]      # 商品名称
                stemmed_tokens = [token for token in jieba.cut(line)]
                tokens_without_stopword = list(filter(my_filter, stemmed_tokens))
                yield tokens_without_stopword, fname + "--" + item_name
            '''
            for line in open(os.path.join(self.dirname, fname), encoding="utf-8"):
                input_str += line
            raw_tokens = tokenizer.tokenize(input_str)
            stemmed_tokens = [token for token in raw_tokens]
            # stemmed_tokens = [stemmer.stem(token) for token in raw_tokens]
            stemmed_tokens_without_stopword = list(filter(my_filter, stemmed_tokens))
            out = open("./simple/" + fname, "w")
            print(stemmed_tokens_without_stopword, end=" ", file=out)
            out.close()
            yield stemmed_tokens_without_stopword, fname
            '''

docs = MyDocs(dir)

'''
k = 0       # test
for tokens_without_stopword, item_name in docs:
    if k < 1000:
        if k % 20 == 0:
            print(item_name)
        k += 1
    else:
        break
'''

# 转为 doc2vec 模型的输入
class TaggedDoc(object):
    def __init__(self, docs_iter):
        self.docs_iter = docs_iter
    # 迭代器
    def __iter__(self):
        for tokens_without_stopword, item_name in self.docs_iter:
            # print(fname)
            yield gensim.models.doc2vec.TaggedDocument(tokens_without_stopword, [jieba.cut(item_name)])

taggedocs = TaggedDoc(docs)

# 训练
model = gensim.models.Doc2Vec(documents = taggedocs, workers = 8, size = 100, 
        negative = 5, hs = 0, min_count = 2, sample = 0, iter = 20)
model.save(os.path.join(out_dir, "my_model"))

# 预测
# model = gensim.models.Doc2Vec.load(os.path.join(out_dir, "my_model"))
N = 10
out_file = open(os.path.join(out_dir, "doc_vec.txt"), "w")
for text, item_name in docs:
    print(item_name, end = "\t", file = out_file)
    item_vec = model.infer_vector(str(text))
    topN_sims = model.docvecs.most_similar(positive = item_vec, topn = 3)
    # for i in model.infer_vector(str(text)):
    #     print(i, end = " ", file = out_file)
    print(file = out_file)

for text, item_name in docs:
    print(item_name, end = "\t")
    item_vec = model.infer_vector(str(text))
    topN_sims = model.docvecs.most_similar(positive = [item_vec], topn = 3)
    # for i in model.infer_vector(str(text)):
    #     print(i, end = " ", file = out_file)
    print()

# 读入
str = ""
data = []
name = []
for line in open("doc_vec.txt"):
    name.append(line[:line.index("\t")])
    list = line[line.index("\t") + 1:].split()
    list = [float(str) for str in list]
    data.append(list)
# 标准化
np_data = np.array(data)
np_data = (np_data - np.mean(np_data, axis=0)) / np.sqrt(np.var(np_data, axis=0))
# 输出
out = open("doc_vec_out.txt", "w")
for i, name in enumerate(name):
    print(name, end="\t", file=out)
    for f in np_data[i]:
        print(f, end=" ", file=out)
    print(file=out)

def printSimOutput(sims):
    indx = len(sims)    
    print("Total num of results: ", indx) 
    cntr = 1
    for index, label in sims:
        print(cntr, ') ', getLineFromLabledDocs(index))
        cntr = cntr + 1
        print("")

def getLineFromLabledDocs(tag):
    tempfilename, index = tag.split("_")
    #print ("filename: " + filename + ", index: " + index )
    return getLineFromFile(docpath + tempfilename, index)