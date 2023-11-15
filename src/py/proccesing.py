import numpy as np
import os
from tkinter import filedialog
import re
import pymorphy3

def get_files(path):
    files = [f for f in os.listdir(f"{path}")]
    docs = []

    for file in files:
        with open(f"{path}/{file}", mode='r', encoding='utf-8') as f:
            f = [value.strip().upper() for value in f.readlines() if value != "\n"]
            docs.append(f)

    return docs, files

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
    docs_words = []

    docs_words = list(map(lambda word: morph.parse(word)[0].normal_form.upper(), doc))

    return docs_words

def get_answer(doc):
    words_dict = {}

    for word in doc:
        words_dict[word] = doc.count(word)
    words_dict = sorted(words_dict.items(), key = lambda items: items[1], reverse = True)

    return words_dict

def create_dir(docs, files_name):
    os.mkdir(f'{path}/output')
    for doc in range(len(docs)):
        with open(f"{path}/output/{files_name[doc]}", mode='w', encoding='utf-8') as f:
            for line in docs[doc]:
                f.write(f'{line[0]}\t{line[1]}\n')

def god_func(path):
    docs, files_name = get_files(path)
    docs = map(clean_files, docs)
    docs = map(get_words, docs)
    docs = map(get_infinitive, docs)
    answer_list = list(map(get_answer, docs))
    create_dir(answer_list, files_name)

path = filedialog.askdirectory()

if path != "":
    path = str(path)
else:
    exit()

god_func(path)
