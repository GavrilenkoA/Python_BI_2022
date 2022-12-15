import argparse
import os





# %%

parser = argparse.ArgumentParser()
parser.add_argument('nm', help="name of directories", nargs='*', default=None)
args = parser.parse_args()
dirs = args.nm
if len(dirs) == 0:  # если не ввели ни одного названия директории, выводим сообщение
    print("mkdir: missing operand \n Try mkdir --help for more information.")
else:
    for dir in dirs:
        if os.path.exists(dir):
            print(f"mkdir: cannot create directory '{dir}': File exists")
        else:
            os.mkdir(dir)