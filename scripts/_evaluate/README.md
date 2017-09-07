# How to run evaluation scripts


Command to run bowtie2 in order to obtain ground truths:

for x in `ls ../reads/IGH`; do bowtie2 --quiet --no-hd --reorder -k 1 -q -p 5 -x bowtie2_index/igh_transcripts_index -U ../reads/IGH/$x/input_2.fastq -S sam/IGH/$x/input_2.sam; done
