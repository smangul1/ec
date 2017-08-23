#!/bin/bash

AUTHOR="imandric1"



################################################################
##########          The main template script          ##########
################################################################

toolName="pollux"
toolPath="/u/home/n/ngcrawfo/project-zarlab/igor/VIRAL_CORRECTION/tools/pollux/pollux"

compressScript="/u/home/i/imandric/project-zarlab/ErrorCorrection/scripts/compress.py"

# STEPS OF THE SCRIPT
# 1) prepare input if necessary
# 2) run the tool
# 3) transform output if necessary
# 4) compress output
# 5) send the output to the designated directory
# 6) remove temporary files


# THE COMMAND LINE INTERFACE OF THE WRAPPER SCRIPT
# $tool $input1 $input2 $outdir $kmers $others
# |      mandatory part       | | extra part |
# <---------------------------> <------------>




if [ $# -lt 5 ]
then
echo "********************************************************************"
echo "Script was written for project : Best practices for  conducting benchmarking in the most comprehensive and reproducible way"
echo "This script was written by Igor Mandric"
echo "********************************************************************"
echo ""
echo "1 <input1>  - _1.fastq "
echo "2 <input2> - _2.fastq"
echo "3 <tmpdir - dir to save the intermediate output"
echo "4 <outdir - dir to save the output"
echo "5 <kmer> - kmer length"
echo "--------------------------------------"
exit 1
fi



# mandatory part
input1=$1
input2=$2
tmpdir=$3
outdir=$4

# extra part (tool specific)
kmer=$5





# STEP 1 - prepare input if necessary (ATTENTION: TOOL SPECIFIC PART!)


# -----------------------------------





# STEP 2 - run the tool (ATTENTION: TOOL SPECIFIC PART!)

wdir=${tmpdir}/$toolName-$( date +%Y-%m-%d-%H-%M-%S )

#run the command (in a temporary directory)
$toolPath -i $input1 $input2 -p -o $wdir -k $kmer

# ---------------------




# STEP 3 - transform output if necessary (ATTENTION: TOOL SPECIFIC PART!)

cat $wdir/input_1.fastq.corrected $wdir/input_2.fastq.corrected | gunzip - > $wdir/${toolName}.corrected.fastq.gz
rm $wdir/input_1.fastq.corrected
rm $wdir/input_2.fastq.corrected

# --------------------------------------





# STEP 4 - send the output to the designated directory

cp $wdir/${toolName}.corrected.compressed.fastq.gz $outdir

# ----------------------------------------------------



# STEP 5 - remove temporary files

rm -rf $wdir

# -------------------------------


