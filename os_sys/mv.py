#! /usr/bin/env python3

# переименование присходит если файлы в одной директории
import os
import sys
import argparse
import shutil

# %%
parser = argparse.ArgumentParser()
parser.add_argument('a', help="destination path", nargs="+")
parser.add_argument("b")
args = parser.parse_args()
input1 = args.a
input2 = args.b
if len(input1) > 1:  # если первых инпутов (input1) больше чем один, то это однозначно перемещение в директорию
    # input2
    if os.path.isdir(input2):  # то куда перемещаем должна быть директория
        for entry in input1:
            if os.path.exists(entry):
                if entry in os.listdir(input2):  # если entry уже есть в директории, просто удаляем его из сходной
                    os.remove(entry)
                else:
                    shutil.move(entry, input2)
            else:
                print(f"mv: cannot stat '{input1}': No such file or directory")
    else:
        print(f"mv: target '{input2}' is not a directory")
else:  # один input1 на вход, здесь может быть как перемещение, так и переименование
    entry = input1[0]
    if os.path.exists(entry):  # проверяем что input 1 существует
        if not os.path.exists(input2) or os.path.isfile(input2):  # input2 не существует или input2 это файл -> это
            # переименование
            a = os.path.split(entry)[-1]
            b = os.path.split(input2)[-1]
            if a == b:  # проверка, что это одинаковые файлы
                print(f"mv: '{a}' and '{b}' are the same file")
            else:
                os.rename(entry, input2)
        if os.path.isdir(input2):  # если input 2 директория -> перемещение
            if os.path.isdir(entry):
                common = os.path.commonpath([entry, input2])
                entry_name = os.path.split(entry)[-2]
                if entry_name == common:    # если это две одинаковых директории в одной директории
                    print(f"mv: cannot move '{entry_name}' to a subdirectory of itself, {entry_name}/{entry_name}")

            if entry in os.listdir(input2):  # если input1 уже есть в директории, просто удаляем его из сходной
                os.remove(entry)
            else:  # если нет -> перемещаем
                shutil.move(entry, input2)
        else:
            print(f"mv: target '{input2}' is not a directory")

# %%
