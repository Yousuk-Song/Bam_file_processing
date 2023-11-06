#!/data2/home/song7602/miniconda3/bin/python3.11

import sys
import os

bam = sys.argv[1]

thread = 20

gatk = '/data2/home/song7602/1.Scripts/gatk-4.2.6.1/gatk'
def sort(bam, thread):
	sorted_bam = bam.replace('.bam', '.sort.bam')
	sort_command = ['samtools', 'sort', '-@', str(thread), bam, '-o', sorted_bam]	
	os.system(' '.join(sort_command))

def index(bam, thread):
	index_command = ['samtools', 'index', '-@', str(thread), bam]
	os.system(' '.join(index_command))

def markdup(bam):
	markdup_command = [gatk, 'MarkDuplicates', '-I', bam, '-O', bam.replace('.sort.bam', '.dedupped.bam'), '--METRICS_FILE', bam.replace('.sort.bam', '_metrics.txt'), '--REMOVE_DUPLICATES true']
	os.system(' '.join(markdup_command))

#index(bam, thread)
#sort(bam, thread)

sorted_bam = bam.replace('.bam', '.sort.bam')

#index(sorted_bam, thread)

markdup(sorted_bam)

dedup_bam = sorted_bam.replace('.sort.bam', '.dedupped.bam')

index(dedup_bam, thread)


