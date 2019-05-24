from Sample import Sample_conv
import datetime
import matplotlib.pyplot as plt
import sys
import matplotlib.dates as mdates
from scipy.stats import linregress
from scipy.optimize import curve_fit
import numpy as np
import math

def parse_date(string):
	year = string[-2:]
	day = string[:2]
	month = string[2:5]
	year, day = day, year
	monthtonum = {
		"JAN": 1,
		"FEB": 2,
		"MAR": 3,
		"APR": 4,
		"MAY": 5,
		"JUN": 6,
		"JUL": 7,
		"AUG": 8,
		"SEP": 9,
		"OCT": 10,
		"NOV": 11,
		"DEC": 12,
	}
	year = int(year)
	if year > 20:
		year += 1900
	else:
		year += 2000
	day = int(day)
	return datetime.datetime(year, monthtonum[month], day)


lat_file = open("newthing/{}.lat".format(sys.argv[1])).readlines()
lon_file = open("newthing/{}.lon".format(sys.argv[1])).readlines()
rad_file = open("newthing/{}.rad".format(sys.argv[1])).readlines()

points = []

for i in range(len(lat_file)):
	lat = float(lat_file[i].split()[1])
	lon = float(lon_file[i].split()[1])
	hei = float(rad_file[i].split()[1])
	dat = lat_file[i].split()[-1]
	s_lat = float(lat_file[i].split()[2])
	s_lon = float(lon_file[i].split()[2])
	s_hei = float(rad_file[i].split()[2])

	points.append(Sample_conv("PHKT", parse_date(dat), [lat,lon,hei], [s_lat,s_lon,s_hei]))

f, axarr = plt.subplots(3, sharex=True)

baseline = points[0].time
split = datetime.datetime(2004,12,26)
splitindex = 0
for i in range(len(points)): 
    if points[i].time < split:
        splitindex = i
    else:
        break

f.suptitle(sys.argv[1])
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')	
print(type(points[0].time))
def to_fit(x, a, b, c, d):
    return a + b*x + c*np.sin(2*math.pi/365 * x + d)

def trend(x, a, b, c):
	return a/x + b*x + c
pr = []
for i in range(1140):
	pr.append(datetime.datetime(2018,12,29)+datetime.timedelta(days = 10*i))
print(datetime.datetime(2018,12,29)+datetime.timedelta(days = 10*5))
print(pr[1])
name = ["East","North","Up"]
for i in range(2):
	predict = linregress([(x.time-points[0].time).days for x in points[:splitindex+1]], [x.pos[i] for x in points[:splitindex+1]])
	p, cov = curve_fit(trend, [(x.time-points[0].time).days for x in points[splitindex+1:]], [x.pos[i] for x in points[splitindex+1:]])
	st = "{}, before:{} $\pm${} mm/year" .format(name[i],round(predict[0]*365,5),round(predict[-1]*365,5))
    #st2 = "{}, after:{} $\pm${} mm/year" .format(name[i],round(p[1]*365,5),round(np.sqrt(np.diag(cov))[1]*365,5))
	axarr[i].axvline(x=datetime.datetime(2004,12,26))
	axarr[i].axhline(y=0, color='k')
	axarr[i].set_xlim([min([x.time for x in points]), max([x.time for x in points])])
	axarr[i].errorbar([x.time for x in points], [x.pos[i] for x in points], yerr=[x.err[i] for x in points], fmt='x', elinewidth=0.1, markersize=0.55)
	#axarr[i].plot([points[0].time, points[-1].time], [predict[1], predict[1]+predict[0]*(points[-1].time-points[0].time).days])
	axarr[i].set_ylabel("Deformation [mm]")
	axarr[i].plot([points[0].time, points[splitindex].time], [predict[1], predict[1]+predict[0]*(points[splitindex].time-points[0].time).days], 'r-',label = st)
	axarr[i].plot([x.time for x in points[splitindex+50:]], [trend((x.time-points[0].time).days, *p) for x in points[splitindex+50:]])
	axarr[i].plot([x for x in pr], [trend((x-points[0].time).days, *p) for x in pr], "b--")
	axarr[i].legend(loc = 3)

for i in range(2,3):
	up, away = curve_fit(to_fit,[(x.time-points[0].time).days for x in points[:splitindex+1]], [x.pos[i] for x in points[:splitindex+1]])
	#print(name[i],"before:",up[1]*365*1000,"mm/year",np.sqrt(np.diag(away))[1]*1000,"mm")
	st = "{}, before:{} $\pm${} mm/year" .format(name[i],round(up[1]*365,5),round(np.sqrt(np.diag(away))[1]*365))
	up2, away = curve_fit(to_fit,[(x.time-points[0].time).days for x in points[splitindex+1:]], [x.pos[i] for x in points[splitindex+1:]])
	#print(name[i],"after:",up2[1]*365*1000,"mm/year",np.sqrt(np.diag(away))[1]*1000,"mm")
	st2 = "{}, after:{} $\pm${} mm/year" .format(name[i],round(up2[1]*365),round(np.sqrt(np.diag(away))[1]*365,5))
	axarr[i].axhline(y=0, color='k')
	axarr[i].set_xlim([min([x.time for x in points]), max([x.time for x in points])])
	axarr[i].axvline(x=datetime.datetime(2004,12,26))
	axarr[i].set_ylabel("Deformation [mm]")
	#axarr[].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
	axarr[i].plot([x.time for x in points[:splitindex+1]], [to_fit((x.time-points[0].time).days, *up) for x in points[:splitindex+1]],label = st)
	axarr[i].plot([x.time for x in points[splitindex+1:]], [to_fit((x.time-points[0].time).days, *up2) for x in points[splitindex+1:]],label = st2)
	axarr[i].errorbar([x.time for x in points], [x.pos[i] for x in points], yerr=[x.err[i] for x in points], fmt='x', elinewidth=0.1, markersize=0.55)
	axarr[i].legend(loc = 3)
plt.show()