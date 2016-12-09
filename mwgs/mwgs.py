#/usr/bin/env python
import logging
import sys
from os import path
import glob
import subprocess

from reference_handling import Reference
from get_lims_info import get_reference_id
from align_to_reference import perform_alignment, remove_duplicates
from calculate_metrics import get_insert_size, reads_aligned


class Sample(object):
	def __init__(self, sample_path):
		self.sample_path = sample_path
		self.sample_name = path.basename(path.normpath(sample_path))
		self.sample_ref_nc = get_reference_id(self.sample_name)
		if not self.sample_ref_nc:
			raise ValueError('No reference found in LIMS')
		self.sample_reference = Reference(self.sample_ref_nc)
		self.r1 = glob.glob(sample_path + '/*_1.fastq.gz')
		self.r2 = [x.replace('_1.fastq.gz', '_2.fastq.gz') for x in self.r1]

	def __str__(self):
		return '<Sample {} at {}>'.format(self.sample_path, path.abspath(self.sample_path))

	def run_qc(self):
		prefix = path.join(self.sample_path, self.sample_name)
		self.bamfile, self.dupmetrics = remove_duplicates(perform_alignment(
															prefix,
															self.r1,
															self.r2,
															self.sample_reference.fasta_file))
		self.total_reads, self.mapped_reads = reads_aligned(self.bamfile)
		self.insertmetricsfile, self.inserthistfile = get_insert_size(self.bamfile)
		self.median_insert = self.gather_insert_metrics()
		self.duplication_rate = self.gather_duplication_metrics()
		self.above_10X = self.gather_fraction_above_10X()

	def gather_insert_metrics(self):
		with open(self.insertmetricsfile, 'r') as f:
			l = ''
			while not l.startswith('MEDIAN_INSERT_SIZE'):
					l = f.readline()
			return f.readline().split('\t')[0]

	def gather_duplication_metrics(self):
		with open(self.dupmetrics, 'r') as f:
			l = ''
			while not l.startswith('LIBRARY'):
				l = f.readline()
			return f.readline().split('\t')[-2]


	def gather_fraction_above_10X(self):
		cmd = ['samtools', 'depth', self.bamfile]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		proc_out, proc_error = p.communicate()
		lines = proc_out.decode('utf-8').split('\n')
		bases_below_10 = 0
		for line in lines[:-1]:
			if int(line.split('\t')[2]) < 10:
				bases_below_10 +=1
		return (len(lines) - bases_below_10)/len(lines) 

	def dump_metrics(self):
		with open(path.join(self.sample_path, 'statistics.yml'), 'w') as f:
			f.write('Sample Name : {}\n'.format(self.sample_name))
			f.write('Reference Genome : {}\n'.format(self.sample_ref_nc))
			f.write('Median Insert Size : {}\n'.format(self.median_insert))
			f.write('Duplication Rate : {}\n'.format(self.duplication_rate))
			f.write('Fraction aligned to Reference : {}\n'.format(self.mapped_reads/self.total_reads))
			f.write('Fraction of bases with cov >= 10X : {}\n'.format(self.above_10X) )

if __name__ == '__main__':
	sample_path = sys.argv[1]
	s = Sample(sample_path)
	s.run_qc()
	s.dump_metrics()
