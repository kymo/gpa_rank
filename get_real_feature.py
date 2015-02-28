# -*- encoding:utf8 -*-
# get the pair-wise features
import sys


data_set = []

with open(sys.argv[1], "r") as f:
	for line in f:
		data = [float(i) for i in line.strip().split('\t')]
		data_set.append(data)

positive_feature = []
negative_feature = []
lens = len(data_set)


for i in range(lens - 1):	
	for j in range(i + 1, lens):
		tem_feature = []
		for k in range(20):
			if data_set[i][k] > data_set[j][k]:
				tem_feature.append('1')
			else:
				tem_feature.append('0')
		tem_feature.append('1')
		print '\t'.join(tem_feature)
		tem_feature = []
		for k in range(20):
			if data_set[i][k] > data_set[j][k]:
				tem_feature.append('0')
			else:
				tem_feature.append('1')
		tem_feature.append('0')
		print '\t'.join(tem_feature)
