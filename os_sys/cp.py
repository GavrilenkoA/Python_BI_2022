#! /usr/bin/env python3
import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--recurs', help='cp recursively', action='store_const', const='-r')
parser.add_argument('source', help="name of source", nargs="*")
parser.add_argument('dest', help="destination path", nargs="+")
args = parser.parse_args()
source = args.source
destination = args.dest[0]
files_destin = os.listdir(destination)  # директории может и не быть?
for entry in source:  # итерируемся через все входные файлы/директории
    if os.path.isfile(entry):  # проверяем файл ли это
        if entry in files_destin:
            continue  # если файл уже есть в конечной директории, то ничего не делаем
        else:
            shutil.copy(entry, destination)
    else:  # если директория
        if args.recurs is None:  # если в инпуте директория -> необходимо иметь флаг -r
            print(f"cp: -r not specified; omitting directory '{entry}'")
        else:
            if entry in files_destin:  # если такая директория/файл уже есть в destination -> пропускаем
                continue
            else:
                entry = os.path.abspath(entry)  # поучим полный путь директории
                dir_name = os.path.split(entry)[-1]     # возьмем ее название
                dest_path = os.path.abspath(destination)    # полный путь директории куда будем копировать
                new_dir = os.path.join(dest_path, dir_name) # склеим путь dest директории и исходной
                os.mkdir(new_dir)   # создадим директорию с таким же именем, что и исходная
                shutil.copytree(entry, new_dir, dirs_exist_ok=True) # положим в нее все что было

