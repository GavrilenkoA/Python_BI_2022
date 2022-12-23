import re
import os


def process_batch(batch):
    batch[0] = re.sub(r'\n|@', '', batch[0])  # удаляю перенос строки и символ @ из идентификатора
    for i in range(1, len(batch)):
        batch[i] = re.sub(r'\n', '', batch[i])  # у всех остальных удаляю перенос строки


class Read:
    def __init__(self, read_id, read_sequence, comment, quality):
        self.read_id = read_id
        self.read_sequence = read_sequence
        self.comment = comment
        self.quality = quality

    def gc(self):
        read_sequence = self.read_sequence

        def find(ch):
            if ch == "G" or ch == "C":
                return 1
            else:
                return 0

        gc_content = sum(map(find, read_sequence)) / len(read_sequence)
        return gc_content

    def mean_quality(self):
        quality = self.quality
        mean = sum(map(lambda x: ord(x) - 33, quality)) / len(quality)
        return mean

    def __len__(self):
        read_sequence = self.read_sequence
        return len(read_sequence)


class FASTQFile:
    def __init__(self, fastq_records, file_path):  # file_path - путь до исходного fastq файла
        self.fastq_records = fastq_records
        self.file_path = file_path

    def sort_reads(self):
        def check_duplicate(data):  # проверка на дубликаты
            unique_data = list(set(data))
            if len(unique_data) == len(data):  # если длина осталась такая же, то дубликатов нет
                return False
            else:  # если длина изменилась(уменьшилась), то есть дубликаты
                return True

        def get_quality(read):  # вытаскивание качества
            quality = read.mean_quality()
            return quality

        def get_length(read):  # вытаскивание длины
            length = len(read)
            return length

        def get_gc(read):  # вытаскивание gc
            gc = read.gc()
            return gc

        def get_id(read):  # вытаскивание id
            idi = read.read_id
            return idi

        self.fastq_records.sort(key=get_quality)
        qualities = [get_quality(read) for read in self.fastq_records]
        if check_duplicate(qualities):  # проверка на повторяющиеся значения, если они есть то сортируем по длине и
            # так далее...
            self.fastq_records.sort(key=get_length)
            lengths = [get_length(read) for read in self.fastq_records]
            if check_duplicate(lengths):
                self.fastq_records.sort(key=get_gc)
                gc_stat = [get_gc(read) for read in self.fastq_records]
                if check_duplicate(gc_stat):
                    self.fastq_records.sort(key=get_id)

    def write_to_file(self):
        file_path = self.file_path
        prefix = os.path.split(file_path)[0]
        path = "sorted.fastq"
        file_path = os.path.join(prefix, path)  # создали новый путь для sorted fastq файла, в той же директории
        fastq_records = self.fastq_records
        with open(file_path, "w") as file:
            for fastq in fastq_records:
                file.write("@" + fastq.read_id + "\n")
                file.write(fastq.read_sequence + "\n")
                file.write(fastq.comment + "\n")
                file.write(fastq.quality + "\n")


def read_fastq(fastq_file_name):
    with open(fastq_file_name) as file:
        a = 0  # счетчик
        batch = []  # в batch будем класть один рид
        reads = []
        line = file.readline()
        batch.append(line)
        a += 1  # после прочтения обновляем на единицу
        while line:  # пока строка непустая
            line = file.readline()
            batch.append(line)
            a += 1
            if a == 4:  # считали 4 строки, то есть информацию одного рида
                process_batch(batch)  # удаляем переносы сроки и @ из идентификатора
                read = Read(*batch)  # создаем объект класса Read
                reads.append(read)
                batch = []
                a = 0
    fastq_file = FASTQFile(reads, fastq_file_name)
    fastq_file.sort_reads()
    return fastq_file

# %%
fastq_file = read_fastq("./example.fastq")
#%%
fastq_file.write_to_file()