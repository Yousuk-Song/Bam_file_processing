#!/usr/bin/bash

bam=$1
gatk=/data2/home/song7602/1.Scripts/gatk-4.2.6.1/gatk
$gatk BamIndexStats I=$bam >${bam}.stat

