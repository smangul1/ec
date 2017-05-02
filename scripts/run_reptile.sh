#!/bin/bash

# Kevin Hsieh
# 27 April 2017

REPTILE_DIR="$HOME/project/tools/reptile-v1.1"
DATA_DIR="/u/home/n/ngcrawfo/project-zarlab/igor/imrep_revision/data/simulation/IGH/"

# Step 1
echo --------------------------------------------------------------------------------
echo Preprocessing
echo --------------------------------------------------------------------------------
mkdir data_separated reptile_output
perl $REPTILE_DIR/utils/fastq-converter-v2.0.pl $DATA_DIR data_separated/ 1

for filename in `ls data_separated | grep '\.fa$'`; do
	echo --------------------------------------------------------------------------------
	echo Running $filename
	echo --------------------------------------------------------------------------------
	prefix=`echo $filename | sed 's \.[^.]*$  '`
	
	# Step 2
	echo "IFlag                   1
BatchSize               1000000
InFaFile                data_separated/$prefix.fa
IQFile                  data_separated/$prefix.q
KmerLen                 24
OKmerHistFile           data_separated/$prefix.kmerhist
QHistFile               data_separated/$prefix.qualhist
OKmerCntFile    
MaxErrRate              0.02
QThreshold              73
MaxBadQPerKmer          4
QFlag                   1" >seq-analy-config
	$REPTILE_DIR/utils/seq-analy/seq-analy seq-analy-config
	QThreshold=`python reptile_extract_param.py QThreshold data_separated/$prefix.qualhist`
	Qlb=`python reptile_extract_param.py Qlb data_separated/$prefix.qualhist`
	rm seq-analy-config
	find data_separated | grep hist | xargs rm
	
	# Step 3 (changed: MaxBadQPerKmer)
	echo "IFlag                   1
BatchSize               1000000
InFaFile                data_separated/$prefix.fa
IQFile                  data_separated/$prefix.q
KmerLen                 24
OKmerHistFile           data_separated/$prefix.kmerhist
QHistFile               data_separated/$prefix.qualhist
OKmerCntFile    
MaxErrRate              0.02
QThreshold              $QThreshold
MaxBadQPerKmer          6
QFlag                   1" >seq-analy-config
	$REPTILE_DIR/utils/seq-analy/seq-analy seq-analy-config
	T_expGoodCnt=`python reptile_extract_param.py T_expGoodCnt data_separated/$prefix.kmerhist`
	T_card=`python reptile_extract_param.py T_card data_separated/$prefix.kmerhist`
	rm seq-analy-config
	find data_separated | grep hist | xargs rm
	
	# Step 4 (changed: KmerLen, Step, MaxBadQPerKmer)
	echo "InFaFile                data_separated/$prefix.fa
QFlag                   1
IQFile                  data_separated/$prefix.q
OErrFile                reptile_output/$prefix.errors
BatchSize               1000000 
KmerLen                 16
hd_max                  1
Step                    8
ExpectSearch            16 
T_ratio                 0.5

######## The following parameters need to be tuned to specific dataset ########

QThreshold              $QThreshold
MaxBadQPerKmer          6
Qlb                     $Qlb
T_expGoodCnt            $T_expGoodCnt
T_card                  $T_card" >reptile-config
	$REPTILE_DIR/src/reptile-v1.1 reptile-config
	rm reptile-config
	
	# Step 5
	$REPTILE_DIR/utils/reptile_merger/reptile_merger data_separated/$prefix.fa \
		reptile_output/$prefix.errors reptile_output/${prefix}_corrected.fa
done
