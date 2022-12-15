import os
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?',
                    default=sys.stdin)
args = parser.parse_args()
entry = args.infile
if type(entry) == str:
    file_exists = os.path.exists(entry)
    if file_exists:
        file = open(entry)
        data = file.read()
        print(data)
        file.close()
    else:
        sys.stdout.write(f'cat: {entry}: No such file or directory'+"\n")
else:
    for line in sys.stdin:
        sys.stdout.write(line.strip()+"\n")







# entry = args.infile
# file_exists = os.path.exists(entry)
# if file_exists:
#     file = open(entry)
#
# else:
#     print(f'cat: {entry}: No such file or directory')



#
# for line in sys.stdin:
#     sys.stdout.write(line.strip()+"\n")
#
# file_name_given = input()   # вот здесь argparse

# file_exists = os.path.exists(file_name_given)
# print(file_exists)
# #%%
# if file_exists:
#     inf = open(file_name_given)
#     for line in inf:
#         sys.stdout.write(line)


#%%
os.getcwd()
#%%
