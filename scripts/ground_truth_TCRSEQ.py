#!/usr/bin/env python

__author__ = "Igor Mandric"
__credits__ = ["Igor Mandric", "Serghei Mangul"]
__license__ = "GPL"
__maintainer__ = "Igor Mandric"
__email__ = "imandric1@student.gsu.edu"
__description__ = "Python script for computing ground truth based on barcodes for amplicon reads"



import sys
from collections import Counter
from Bio import SeqIO


# some global settings
__CLUSTER_THRESHOLD__ = 5 # if less or equal than this reads in a cluster, drop it
__DISREGARD_FREQUENCY__ = 0.9 # if the most popular nucleotide frequency less than this, drop the cluster


# functions

def consensus(reads):
    """
       Based on a bunch of reads, compute their consensus
       @ params reads - a list of string
    """
    disregard = False
    if len(set(map(len, reads))) != 1:
        raise Exception("The reads of the cluster are not of the same length or the cluster is empty!")
    positions = range(len(reads[0]))
    consensusSeq = ""
    for position in positions:
        bases = [x[position] for x in reads]
        basesCounter = Counter(bases)
        topFrequency = basesCounter.most_common(1)[0][1] * 1.0 / len(reads)
        if topFrequency < __DISREGARD_FREQUENCY__:
            disregard = True
            break
        consensusSeq += basesCounter.most_common(1)[0][0]
    if disregard:
        return None
    return consensusSeq    



# first argument is a fastq file with reads (no barcode)
reads = sys.argv[1]

# second argument is a fasta file with barcodes (the same IDs)
barcodes = sys.argv[2]

# output filename
output = sys.argv[3]

rdict = {} # keep reads here
for record in SeqIO.parse(reads, "fastq"):
    rdict[record.id] = str(record.seq)

bdict = {} # barcodes go here
barcodesSeq = []
"""bdict is like this: barcode -> [read IDs]"""
for record in SeqIO.parse(barcodes, "fasta"):
    if str(record.seq) not in bdict:
        bdict[str(record.seq)] = []
    bdict[str(record.seq)].append(record.id)
    barcodesSeq.append(str(record.seq))

readCounter = Counter(barcodesSeq)
goodBarcodes = [x for x, y in readCounter.items() if y > __CLUSTER_THRESHOLD__]

print len(goodBarcodes)

ground_truth = {}
# determine consensus for all good barcodes
for barcode in goodBarcodes:
    clusterReads = [rdict[r] for r in bdict[barcode]]
    consensusSeq = consensus(clusterReads)
    if consensusSeq:
        for readID in bdict[barcode]:
            ground_truth[readID] = consensusSeq

print len(ground_truth)

with open(output, "w") as output_handle:
    for readID, readSeq in ground_truth.items():
        output_handle.write("@%s\n" % readID)
        output_handle.write("%s\n" % readSeq)
        output_handle.write("+\n")
        output_handle.write("%s\n" % ("I" * len(readSeq)))

