import numpy as np
import sys
import datetime
import glob
import os
from matplotlib import pyplot as plt
from math import degrees as deg
from sklearn.covariance import EllipticEnvelope





def outlierdet(data,n,sl):
	
	d = data[:,1]

	avg_mask = np.ones(n)/n
	d_ave = np.convolve(d,avg_mask,mode = "same")


	diff = []

	for j in range(n//2,len(data[:,1]) - n//2):
		diff.append(abs(d_ave[j] - d[j]))

	sdev = np.std(diff)
	count = 0

	for i in range(n//2,len(data[:,1]) - n//2):
		if abs(d_ave[i] - d[i]) > (sl * sdev):
			data = np.delete(data,(i - count), axis = 0)
			count += 1

		# if (i+1) == len(data[:,1]):
		# 	break




	return data
