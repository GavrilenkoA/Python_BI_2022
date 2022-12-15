# ! /usr/bin/env python3
import argparse
import os
import sys
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--recurs', help='remove recursively', action='store_const', const='-r')
parser.add_argument('path', nargs='?')
args = parser.parse_args()
target = args.path
if target is None:  # если нет входного файла -> выдаем ошибку
    print('rm: missing operand \nTry rm --help for more information.')
    sys.exit(0)
if os.path.exists(target):  # проверяем существует ли такая директория\файл
    if os.path.isfile(target):  # проверяем файл ли это
        os.remove(target)
    else:
        if args.recurs is None:
            print(f"rm: cannot remove '{target}': Is a directory")  # без флага -r директорию удалить не сможем
        else:
            shutil.rmtree(target)  # а директорию можем удалить только с помощью флага -r
else:
    sys.stdout.write(f"rm: cannot remove '{target}': No such file or directory" + '\n')
