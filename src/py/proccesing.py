from os import listdir
import pymorphy3

from tkinter import *
from tkinter import filedialog

#############################################################################################################################################################################

def process_func(path):

    # Все файлы из папки ####################################################################################################################################################
    files = [f for f in listdir(f"{path}")]

    # Преобразование документов в списки #####################################################################################################################################
    lists = []

    for file in files:
        with open(f"{path}/{file}", mode='r', encoding='utf-8') as f:
            f = [value for value in f.readlines() if value != "\n"]
            lists.append(f)

    # Срезание у строк списков \n в конце и перевод в верхний регистр ########################################################################################################
    for list in lists:
        for i in range(len(list)):
            list[i] = list[i][:-1]
            list[i] = list[i].upper()

    # Удаление мусора из всех строк ##########################################################################################################################################
    for list in lists:
        for string in range(len(list)):
            for symb in list[string]:
                n = ord(symb)
                if not (n >= 1040 and n <= 1071) or n == 1025 or n == 32:
                    list[string] = list[string].replace(symb, " ", 1)

    # Цифры сверху в цикле это Юникод крайних русских букв и пару исключений
    # print(ord("А"), ord("Я"), ord("Ё"), ord(" "))

    # Создание новых списков со всеми словами из документа ##################################################################################################################
    lists_words = []

    for list in lists:
        words = []
        for string in list:
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

print(answer_list)
