
# -*- encoding:utf -*-

from model import RandomForestModel
from model import GBDTModel
from model import SVMModel


class ModelFactory(object):
	""" model factory """
	
	__instance = None

	def __init__(self):
		pass

	def __new__(cls, *args, **kwargs):
		if cls.__instance == None:
			cls.__instance = super(ModelFactory, cls).__new__(cls, *args, **kwargs)
		return cls.__instance

	@classmethod
	def produce(self, model_name, *path, **argv):
		if model_name == "svm":
			return SVMModel(*path, **argv)
			#urn SvmModel(path, argv)
		elif model_name == "rf":	
			return RandomForestModel(*path, **argv)

		elif model_name == "gbdt":
			pass
			#return GBDTModel(path, argv)

