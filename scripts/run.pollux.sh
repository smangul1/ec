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


# mandatory part
input1=$1
input2=$2
outdir=$3

# extra part (tool specific)
kmer=$4





# STEP 1 - prepare input if necessary (ATTENTION: TOOL SPECIFIC PART!)


# -----------------------------------





# STEP 2 - run the tool (ATTENTION: TOOL SPECIFIC PART!)

wdir=/tmp/$toolName-$( date +%Y-%m-%d-%H-%M-%S )

#run the command (in a temporary directory)
$toolPath -i $input1 $input2 -p -o $wdir -k $kmer

# ---------------------




# STEP 3 - transform output if necessary (ATTENTION: TOOL SPECIFIC PART!)

cat $wdir/input_1.fastq.corrected $wdir/input_2.fastq.corrected > $wdir/${toolName}.corrected.fastq
rm $wdir/input_1.fastq.corrected
rm $wdir/input_2.fastq.corrected

# --------------------------------------





# STEP 4 - compress output

python $compressScript $input1 $input2 $wdir/${toolName}.corrected.fastq $wdir/${toolName}.corrected.compressed.fastq

# ------------------------





# STEP 5 - send the output to the designated directory

cp $wdir/${toolName}.corrected.compressed.fastq $outdir

# ----------------------------------------------------





# STEP 6 - remove temporary files

rm -rf $wdir

# -------------------------------


