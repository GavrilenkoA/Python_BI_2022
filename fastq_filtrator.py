
def read_func(input_path):
    with open(input_path, "r") as file:
        data = file.read()
    return data


def get_every_read(data):
    reads = []
    data = data.split("\n")     # Разбиваем строку по переносу строки, получаем список.
    start_idx = 0
    for i in range(4, len(data), 4):    # Каждый  read чередуется с периодичностью 4.
        cur_reads = dict(zip(['id', 'seq', "sep", "quality"], data[start_idx:i]))   # Создаем для каждого рида словарь с ключами соотвествующими описанию fastq файла
        reads.append(cur_reads)     # кладем текущий рид в список
        start_idx = i
    return reads


def gc_calc(reads):
    gc_count = []
    for i in range(len(reads)):
        seq = reads[i]["seq"]
        GC_value = ((seq.count("C") + seq.count("G") ) /len(seq)) * 100
        gc_count.append(GC_value)
    return gc_count


def len_calc(reads):
    len_count = []
    for i in range(len(reads)):
        seq = reads[i]["seq"]
        cur_len = len(seq)
        len_count.append(cur_len)
    return len_count


def quality_calc(reads):
    average_quality = []
    for i in range(len(reads)):
        read_quality = reads[i]["quality"]
        quality_val = 0
        for ch in read_quality:
            quality_val += ord(ch) - 33
        average_quality_per_read = quality_val/len(read_quality)
        average_quality.append(average_quality_per_read)
    return average_quality


def sort_by_len(len_count, length_bounds):
    if type(length_bounds) != int:
        up = length_bounds[1]
        down = length_bounds[0]
    else:
        up = length_bounds
        down = 0
    passed_reads_idx = []
    failed_reads_idx = []
    for i in range(len(len_count)):
        if (len_count[i] <= up) and (len_count[i] >= down):
            passed_reads_idx.append(i)
        else:
            failed_reads_idx.append(i)
    return set(passed_reads_idx), set(failed_reads_idx)



def sort_by_GC(gc_count, gc_bounds):
    if type(gc_bounds) != int:
        up = gc_bounds[1]
        down = gc_bounds[0]
    else:
        up = gc_bounds
        down = 0
    passed_reads_idx = []
    failed_reads_idx = []
    for i in range(len(gc_count)):
        if (gc_count[i] <= up) and (gc_count[i] >= down):
            passed_reads_idx.append(i)
        else:
            failed_reads_idx.append(i)
    return set(passed_reads_idx), set(failed_reads_idx)



def sort_by_quality(average_quality, quality_threshold):
    passed_reads_idx = []
    failed_reads_idx = []
    for i in range(len(average_quality)):
        if average_quality[i] >= quality_threshold:
            passed_reads_idx.append(i)
        else:
            failed_reads_idx.append(i)
    return set(passed_reads_idx), set(failed_reads_idx)


def sorted_fastq(reads, passed_idx, failed_idx):
    passed_fastq = [reads[i] for i in passed_idx]
    failed_fastq = [reads[i] for i in failed_idx]
    return passed_fastq, failed_fastq


def write_output(output_path, passed_fastq, failed_fastq, save_filtered):
    if save_filtered:
        passed_path = output_path +"_passed.fastq"
        failed_path = output_path +"_failed.fastq"
        with open(passed_path, "w") as fi:
            for entry in passed_fastq:  # прохожусь по каждому отфильтрованному риду
                for i in entry.values():
                    fi.write(i)     # записываю каждую строку формата файла fastq с новой строки
                    fi.write("\n")
        with open(failed_path, "w") as fi:
            for entry in failed_fastq:
                for i in entry.values():
                    fi.write(i)
                    fi.write("\n")




def main(input_fastq, output_file_prefix, gc_bounds = (0, 100), length_bounds = (0, 2**32), quality_threshold=0,
         save_filtered=False):
    data = read_func(input_fastq)

    reads = get_every_read(data)

    gc_count = gc_calc(reads)
    passed_gc_idx, failed_gc_idx = sort_by_GC(gc_count, gc_bounds)  # используя индексы для фильтрации ридов
    all_idx = passed_gc_idx.union(failed_gc_idx)  # все индексы понадобятся в дальнейшем

    len_count = len_calc(reads)
    passed_len_idx, failed_len_idx = sort_by_len(len_count, length_bounds)

    average_quality = quality_calc(reads)
    passed_qual_idx, failed_qual_idx = sort_by_quality(average_quality, quality_threshold)

    passed_idx = passed_gc_idx & passed_len_idx & passed_qual_idx  # выбираю те индексы, которые пересекаются из выходов всех функций
    failed_idx = all_idx - passed_idx  # оставшиеся идут в failed

    passed_fastq, failed_fastq = sorted_fastq(reads, passed_idx, failed_idx)

    write_output(output_file_prefix, passed_fastq, failed_fastq, save_filtered)






#%%
#Test
input_fastq = "/home/alexg/IB/python/HW2/1_control_18S_2019_minq7.fastq"
output_file_prefix = "/home/alexg/IB/python/HW2/filtered"
main(input_fastq, output_file_prefix, gc_bounds=(20, 50), quality_threshold=5, save_filtered=True)