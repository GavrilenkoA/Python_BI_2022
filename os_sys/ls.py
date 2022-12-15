# попробую сначала без опции a
# %%
import argparse
import os
import sys

# %%
# %%
parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default=os.getcwd())
parser.add_argument('-a', '--all', help='include starts with.', action='store_const', const='-a')
args = parser.parse_args()
target_dir = args.path
if os.path.isfile(target_dir):  # если путь это файл, то просто выводим его название
    print(target_dir)
    sys.exit(0)
if not os.path.exists(target_dir):  # если нет такой директории или файла, то выводим сообщение
    print(f"ls: cannot access '{target_dir}': No such file or directory")
    sys.exit(0)
if args.all == "-a":  # если есть флаг -a, включаем в тч начинающихся с .
    ans = os.listdir(target_dir)
    ans = " ".join(ans)
    print(ans)
else:  # если нет флага -a, исключаем начинающихся с
    all_files = os.listdir(target_dir)
    ans = [i for i in all_files if not i.startswith(".")]
    ans = " ".join(ans)
    print(ans)
