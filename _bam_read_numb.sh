#!/usr/bin/bash

bam=$1
samtools=/home/eaststar0/miniconda3/bin/samtools
$samtools view -c -F 4 $bam > ${bam}.readnumb.txt



