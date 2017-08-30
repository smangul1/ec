import pysam
import argparse
import csv
import sys
import copy



# Explanation of MD tag : https://github.com/vsbuffalo/devnotes/wiki/The-MD-Tag-in-BAM-Files



def compare(gold_list,list ):

    print gold_list, list

ap = argparse.ArgumentParser()
ap.add_argument('inCRAM', help='Mapped reads in cram format')
ap.add_argument('chr', help='chr')
ap.add_argument('out', help='chr')
ap.add_argument('wesFile', help='file with gold standard define by WES sample')


args = ap.parse_args()


pSet=set()
gold={}

with open (args.wesFile) as csvfile:
    readCSV=csv.reader(csvfile)
    for line in readCSV:
        pos=int(line[1])
        pSet.add(pos)
        gold[pos]=line


print "Number of gold SNPs from WES", len(pSet)



samfile = pysam.AlignmentFile(args.inCRAM, "rc" )



file=open(args.out,"w")








for pileupcolumn in samfile.pileup(args.chr):
    
        pos=pileupcolumn.pos

        alleles=[]
        alleles[:]=[]
        alleles=[0,0,0,0]
    
    

        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                
                
                #print ('\tbase in read %s = %s' %(pileupread.alignment.query_name,pileupread.alignment.query_sequence[pileupread.query_position]))
                
                
                
                        base=pileupread.alignment.query_sequence[pileupread.query_position]
                        if base=='A':
                            alleles[0]+=1
                        elif base=='C':
                            alleles[1]+=1
                        elif base=='T':
                            alleles[2]+=1
                        elif base=='G':
                            alleles[3]+=1
                
        #print ("\ncoverage at base %s = %s" %(pileupcolumn.pos, pileupcolumn.n))
        if pos in pSet:
            print ("\ncoverage at base %s = %s" %(pileupcolumn.pos, pileupcolumn.n))
            print alleles
            print gold[pileupcolumn.pos ]
            compare(gold[pileupcolumn.pos ],alleles)


samfile.close()
