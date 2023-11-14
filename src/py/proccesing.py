from os import listdir
import pymorphy3
import numpy as np
from string import punctuation
from tkinter import filedialog
import time
start_time = time.time()
#############################################################################################################################################################################

def process_func(path):

    # Все файлы из папки ####################################################################################################################################################
    files = np.array([f for f in listdir(f"{path}")])
    # Преобразование документов в списки #####################################################################################################################################
    lists = np.array([])
    for file in files:
        with open(f"{path}/{file}", mode='r', encoding='utf-8') as f:
            lists = np.append(lists, [[value.rstrip().upper() for value in f.readlines() if value != "\n"]])
    # Удаление мусора из всех строк ##########################################################################################################################################
    # translator = str.maketrans("", "", punctuation)
    # remove_punctuation = np.vectorize(lambda x: x.translate(translator)) # Если потребуется объяснить
    # lists = remove_punctuation(lists)

    lists = (np.vectorize(lambda x: x.translate(str.maketrans("", "", punctuation)))(lists))
    print(lists)
    print("--- %s seconds ---" % (time.time() - start_time))
    # Создание новых списков со всеми словами из документа ##################################################################################################################
    lists_words = []

    for doc in lists:
        words = []
        for string in doc:
            if string:
                words.extend(string.split())
        if words:
            lists_words.append(words)

    # Перевод всех слов в начальную форму. #################################################################################################################################
    final_lists = []
    s = []

    #with open(f"C:/Users/andre/Documents/Хакатон/stopwords-ru.txt", mode='r', encoding='utf-8') as f:
    #    stopwords = [i.strip() for i in f.readlines()]

    morph = pymorphy3.MorphAnalyzer()

    for list_ in lists_words:
        s = []
        for word in list_:
            s.append(morph.parse(word)[0].normal_form.upper())
        final_lists.append(s)

    return final_lists

############################################################################################################################################################################

path = filedialog.askdirectory()

if path != "":
    path = str(path)
else:
    exit()

print("Ожидайте...")

# path = "C:/Users/andre/Documents/Хакатон"
# path = input()

final_lists = process_func(path)


# Создание словаря со всеми ответами
words_dict = {}
answer_list = []

for list in final_lists:
    for word in list:
        words_dict[word] = list.count(word)
    answer_list.append(sorted(words_dict.items(), key = lambda items: items[1], reverse = True))
    words_dict = {}

print(len(answer_list))
print("--- %s seconds ---" % (time.time() - start_time))