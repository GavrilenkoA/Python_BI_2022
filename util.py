def process_seq(seq: str):
    idx_low = [idx for idx, ch in enumerate(seq) if ch.islower()]
    seq = seq.upper()
    return idx_low, seq


def output_seq(idx_low, seq: str):
    seq = [ch for ch in seq]
    for idx in idx_low:
        seq[idx] = seq[idx].lower()
    seq = "".join(seq)
    return seq


def check_acid(target: set, orig: set):
    default = True
    for i in target:
        if i in orig:
            continue
        else:
            default = False
            break
    return default


def transfer(seq: str, dna=True):
    seq = [ch for ch in seq]
    if dna:
        dict_sub = {"A": "T", "T": "A", "G": "C", "C": "G"}
    else:
        dict_sub = {"A": "U", "U": "A", "G": "C", "C": "G"}
    for i in range(len(seq)):
        seq[i] = dict_sub[seq[i]]
    seq = "".join(seq)
    return seq


def transribe(seq: str):
    idx_low, seq = process_seq(seq)
    dna_alpha = {"A", "T", "G", "C"}
    cur_seq = set(seq)
    val = check_acid(cur_seq, dna_alpha)
    if val:
        seq = transfer(seq)
        seq = output_seq(idx_low, seq)
        return seq
    else:
        return "Invalid alphabet. Try again!"


def reverse(seq: str):
    rna_alpha = {"A", "U", "G", "C", "a", "u", "g", "c"}
    dna_alpha = {"A", "T", "G", "C", "a", "t", "g", "c"}
    cur_seq = set(seq)
    val1 = check_acid(cur_seq, rna_alpha)
    val2 = check_acid(cur_seq, dna_alpha)
    if val1 or val2:
        seq = [ch for ch in seq]
        for i in range(len(seq) // 2):
            if i != len(seq) // 2:
                temp = seq[i]
                seq[i] = seq[len(seq) - i - 1]
                seq[len(seq) - i - 1] = temp
        seq = "".join(seq)
        return seq
    else:
        return "Invalid alphabet. Try again!"



def complement(seq: str):
    idx_low, seq = process_seq(seq)
    cur_seq = set(seq)
    rna_alpha = {"A", "U", "G", "C"}
    dna_alpha = {"A", "T", "G", "C"}
    val_dna = check_acid(cur_seq, dna_alpha)
    val_rna = check_acid(cur_seq, rna_alpha)
    if (val_dna and val_rna) or (val_dna and not val_rna):
        seq = transfer(seq)
    elif (not val_dna) and (val_rna):
        seq = transfer(seq, dna=False)
    else:
        return "Invalid alphabet. Try again!"
    seq = output_seq(idx_low, seq)
    return seq


def reverse_comlement(seq: str):
    seq1 = complement(seq)
    if seq1 != "Invalid alphabet. Try again!":
        seq = reverse(seq1)
        return seq
    else:
        return seq1


while True:
    inp = input("Enter command: ")
    seq = input("Enter sequence: ")
    if inp == "transcribe":
        print(transribe(seq))
    elif inp == "reverse":
        print(reverse(seq))
    elif inp == "complement":
        print(complement(seq))
    elif inp == "reverse comlement":
        print(reverse_comlement(seq))
    elif inp == "exit":
        print("Good luck")
        break

















#%%
