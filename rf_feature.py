# -*- encoding:utf-8 -*-
import sys

class FeatureEngineer:

	def __init__(self):
		pass
	
	@classmethod
	def extract_feature(self):
		if len(sys.argv) < 3:
			print 'Usge: python feature.py [data_path:./data/train/] [train for test]'
			return
		path = sys.argv[1]
		feature_raw = {}
		book_type_dit = {}
		st = {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}}
		# load book type
		with open(path + "book_type.txt") as f:
			f.readline()
			for line in f:
				data = line.strip().split('\t')
				book_type_dit[data[0]] = data[1]

		# read book txt
		with open(path + "book.txt") as f:
			f.readline()
			for line in f:
				semester, stu_id, book_id = line.strip().split('\t')[:-1]
				if stu_id not in feature_raw:
					feature_raw[stu_id] = {'1' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'2' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'3' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}}}
				feature_raw[stu_id][semester]['books'][book_id] = book_type_dit[book_id] \
					if book_id in book_type_dit else '0'
	
		# read lib txt
		with open(path + "lib.txt") as f:
			f.readline()
			for line in f:
				semester, stu_id = line.strip().split('\t')[:2]
				if stu_id not in feature_raw:
					feature_raw[stu_id] = {'1' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'2' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'3' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}}}
				feature_raw[stu_id][semester]['enter_lib_cnt'] += 1

		# read comsume txt
		with open(path + "comsume.txt") as f:
			f.readline()
			for line in f:
				semester, stu_id, address,day,minute, price = line.strip().split('\t')
				if stu_id not in feature_raw:
					feature_raw[stu_id] = {'1' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'2' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'3' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}}}
				if address not in feature_raw[stu_id][semester]['comsume_address']:
					feature_raw[stu_id][semester]['comsume_address'][address] = 0
				feature_raw[stu_id][semester]['comsume_cnt'] += 1
				feature_raw[stu_id][semester]['comsume_credit'] += float(price)
		
		# read gpa txt
		with open(path + "gpa.txt") as f:
			f.readline()
			for line in f:
				semester, stu_id, gpa = line.strip().split('\t')
				if stu_id not in feature_raw:
					feature_raw[stu_id] = {'1' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'2' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}},
						'3' : {'books' : {},'gpa' : 0, 'enter_lib_cnt' : 0, 'comsume_cnt' : 0, 'comsume_credit' : 0,'comsume_address' : {}}}
				feature_raw[stu_id][semester]['gpa'] = int(gpa)
		
		

		# gather the feature
		feature_list = []
		P = 21
		max_values = [0] * P
		
		for stu_id in feature_raw:
			feat = feature_raw[stu_id]
			temp_feature_list = []
			for sem in ['1', '2', '3']:
				borrow_book_cnt = len(feat[sem]['books'].keys())
				borrow_book_type_cnt = len(set([i[1] for i in feat[sem]['books'].items()]))
				enter_lib_cnt = feat[sem]['enter_lib_cnt']
				comsume_cnt = feat[sem]['comsume_cnt']
				comsume_credit = feat[sem]['comsume_credit']
				comsume_address_cnt = len(feat[sem]['comsume_address'])
				gpa = feat[sem]['gpa']
				temp_feature_list.append(borrow_book_cnt)
				temp_feature_list.append(borrow_book_type_cnt)
				temp_feature_list.append(enter_lib_cnt)
				temp_feature_list.append(comsume_cnt)
				temp_feature_list.append(comsume_credit)
				temp_feature_list.append(comsume_address_cnt)
				temp_feature_list.append(gpa)
			
			if "test" in sys.argv[2]:
				temp_feature_list[20] = int(stu_id)
			
			if "sig" in sys.argv[2]:
				temp_feature_list.append(int(stu_id))

			for idx in range(P):
				max_values[idx] = max(max_values[idx], temp_feature_list[idx])
			feature_list.append(temp_feature_list)
		features = feature_list
		"""
		for lit in feature_list:
			lt = [0] * 21
			for i in range(21):
				if i != 6 and i != 13 and i != 20:
					lt[i] = 1.0 * lit[i] / max_values[i] if max_values[i] != 0 else lit[i]
				else:
					lt[i] = lit[i]
			features.append(lt)
		print max_values
		"""
		features.sort(lambda x,y : cmp(x[P-1], y[P-1]))
		f = open(sys.argv[2] + "_feature", "w")
		for lit in features:
			f.write('\t'.join([str(i) for i in lit]))
			f.write('\n')
		f.close()

if __name__ == '__main__':
	FeatureEngineer.extract_feature()
