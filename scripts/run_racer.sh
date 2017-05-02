#!/bin/bash

# Kevin Hsieh
# 27 April 2017

RACER_DIR="$HOME/project/tools/racer_program"
DATA_DIR="/u/home/n/ngcrawfo/project-zarlab/igor/imrep_revision/data/simulation/IGH/"
GENOME_SIZE="405000"

mkdir data racer_output
find $DATA_DIR -maxdepth 1 | grep fastq | xargs cp -t data
for filename in `ls data`; do
	echo --------------------------------------------------------------------------------
	echo Running $filename
	echo --------------------------------------------------------------------------------
	prefix=`echo $filename | sed 's \.[^.]*$  '`
	$RACER_DIR/RACER data/$filename racer_output/${prefix}_corrected.fastq $GENOME_SIZE
done
