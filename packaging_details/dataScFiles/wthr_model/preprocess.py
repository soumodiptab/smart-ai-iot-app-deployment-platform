import numpy as np

def preprocess(data):
	perc = data['perc']
	temp_max = data['temp_max']
	l = [perc,temp_max]
	l[0] = np.sqrt(l[0])
	
	return [l]
	