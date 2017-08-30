import pysam
import argparse
import csv
import sys
import copy



# Explanation of MD tag : https://github.com/vsbuffalo/devnotes/wiki/The-MD-Tag-in-BAM-Files



ap = argparse.ArgumentParser()
ap.add_argument('inCRAM', help='Mapped reads in cram format')
ap.add_argument('chr', help='chr')
ap.add_argument('out', help='chr')

args = ap.parse_args()


samfile = pysam.AlignmentFile(args.inCRAM, "rc" )



file=open(args.out,"w")

for pileupcolumn in samfile.pileup(args.chr):
    


    
    
    if pileupcolumn.n>10:
        
        alleles=[]
        alleles[:]=[]
        alleles=[0,0,0,0]
        
    
        print ("\ncoverage at base %s = %s" %(pileupcolumn.pos, pileupcolumn.n))
        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                # query position is None if is_del or is_refskip is set.
                #print ('\tbase in read %s = %s' %(pileupread.alignment.query_name,pileupread.alignment.query_sequence[pileupread.query_position]))
                
                
                
                
                ed=int(pileupread.alignment.get_tag("NM"))
                
                mq=pileupread.alignment.mapping_quality
                cigar=pileupread.alignment.cigarstring
                
                
                
                #If a read has more than INT hits, the XA tag will not be written.
                if pileupread.alignment.has_tag("XA"):
                    alternativeA=pileupread.alignment.get_tag("XA")
                    
                    ed2=int(alternativeA.split(";")[0].split(",")[3])
                    
                    if ed<ed2:
                
                
                
                        base=pileupread.alignment.query_sequence[pileupread.query_position]
                        if base=='A':
                            alleles[0]+=1
                        elif base=='C':
                            alleles[1]+=1
                        elif base=='T':
                            alleles[2]+=1
                        elif base=='G':
                            alleles[3]+=1
                
                
        if alleles.count(0)==3:
            if max(alleles)>10:
                print alleles
                file.write("homo,"+ str(pileupcolumn.pos)+","+str(alleles[0])+","+str(alleles[1])+","+str(alleles[2])+","+str(alleles[3]))
                file.write("\n")
        
        
        if alleles.count(0)==2:
            new_list = copy.copy(alleles)
            new_list.sort()
            
            
            
            if new_list[2]>10 and new_list[3]>10:
                file.write("het,"+ str(pileupcolumn.pos)+","+str(alleles[0])+","+str(alleles[1])+","+str(alleles[2])+","+str(alleles[3]))
                file.write("\n")



samfile.close()
