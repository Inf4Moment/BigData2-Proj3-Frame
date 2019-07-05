import gensim
import os
import gensim.models
import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

# 进行stem和过滤stop word
tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
stemmed_stop_words = set([stemmer.stem(token) for token in stop_words])
# 输入输出准备
dir = "./base"
out_dir = "./processed"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# 过滤规则
def my_filter(str):
    return (str not in stop_words and
            len(str) <= 21)


# 迭代器，每次读入一个文本
class MyDocs(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            input_str = ""
            for line in open(os.path.join(self.dirname, fname), encoding="utf-8"):
                input_str += line
            raw_tokens = tokenizer.tokenize(input_str)
            stemmed_tokens = [token for token in raw_tokens]
            # stemmed_tokens = [stemmer.stem(token) for token in raw_tokens]
            stemmed_tokens_without_stopword = list(filter(my_filter, stemmed_tokens))
            out = open(".\\simple\\" + fname, "w")
            print(stemmed_tokens_without_stopword, end=" ", file=out)
            out.close()
            yield stemmed_tokens_without_stopword, fname


docs = MyDocs(dir)


# 转为doc2vec模型的输入
class TaggedDoc(object):
    def __init__(self, docs_iter):
        self.docs_iter = docs_iter

    def __iter__(self):
        for stemmed_tokens_without_stopword, fname in self.docs_iter:
            # print(fname)
            yield gensim.models.doc2vec.TaggedDocument(stemmed_tokens_without_stopword, fname)


taggedocs = TaggedDoc(docs)

# 训练
model = gensim.models.Doc2Vec(taggedocs, workers=8, vector_size=200)
model.save(os.path.join(out_dir, "my_model"))

# 预测
model = gensim.models.Doc2Vec.load(os.path.join(out_dir, "my_model"))
out_file = open(os.path.join(out_dir, "doc_vec.txt"), "w")
for text, fname in docs:
    print(fname, end="\t", file=out_file)
    for i in model.infer_vector(str(text)):
        print(i, end=" ", file=out_file)
    print(file=out_file)

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
