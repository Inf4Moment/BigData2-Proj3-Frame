# 预测
model = gensim.models.Doc2Vec.load(os.path.join(out_dir, "my_model"))
out_file = open(os.path.join(out_dir, "doc_vec.txt"), "w")
for text, item_name in docs:
    print(item_name, end = "\t", file = out_file)
    for i in model.infer_vector(str(text)):
        print(i, end = " ", file = out_file)
    print(file = out_file)

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
