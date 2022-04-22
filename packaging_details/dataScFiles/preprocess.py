import numpy as np

def preprocess(l):
	l[0] = np.sqrt(l[0])
	
	return l
	