

from Bio import SeqIO
import sys
import jellyfish


gt1 = sys.argv[1]
gt2 = sys.argv[2]
corrected_reads1 = sys.argv[3]
corrected_reads2 = sys.argv[4]

with open(gt1) as f:
    gt1 = f.readlines()


gt1 = map(lambda x: x.strip().split(), gt1)

gt1dict = {}

for x, y, z in gt1:
    gt1dict[x] = (y, z)



with open(gt2) as f:
    gt2 = f.readlines()


gt2 = map(lambda x: x.strip().split(), gt2)

gt2dict = {}

for x, y, z in gt2:
    gt2dict[x] = (y, z)



histogram = {}

handle = open(corrected_reads1, "rU")
for record in SeqIO.parse(handle, "fastq"):
    if True:
        if record.id in gt1dict:
            corread = record.seq.tostring()
            origread, trueread = gt1dict[record.id]
            distance = jellyfish.levenshtein_distance(unicode(corread), unicode(trueread))
            if distance not in histogram:
                histogram[distance] = 0
            histogram[distance] += 1


handle = open(corrected_reads2, "rU")
for record in SeqIO.parse(handle, "fastq"):
    if True:
        if record.id in gt2dict:
            corread = record.seq.tostring()
            origread, trueread = gt2dict[record.id]
            distance = jellyfish.levenshtein_distance(unicode(corread), unicode(trueread))
            if distance not in histogram:
                histogram[distance] = 0
            histogram[distance] += 1




handle.close()


hist = []
for key in sorted(histogram.keys()):
    hist.append("%s:%s" % (key, histogram[key]))

print " ".join(hist)




