

"""
The purpose of this python3 script is to process WGS data and call somatic mutation
Author: Yousuk Song
Last updated date: 2023.08.04
"""

import argparse
import datetime
import os
import sys
import pysam
import time
import multiprocessing as mp

# Dependency PATH
samtools = ''
gatk = ''
picard = ''
bwa = ''
ref = '' # reference_genome.fa ex) /path/to/hg19.fa, /path/to/hg38.fa 

ToolDir = sys.path[0]

def parse_arguments():
	parser = argparse.ArgumentParser(description='Type Normal & Tumor fastq files') 
	required = parser.add_argument_group('required arguments')
	required.add_argument('-n_fq1', '--Normal_Fastq_1',
                              type=str,
                              required=True,
                              help='Normal read1 fastq file')
	required.add_argument('-n_fq2', '--Normal_Fastq_2',
                              type=str,
                              required=True,
                              help='Normal read2 fastq file')
	required.add_argument('-t_fq1', '--Tumor_Fastq_1',
                              type=str,
                              required=True,
                              help='Tumor read1 fastq file')
	required.add_argument('-t_fq2', '--Tumor_Fastq_2',
                              type=str,
                              required=True,
                              help='Tumor read2 fastq file')
	required.add_argument('-name', '--Name',
                              type=str,
                              required=True,
                              help='Sample Name')

	optional = parser.add_argument_group('optional arguments')
	optional.add_argument('-t', '--THREADS',
                              default=4,
                              help='Threads for multi-proecessing')
	args = parser.parse_args()
	return args

def align(fq1, fq2, bam_name, thread, ref, nt, name):
	bwa_command = [bwa, 'mem', '-R', f'"@RG\tID:HWI\tSM:{nt}_{name}\tPL:ILLUMINA"', '-t', str(thread), ref, fq1, fq2, '-o', bam_name]
	os.system(' '.join(bwa_command))

def sort(bam, thread):
	sorted_bam = bam.replace('.bam', 'sort.bam')
	sort_command = [samtools, 'sort', '-@', str(thread), bam, '-o', sorted_bam]
	os.system(' '.join(sort_command))
	
def index(bam, thread):
	index_command = [samtools, 'index', '-@', str(thread), bam]
	os.system(' '.join(index_command))

def markdup(bam):
	markdup_command = [gatk, 'MarkDuplicates', '-I', bam, '-O', bam.replace('.sort.bam', '.dedupped.bam'), '--METRICS_FILE', bam.replace('.sort.bam', '_metrics.txt'), '--REMOVE_DUPLICATES true']
	os.system(' '.join(markdup_command))

def mutect(n_bam, t_bam, name):
	mutect_command = [gatk, 'Mutect2', '-R', ref, '-I', n_bam, '-I', t_bam, '-normal', f'normal_{name}', '-O', bam.replace('.dedupped.bam', '.somatic.vcf')]
	os.system(' '.join(mutect_command))

if __name__ == '__main__':
	args = parse_arguments()
	normal_fq1 = args.Normal_Fastq_1
	normal_fq2 = args.Normal_Fastq_2
	tumor_fq1 = args.Tumor_Fastq_1
	tumor_fq2 = args.Tumor_Fastq_2
	thread = args.THREADS
	name = args.Name

	norm_bam = f'{name}.normal.bam'
	tumor_bam = f'{name}.tumor.bam'

	# align
	process1 = mp.Process(target=align, args=(normal_fq1, normal_fq2, norm_bam, thread, ref, 'normal', name))	
	process2 = mp.Process(target=align, args=(tumor_fq1, tumor_fq2, tumor_bam, thread, ref, 'tumor', name))	
	process1.start()
	process2.start()
	for process in mp.active_children():
		process.join()

	# sort
	process1 = mp.Process(target=sort, args=(norm_bam, thread))       
	process2 = mp.Process(target=sort, args=(tumor_bam, thread)) 
	process1.start()
	process2.start()
	for process in mp.active_children():
		process.join()
	sorted_normal_bam = norm_bam.replace('.bam', 'sort.bam')
	sorted_tumor_bam = tumor_bam.replace('.bam', 'sort.bam')

	# index
	process1 = mp.Process(target=index, args=(sorted_normal_bam, thread))       
	process2 = mp.Process(target=index, args=(sorted_tumor_bam, thread))       
	process1.start()
	process2.start()
	for process in mp.active_children():
		process.join()

	# markdup
	process1 = mp.Process(target=markdup, args=(sorted_normal_bam))
	process2 = mp.Process(target=markdup, args=(sorted_tumor_bam))
	process1.start()
	process2.start()
	for process in mp.active_children():
		process.join()
	dedupped_normal_bam = sorted_normal_bam.replace('.sort.bam', '.dedupped.bam')
	dedupped_tumor_bam = sorted_tumor_bam.replace('.sort.bam', '.dedupped.bam')

	# index
	process1 = mp.Process(target=index, args=(dedupped_normal_bam, thread))
	process2 = mp.Process(target=index, args=(dedupped_tumor_bam, thread))
	process1.start()
	process2.start()
	for process in mp.active_children():
		process.join()

	# mutect
	mutect(dedupped_normal_bam, dedupped_tumor_bam, name)



	








