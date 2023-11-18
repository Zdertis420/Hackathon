import os
import re
import pymorphy3
import gc
# gc.disable()

def get_files(path, var):
    files = [f for f in os.listdir(path)]
    docs = []
    for file in files:
        if not os.path.isfile(f'{path}/{file}'): 
            continue
        with open(f"{path}/{file}", mode='r', encoding='utf-8') as f:
            f = [value.strip().upper() for value in f.readlines() if value != "\n"]
            docs.append(f)
        try:
            var = min(var, int(file))
        except:
            continue

    return docs, files, path, var


def clean_files(doc):
    doc = list(map(lambda s: re.sub(r'[^a-zA-Zа-яА-ЯёЁ\s]', '', s), doc))

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
    tmp_folder = os.path.dirname(__file__)  # ! НЕ УДАЛЯТЬ, СЛОМАЕТЕ
    with open(os.path.join(tmp_folder, "stopwords-ru.txt"), mode='r', encoding='utf-8') as f:
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
    words_dict = sorted(words_dict.items(), key=lambda items: items[1], reverse=True)

    return words_dict


def new_name_dir(path):
    if not os.path.exists(f'{path}/output'): return ''
    counter = 2
    while True:
        if os.path.exists(f'{path}/output{counter}'):
            counter += 1
            continue
        return counter


def create_dir(docs, files_name, path):
    counter = new_name_dir(path)
    os.makedirs(f'{path}/output{counter}', exist_ok=True)
    for doc in range(len(docs)):
        with open(f"{path}/output{counter}/{files_name[doc]}", mode='w', encoding='utf-8') as f:
            for line in docs[doc]:
                f.write(f'{line[0]}\t{line[1]}\n')


def god_func(**kwargs):
    in_path = kwargs["in_path"]
    out_path = kwargs["out_path"]
    flag = kwargs["flag"]

    ## эта функция вернёт номер первого файла в добавок

    var = 1e69
    docs, files_name, path_docs, var = get_files(in_path, var)
    docs = map(clean_files, docs)
    docs = map(get_words, docs)
    docs = map(get_infinitive, docs)
    docs = map(del_stopwords, docs)

    if flag == 1:
        answer_list = list(map(get_answer, docs))
        create_dir(answer_list, files_name, out_path)

    if flag == 3:
        return list(docs), var

