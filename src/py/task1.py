import os
from tkinter import filedialog
import re
import pymorphy3
import time
start_time = time.time()

def get_files(path):
    files = [f for f in os.listdir(f"{path}")]
    docs = []

    for file in files:
        with open(f"{path}/{file}", mode='r', encoding='utf-8') as f:
            f = [value.strip().upper() for value in f.readlines() if value != "\n"]
            docs.append(f)

    return docs, files, path

def clean_files(doc):
    doc = list(map(lambda s: re.sub(r'[^a-zA-Zа-яА-ЯёЁ\s]', '', s),doc))

    return doc

def get_words(doc):
    docs_words = []
    for string in doc:
        docs_words.extend(string.split())

    return docs_words

def get_infinitive(doc):
    morph = pymorphy3.MorphAnalyzer()

    docs_words = list(map(lambda word: morph.parse(word)[0].normal_form.upper(), doc))

    return docs_words

def del_stopwords(doc):
    with open("stopwords-ru.txt", mode='r', encoding='utf-8') as f:
        stopwords = list(map(lambda s: s.rstrip(), f.readlines()))

    only_words = []

    for word in doc:
        if word not in stopwords:
            only_words.append(word)
    
    return only_words

def get_answer(doc):
    words_dict = {}

    for word in doc:
        words_dict[word] = doc.count(word)
    words_dict = sorted(words_dict.items(), key = lambda items: items[1], reverse = True)

    return words_dict

def create_dir(docs, files_name, path, flag):
    if flag == 1:
        os.mkdir(f'{path}/output')
    if flag == 2:
        os.mkdir(f'{path}/output_themes')
    for doc in range(len(docs)):
        if flag == 1:
            with open(f"{path}/output/{files_name[doc]}", mode='w', encoding='utf-8') as f:
                for line in docs[doc]:
                    f.write(f'{line[0]}\t{line[1]}\n')
        if flag == 2:
            with open(f"{path}/output_themes/{files_name[doc]}", mode='w', encoding='utf-8') as f:
                for line in docs[doc]:
                    f.write(f'{line[0]}\t{line[1]}\n')

def god_func(**kwargs):

    in_path = kwards["in_path"]
    out_pth = kwargs["out_path"]
    flag = kwargs["flag"]


    docs, files_name, path_docs = get_files(in_path)
    docs = map(clean_files, docs)
    docs = map(get_words, docs)
    docs = map(get_infinitive, docs)
    docs = map(del_stopwords, docs)
    answer_list = list(map(get_answer, docs))
    create_dir(answer_list, files_name, out_path, flag)

    print("--- %s seconds ---" % (time.time() - start_time))
    return list(docs)

