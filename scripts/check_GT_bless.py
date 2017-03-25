

from Bio import SeqIO
import sys


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



corrected = 0
remained = 0
undercorrected = 0
overcorrected = 0

handle = open(corrected_reads1, "rU")
for record in SeqIO.parse(handle, "fastq"):
    if True:
        if record.id in gt1dict:
            corread = record.seq.tostring()
            origread, trueread = gt1dict[record.id]
            if corread == trueread:
                if origread == trueread:
                    remained += 1
                else:
                    corrected += 1
            else:
                if trueread == origread:
                    overcorrected += 1
                else:
                    undercorrected += 1


handle = open(corrected_reads2, "rU")
for record in SeqIO.parse(handle, "fastq"):
    if True:
        if record.id in gt2dict:
            corread = record.seq.tostring()
            origread, trueread = gt2dict[record.id]
            if corread == trueread:
                if origread == trueread:
                    remained += 1
                else:
                    corrected += 1
            else:
                if trueread == origread:
                    overcorrected += 1
                else:
                    undercorrected += 1

handle.close()




sumall = float(corrected + remained + undercorrected + overcorrected)

print "corrected:", corrected, corrected / sumall
print "remained:", remained, remained / sumall
print "undercorrected:", undercorrected, undercorrected / sumall
print "overcorrected:", overcorrected, overcorrected / sumall







