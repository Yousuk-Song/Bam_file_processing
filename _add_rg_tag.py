#!/data2/home/song7602/miniconda3/bin/python3.11

import sys
import os

gatk = '/data2/home/song7602/1.Scripts/gatk-4.2.6.1/gatk'

bam = sys.argv[1]
name = sys.argv[2]

rg_bam = bam.replace('.bam', '.rg.bam')

os.system(f'{gatk} AddOrReplaceReadGroups -I {bam} -O {rg_bam} --RGSM {name} --RGLB {name} --RGPL ILLUMINA --RGPU {name}')


