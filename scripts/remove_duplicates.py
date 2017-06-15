
######################################################################################
####    Script for removing some unnecessary reads from EC output file            ####
####    If you want to run it for .fasta files, just change lines 18 and/or 23    ####
######################################################################################

import sys
from Bio import SeqIO

# assumption: corrected must have the same IDs as original

original = sys.argv[1]
corrected = sys.argv[2]
compressed = sys.argv[3]


ordict = {}
for record in SeqIO.parse(original, "fastq"):
    ordict[record.id] = record


codict = {}
for record in SeqIO.parse(corrected, "fastq"):
    codict[record.id] = record



common = set(ordict.keys()) & set(codict.keys())

complist = []

for ID in common:
    orread = ordict.get(ID)
    coread = codict.get(ID)
    if str(orread.seq) != str(coread.seq):
        complist.append(coread)



with open(compressed, "w") as handle:
    SeqIO.write(complist, handle, "fastq")

