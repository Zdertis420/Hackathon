from os import listdir

# Все файлы из папки
files = [f for f in listdir("C:\\Users\\andre\Documents\Хакатон\docs\docs\\utf8")]

# Преобразование документов в списки
lists = []

for file in files:
    with open(f"C:\\Users\\andre\Documents\Хакатон\docs\docs\\utf8\\{file}", mode = 'r', encoding = 'utf-8') as f:
        f = [value for value in f.readlines() if value != "\n"]
        lists.append(f)

# Срезание у строк списков \n в конце и перевод в верхний регистр
for list in lists:
    for i in range(len(list)):
        list[i] = list[i][:-1]
        list[i] = list[i].upper()

# Удаление мусора из всех строк
for list in lists:
    for string in range(len(list)):
        for symb in list[string]:
            n = ord(symb)
            if not (n >= 1040 and n <= 1071) or n == 1025 or n == 32:
                list[string] = list[string].replace(symb, " ", 1)

# Цифры сверху в цикле это Юникод крайних русских букв и пару исключений
# print(ord("А"), ord("Я"), ord("Ё"), ord(" "))


# Создание новых списков со всеми словами из документа
lists_words = []

for list in lists:
    words = []
    for string in list:
        if string:
            words.extend(string.split())
    if words:
        lists_words.append(words)

## Перевод всех слов в начальную форму. Раскомментируйте этот код ТОЛЬКО если вам не жалко времени, ну или если у вас есть кружка чая. 
## 
## Это счётчик слов чтобы не умереть со скуки, пока код компилится. Не обращайте внимания.
# cc = 0
# for i in lists_words:
#     cc += len(i)
# print(cc)
# 
# import pymorphy2
# morph = pymorphy2.MorphAnalyzer()
# 
# c = 0
# for list in lists_words:
#     for word in range(len(list)):
#         list[word] = morph.parse(list[word])[0].normal_form.upper()
#         c += 1
#         print(c)
# 
# print(lists_words)
