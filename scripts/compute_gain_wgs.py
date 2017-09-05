
read1 = sys.argv[1]
read2 = sys.argv[2]
true1 = sys.argv[3]
true2 = sys.argv[4]
snpfile = sys.argv[5]


r1dict = {}
for r1 in SeqIO.parse(read1, "fastq"):
    r1dict[r1.id[:-2]] = str(r1.seq)

r2dict = {}
for r2 in SeqIO.parse(read2, "fastq"):
    r2dict[r2.id[:-2]] = str(r2.seq)


t1dict = {}
for t1 in SeqIO.parse(true1, "fastq"):
    t1dict[t1.id[:-2]] = str(t1.seq)

t2dict = {}
for t2 in SeqIO.parse(true2, "fastq"):
    t2dict[t2.id[:-2]] = str(t2.seq)





def reverse_complement(sequence):
    basepairs = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}
    reversed_sequence = (sequence[::-1])
    rc = ''.join([basepairs.get(reversed_sequence[i], 'X') for i in range(len(sequence))])
    return rc



record = SeqIO.parse(reference, "fasta").next()
refseq = str(record.seq)



with open(snpfile) as f:
    snps = f.readlines()

snps = map(lambda x: x.strip().split(), snps)

# every snp looks like this: 1       22535   A       R       +

snpdict = {}
for x in snps:
    snpdict[int(x[1])] = []
    if x[3] in ['A', 'C', 'G', 'T']:
        snpdict[int(x[1])].append(x[3])
    elif x[3] == 'R':
        snpdict[int(x[1])].extend(['A', 'G'])
    elif x[3] == 'Y':
        snpdict[int(x[1])].extend(['C', 'T'])
    elif x[3] == 'S':
        snpdict[int(x[1])].extend(['G', 'C'])
    elif x[3] == 'W':
        snpdict[int(x[1])].extend(['A', 'T'])
    elif x[3] == 'K':
        snpdict[int(x[1])].extend(['G', 'T'])
    elif x[3] == 'M':
        snpdict[int(x[1])].extend(['A', 'C'])
    elif x[3] == 'B':
        snpdict[int(x[1])].extend(['C', 'G', 'T'])
    elif x[3] == 'D':
        snpdict[int(x[1])].extend(['A', 'G', 'T'])
    elif x[3] == 'H':
        snpdict[int(x[1])].extend(['A', 'C', 'T'])
    elif x[3] == 'V':
        snpdict[int(x[1])].extend(['A', 'C', 'G'])
    elif x[3] == 'N':
        snpdict[int(x[1])].extend(['A', 'C', 'T', 'G'])


# the most interesting stuff

errors_before_ec = set()
for r1, seq in t1dict.items():
    seq2 = t2dict.get(r1, "")

    coords = map(int, r1.split("_")[1:3])
    refpiece = refseq[coords[0] - 1: coords[1]]
    piece1 = refpiece[:len(seq)]
    piece2 = refpiece[-len(seq):]

    seqr = reverse_complement(seq)
    score1 = score2 = score3 = score4 = 0
    for i in range(20):
        if piece1[i] == seq[i]:
            score1 += 1
        if piece2[i - 20 + 1] == seqr[i - 20 + 1]:
            score4 += 1
    maxscore = max(score1, score4)
    if maxscore == score1:
        read1, read2 = seq, reverse_complement(seq2) 
        # read1 is paired with seq
        coord1 = coords[0]
        for u, v in zip(read1, piece1):
            if u != v:
                if not (coord1 in snpdict and u in snpdict[coord1]):
                    errors_after_ec.add("%s:%s" % (r1, coord1))
            coord1 += 1
        coord2 = coords[1] - len(seq) + 1
        for u, v in zip(read2, piece2):
            if u != v:
                if not (coord2 in snpdict and u in snpdict[coord2]):
                    errors_after_ec.add("%s:%s" % (r1, coord2))
            coord2 += 1
    elif maxscore == score4:
        read1, read2 = seq2, seqr
        coord1 = coords[0]
        for u, v in zip(read1, piece1):
            if u != v:
                if not (coord1 in snpdict and u in snpdict[coord1]):
                    errors_after_ec.add("%s:%s" % (r1, coord1))
            coord1 += 1
        coord2 = coords[1] - len(seq) + 1
        for u, v in zip(read2, piece2):
            if u != v:
                if not (coord2 in snpdict and u in snpdict[coord2]):
                    errors_after_ec.add("%s:%s" % (r1, coord2))
            coord2 += 1
       
    if r1 in t2dict:
        del t2dict[r1]
    if r1 in t1dict:
        del t1dict[r1]




errors_after_ec = set()
for r1, seq in r1dict.items():
    seq2 = r2dict.get(r1, "")

    coords = map(int, r1.split("_")[1:3])
    #refpiece = refseq[coords[0] - 1: coords[1]]
    piece1 = t1dict[r1] #refpiece[:len(seq)]
    piece2 = t2dict[r1] #refpiece[-len(seq):]

    seqr = reverse_complement(seq)
    score1 = score2 = score3 = score4 = 0
    for i in range(20):
        if piece1[i] == seq[i]:
            score1 += 1
        if piece2[i - 20 + 1] == seqr[i - 20 + 1]:
            score4 += 1
    maxscore = max(score1, score4)
    if maxscore == score1:
        read1, read2 = seq, reverse_complement(seq2) 
        # read1 is paired with seq
        coord1 = coords[0]
        for u, v in zip(read1, piece1):
            if u != v:
                if not (coord1 in snpdict and u in snpdict[coord1]):
                    errors_after_ec.add("%s:%s" % (r1, coord1))
            coord1 += 1
        coord2 = coords[1] - len(seq) + 1
        for u, v in zip(read2, piece2):
            if u != v:
                if not (coord2 in snpdict and u in snpdict[coord2]):
                    errors_after_ec.add("%s:%s" % (r1, coord2))
            coord2 += 1
    elif maxscore == score4:
        read1, read2 = seq2, seqr
        coord1 = coords[0]
        for u, v in zip(read1, piece1):
            if u != v:
                if not (coord1 in snpdict and u in snpdict[coord1]):
                    errors_after_ec.add("%s:%s" % (r1, coord1))
            coord1 += 1
        coord2 = coords[1] - len(seq) + 1
        for u, v in zip(read2, piece2):
            if u != v:
                if not (coord2 in snpdict and u in snpdict[coord2]):
                    errors_after_ec.add("%s:%s" % (r1, coord2))
            coord2 += 1
       
    
    if r1 in r2dict:
        del r2dict[r1]
    if r1 in r1dict:
        del r1dict[r1]




print len(errors_before_ec)
print len(errors_after_ec)

print len(errors_before_ec & errors_after_ec)

#TP = errors_before_ec & errors_after_ec
#FP = 
#gain = (TP − FP)/(TP + FN)


