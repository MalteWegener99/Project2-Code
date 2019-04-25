from graphing import parse_binary_llh
import numpy as np
import sys
import datetime
import glob
import os
from matplotlib import pyplot as plt
from math import degrees as deg





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


	return data

if __name__ == "__main__":
	path = "C:\\Users\\Wim Jodehl\\Desktop\\TAaS\\Project2-Code\\conv"
	os.chdir(path)

	collection = parse_binary_llh(path + "\\KUAL.tseries.neu")
	series = sorted(collection,key = lambda x: x.time)

	locations,times = [],[]
	init_time = series[0].time
	init_year = init_time//1000
	init_days = init_time - init_year*1000
	init_date = datetime.date.fromordinal(datetime.date(init_year,1,1).toordinal()+ init_days - 1)

	for i in range(len(series)):

		ts = series[i].time
		year = ts//1000
		days = ts - year*1000
		date = datetime.date.fromordinal(datetime.date(year,1,1).toordinal()+ days - 1)
		time = (date - init_date).total_seconds()
		times.append(time)
		locations.append(deg(series[i].pos[2]))

	data = np.column_stack((times,locations))

	newdata = outlierdet(data,300,1)
	# inl_x, inl_y, outl_x, outl_y = outlierdet(times,locations,0.45)
	plt.subplot(2,1,1)
	plt.scatter(times,locations,s = 0.1)
	plt.ylim(min(locations),max(locations))
	# plt.scatter(times,d_ave)
	plt.subplot(2,1,2)
	plt.scatter(newdata[:,0],newdata[:,1],s = 0.4)
	plt.ylim(min(newdata[:,1]),max(newdata[:,1]))


	# plt.autoscale(enable=True,axis = "y",tight=True)
	plt.show()