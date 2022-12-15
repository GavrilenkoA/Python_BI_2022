import sys
import os
import argparse
import re

# %%
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lines', action='store_const', const='-l')
parser.add_argument('-w', '--words', action='store_const', const='-w')
parser.add_argument('-c', '--bytes', action='store_const', const='-c')
parser.add_argument('file', nargs="*")
args = parser.parse_args()
# %%
lines = args.lines
word = args.words
byte = args.bytes


# %%


# %%
def count_stat(entry, line, word, byte, file=1):
    if file:  # если на вход файл
        file = open(entry)
        data = file.read()
        file.close()
        bytes = os.path.getsize(entry)  # размер в байтах для файла
    else:  # если поток
        data = entry
        bytes = len(data)  # размер в байтах? для потока
    pat_new_line = r"\n"  # кол-во строк
    lines = len(re.findall(pat_new_line, data))
    pat_every_word = r"\S+"  # кол-во слов
    words = len(re.findall(pat_every_word, data))
    if ((line is None) and (word is None) and (byte is None)) or (
            (line is not None) and (word is not None) and (byte is not None)):
        return [lines, words, bytes]
    if (line is not None) and (word is None) and (byte is None):
        return [lines]
    if (line is None) and (word is not None) and (byte is None):
        return [words]
    if (line is not None) and (word is not None) and (byte is None):
        return [bytes]
    if (line is not None) and (word is not None) and (byte is None):
        return [lines, words]
    if (line is not None) and (word is None) and (byte is not None):
        return [lines, bytes]
    if (line is None) and (word is not None) and (byte is not None):
        return [words, bytes]


# %%

if len(args.file) > 0:  # если подаются на вход файлы
    if len(args.file) == 1:  # если один файл
        path = args.file[0]
        if os.path.isdir(path):  # если это директория
            print(f"wc: {path}: Is a directory")
            print(0, 0, 0, f"{path}", sep="\t")
            sys.exit(0)
        if os.path.isfile(path):
            ans = count_stat(path, lines, word, byte, file=1)
            print(*ans, path)
        else:
            print(f"wc: {path}: No such file or directory")
    else:  # если более одного файла
        i = 0  # переменная для подсчета итераций
        for path in args.file:
            if os.path.isdir(path):
                print(f"wc: {path}: Is a directory")
                print(0, 0, 0, f"{path}", sep="\t")
                continue
            if os.path.isfile(path):  # постоянно проверяем существует ли файл
                i += 1
                ans = count_stat(path, lines, word, byte, file=1)
                print(*ans, path, sep="\t")
                if i == 1:  # если это первый файл, начинаем суммировать статистику с нулем
                    total_sum = [0] * len(ans)
                    total_sum = map(lambda x, y: x + y, ans, total_sum)
                else:  # продолжаем суммировать статистику
                    total_sum = map(lambda x, y: x + y, ans, total_sum)
            else:  # если не существует файла, выводим сообщение
                print(f"wc: {path}: No such file or directory")
        print(*total_sum, "total", sep="\t")  # суммарная статистика
else:  # если на вход поток
    for line in sys.stdin:
        if line is None:  # если в конечном счете ничего не получили -> выходим
            sys.exit(0)
        ans = count_stat(line, lines, word, byte, file=0)
        print(*ans, sep="\t")

# %%
