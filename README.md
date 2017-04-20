# Introduction

This project includes simulated and 'golden standard' datasets, software and scripts that we used to benchmark  error correction tools in our study  : Comprehensive benchmarking of error correction methods for next generation sequencing via unique molecular identifiers


# Golden standard data 

We have used simulated and experimentally obtained ‘golden standard’ data from human and Human Immunodeficiency Virus (HIV) virus. We used datasets threee experimentally obtained datasets (T1, T2, T3) and three simulated datasets (S1, S2, S3) to becnmark error corretions algorithms. 

### T1 : reads derived from human genomic DNA data

We use genome in a bottle data (GIAB, http://jimb.stanford.edu/giab/). The data was derived from 

composed of high-quality variant calls


The raw data is here

ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/


Some discussion here
https://www.biostars.org/p/239598/

Paragraph from the paper 

These data and other data sets for NA12878 are available at the Genome in a Bottle ftp site at NCBI (ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878) and are described on a spreadsheet at http://genomeinabottle.org/blog-entry/existing-and-future-na12878-datasets. In addition, the results of this work (high-confidence variant calls and BED files describing confident regions) are available at ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/variant_calls/NIST along with a README.NIST describing the files and how to use them. T


We downloaded raw paired-end reads from http://www.ebi.ac.uk/ena/data/view/PRJNA162355. 
Ground true (high-quality variant calls) was downloaded from ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/NA12878_HG001/NISTv3.3.2/GRCh38/



## Reads derived from human genomic DNA data (T2,S2)

We have also used publically available TCR-Seq data with attached 12bp UMIs from 10 chronic HIV patients (SRP045430). 

Data obtaine from : Best, Katharine, et al. "Dynamic perturbations of the T-cell receptor repertoire in chronic HIV infection and following antiretroviral therapy." Frontiers in immunology 6 (2016): 644.


## Reads derived from human genomic DNA data (in-house) (T3,S3)

We used the UMI-based high-fidelity sequencing protocol (also known as safe-SeqS) to eliminate errors from the sequencing data. Full description of high-fidelity sequencing protocol is provided in Mangul, Serghei, et al. "Accurate viral population assembly from ultra-deep sequencing data." Bioinformatics 30.12 (2014): i329-i337.

We have used in-house sequencing data derived from 3.4 kb region of Human Immunodeficiency Virus (HIV) spanning the Gag/Pol genes.  The data consist of 107 millions 2x100bp reads with attached 13bp UMIs.  Applying high-fidelity protocol resulted in 3.1 million reads used to evaluate error correction algorithms (Golden Dataset 1: GD1). 



| Command | Description |
| --- | --- |
| git status | List all new or modified files |
| git diff | Show file differences that haven't been staged |
