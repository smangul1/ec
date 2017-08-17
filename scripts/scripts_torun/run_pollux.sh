#!/bin/bash

#Russell Littman
#16 August 2017

POLLUX_DIR="/u/home/n/ngcrawfo/project-zarlab/igor/VIRAL_CORRECTION/tools/pollux"

#!/bin/bash

source $(dirname $0)/argparse.bash || exit 1
argparse "$@" <<EOF || exit 1
parser.add_argument('infile_1')
parser.add_argument('infile_2')
parser.add_argument('kmer')

parser.add_argument('outfile')
#parser.add_argument('-a', '--the-answer', default=42, type=int,help='Pick a number [default %(default)s]')

EOF

echo required infile: "$INFILE_1"
echo required infile: "$INFILE_2"
echo required infile: "$KMER"
echo required outfile: "$OUTFILE"

base=$(echo $INFILE_1 | awk -F "_" '{print $1}')


out_dir=${base}_dir




$POLLUX_DIR/pollux -i $INFILE_1  $INFILE_2 -p -o $out_dir -k $KMER




cat $out_dir/${INFILE_1}.corrected $out_dir/${INFILE_2}.corrected >$OUTFILE


