
##########################################################
###     Script for computing gain metric on reads      ###
##########################################################



import sys, os
import random, string
from Bio import SeqIO, AlignIO
from Bio import pairwise2
#from Bio.Emboss import Applications as apps

file1 = sys.argv[1] # this is the corrected reads file1
file2 = sys.argv[2] # this is the original reads file1
file3 = sys.argv[3] # this is the corrected reads file2
file4 = sys.argv[4] # this is the original reads file2
samfile1 = sys.argv[5] # this is the alignment of corrected reads to the reference transcripts
samfile2 = sys.argv[6]
tranfile = sys.argv[7]



def reverse_complement(seq):
    alt_map = {'ins':'0'}
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    for k,v in alt_map.iteritems():
        seq = seq.replace(k,v)
    bases = list(seq)
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)
    for k,v in alt_map.iteritems():
        bases = bases.replace(v,k)
    return bases




# original reads
origreads1 = {}
for record in SeqIO.parse(file2, "fastq"):
    origreads1[record.id] = str(record.seq)
   

origreads2 = {}
for record in SeqIO.parse(file4, "fastq"):
    origreads2[record.id] = str(record.seq)
#------------------------------------------




# reading reference transcripts
transcripts = {}
for record in SeqIO.parse(tranfile, "fasta"):
    transcripts[record.id] = str(record.seq)



mismatches1 = []
deletions1 = []
insertions1 = []
with open(samfile1) as f:
    s1 = f.readlines()
s1 = map(lambda x: x.strip().split(), s1)
true_dict1 = {}
for line in s1:
    read_name, orient, refseq, startpos = line[:4]
    length = len(line[9])
    if refseq not in transcripts:
        continue
    if orient not in ["0", "16", "256", "272"]:
        continue
    true_read = transcripts[refseq][int(startpos) - 1: int(startpos) - 1 + int(length)]
    if orient in ["16", "272"]:
        true_read = reverse_complement(true_read)
    original_read = origreads1[read_name]
    true_dict1[read_name] = true_read
    for i in range(min(len(original_read), len(true_read))):
        if original_read[i] != true_read[i]:
            mismatches1.append("%s:%s" % (read_name, i))
        

mismatches2 = []
deletions2 = []
insertions2 = []
with open(samfile2) as f:
    s2 = f.readlines()
s2 = map(lambda x: x.strip().split(), s2)
true_dict2 = {}
for line in s2:
    read_name, orient, refseq, startpos = line[:4]
    length = len(line[9])
    if refseq not in transcripts:
        continue
    if orient not in ["0", "16", "256", "272"]:
        continue
    true_read = transcripts[refseq][int(startpos) - 1: int(startpos) - 1 + int(length)]
    if orient in ["16", "272"]:
        true_read = reverse_complement(true_read)
    original_read = origreads2[read_name]
    true_dict2[read_name] = true_read
    for i in range(min(len(original_read), len(true_read))):
        if original_read[i] != true_read[i]:
            mismatches2.append("%s:%s" % (read_name, i))



corrdict1 = {}
for record in SeqIO.parse(file1, "fastq"):
    corrdict1[record.id] = str(record.seq)
corrdict2 = {}
for record in SeqIO.parse(file3, "fastq"):
    corrdict2[record.id] = str(record.seq)


common1 = set(true_dict1.keys()) & set(corrdict1.keys())

# format for errors
# mismatches: seq:position
# indels: seq:start-end
mismatches11 = []
insertions11 = []
deletions11 = []

for key in common1:
    alignment = pairwise2.align.globalms(corrdict1[key], true_dict1[key], 10, -1, -5, -2)[0]
    allen = len(alignment[0])
    read_position = -1
    insertion = False
    deletion = False
    instart = None
    delstart = None
    for i in range(allen):
        if alignment[0][i] != "-":
            read_position += 1 # this position belongs to the corrected read
        if alignment[0][i] == alignment[1][i]:
            if insertion == True:
                insertions11.append("%s:%s-%s" % (key, instart, read_position))
                insertion = False
                instart = None
            if deletion == True:
                deletions11.append("%s:%s-%s" % (key, delstart, read_position))
                deletion = False
                delstart = None
        else: # here is an error
            if alignment[0][i] == "-": # deletion
                deletion = True
                if delstart is None:
                    delstart = read_position
            elif alignment[1][i] == "-": #insertion
                insertion = True
                if instart is None:
                    instart = read_position
            else: #mismatch
                mismatches11.append("%s:%s" % (key, read_position))


mismatches22 = []
insertions22 = []
deletions22 = []

common2 = set(true_dict2.keys()) & set(corrdict2.keys())

for key in common2:
    alignment = pairwise2.align.globalms(corrdict2[key], true_dict2[key], 10, -1, -5, -2)[0]
    allen = len(alignment[0])
    read_position = -1
    insertion = False
    deletion = False
    instart = None
    delstart = None
    for i in range(allen):
        if alignment[0][i] != "-":
            read_position += 1 # this position belongs to the corrected read
        if alignment[0][i] == alignment[1][i]:
            if insertion == True:
                insertions22.append("%s:%s-%s" % (key, instart, read_position))
                insertion = False
                instart = None
            if deletion == True:
                deletions22.append("%s:%s-%s" % (key, delstart, read_position))
                deletion = False
                delstart = None
        else: # here is an error
            if alignment[0][i] == "-": # deletion
                deletion = True
                if delstart is None:
                    delstart = read_position
            elif alignment[1][i] == "-": #insertion
                insertion = True
                if instart is None:
                    instart = read_position
            else: #mismatch
                mismatches22.append("%s:%s" % (key, read_position))


errors_after_ec = (mismatches11 + deletions11 + insertions11) + (mismatches11 + deletions11 + insertions11)
errors_before_ec = (mismatches1 + deletions1 + insertions1) + (mismatches2 + deletions2 + insertions2)


tp = len(set(errors_before_ec) - set(errors_after_ec))
fp = len(set(errors_after_ec) - set(errors_before_ec))
fn = len(set(errors_before_ec) & set(errors_after_ec))

gain = (tp - fp) * 1.0 / (tp + fn)

sens = tp * 1.0 / (tp + fn)


print file1.split("/")[-2], gain, sens, tp, fp, fn, len(errors_before_ec), len(errors_after_ec)
