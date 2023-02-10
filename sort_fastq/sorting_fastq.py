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
        gc_content = sum(map(lambda x: x == "C" or x == "G", read_sequence))/len(read_sequence)
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
        stat_per_read = {}   # словарь (статистика рида): объект рида
        for fastq in self.fastq_records:
            stat_per_read[(fastq.mean_quality(), len(fastq), fastq.gc(), fastq.read_id)] = fastq
        stat = [key for key in stat_per_read]   # положим все статистики ридов в виде кортежей в список
        stat = sorted(stat)     # сортируем кортежи внутри списка
        for k, i in enumerate(stat):    # вернемся к объектам из сортированных статистик
            fastq = stat_per_read[i]
            self.fastq_records[k] = fastq   # изменим исходный атрибут


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