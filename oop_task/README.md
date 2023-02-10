__Sorting fastqs files using OOP__
Python script in sort_fastq/sorting_fastq.py
__sort_fastq/example.fastq - example of fastq file__
__sort_fastq/sorted.fastq - resulted sorted file__
__Realization__:
1. Function read_fastq need path to fastq file.
2. The Function sequentially prosseses read by read at a time and creates the instances of Read class and puts them in a list.
3. The class FASTQFile accepts a list from instances of the READ class and path to write new sort fastq file. The class has method for sorting read by length, gc content, quality and id name.
4. Function read_fastq return instance of FASTQFile class, that alredy  has sorted fastq file.
5. To write new sort fastq file, use method write_to_file of FASTQFile class.
