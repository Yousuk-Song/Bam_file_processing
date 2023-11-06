#!/usr/bin/bash

samtools=/home/eaststar0/miniconda3/bin/samtools
bam=$1
$samtools depth $bam | awk '{sum += $3} END {print "평균 depth:", sum / NR}' > ${bam}.depth.txt



