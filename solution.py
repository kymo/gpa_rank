# encoding:utf8

from factory import ModelFactory

class Solution:

	def __init__(self):
		"""
		self.model = ModelFactory.produce("svm",
				"train_svm_feature",
				"model",
				"test_feature",
				kernel = "rbf",
				max_iter = 100,
				random_seed = 0.3,
				penalty = "l2")
		
		"""
		self.model = ModelFactory.produce("rf",
				"train_real_feature",
				"model",
				"test_feature",
				n_estimators = 250)

	def predict(self, first_f, second_f):
		"""
		tem_feature = first_f
		tem_feature.extend(second_f)
		"""
		tem_feature = []
		for i in range(20):
			if first_f[i] > second_f[i]:
				tem_feature.append(1)
			else:
				tem_feature.append(0)

		return self.model.predict(tem_feature)


	def solve(self):

		# load the feature
		self.model.load_feature()
		
		# train the model
		self.model.train()
		
		# test model
		print "Testing model"
		test_sig_features = []
		with open("sig_feature", "r") as f:
			for line in f:
				test_sig_features.append([float(i) for i in line.strip().split('\t')])
		
		tot_sig = len(test_sig_features)
		
		right = 0.0

		for i in range(tot_sig):
			for j in range(i + 1, tot_sig):
				if self.predict(test_sig_features[i][:-2], test_sig_features[j][:-2]) < 0.5:
					if test_sig_features[i][20] < test_sig_features[j][20]:
						right += 1
					test_sig_features[i], test_sig_features[j] = test_sig_features[j], test_sig_features[i]
				elif test_sig_features[i][20] > test_sig_features[j][20]:
					right += 1
		print right, tot_sig * tot_sig / 2.0, right * 1.0 * 2.0 / (tot_sig * tot_sig)

		tot_up = 0.0
		for i in range(tot_sig):
			#print i + 1, test_sig_features[i][20], test_sig_features[i][21]
			tot_up += (i + 1 - test_sig_features[i][20]) ** 2
		n = tot_sig

		# load test feature
		test_features = []
		with open("test_feature", "r") as f:
			for line in f:
				test_features.append([float(i) for i in line.strip().split('\t')])
		
		# rank
		
		for i in range(0, 91):
			for j in range(i + 1, 91):
				if self.predict(test_features[i][:-1], test_features[j][:-1]) < 0.5:
					test_features[i], test_features[j] = test_features[j], test_features[i]
		
		# output the outcome
		id_ranks = {}
		
		print 'id,rank'
		
		for j in range(91):
			id_ranks[test_features[j][-1]] = j + 1
		out = open("out.csv", "w")
		out.write('id,rank\n')
		for id in range(1, 92):
			out.write(str(id) + ',' + str(id_ranks[id]))
			out.write('\n')

