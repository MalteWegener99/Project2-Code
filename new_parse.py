from Sample import Sample_conv
import datetime
import matplotlib.pyplot as plt
import sys
import matplotlib.dates as mdates
from scipy.stats import linregress

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
	print(lat)
	lon = float(lon_file[i].split()[1])
	hei = float(rad_file[i].split()[1])
	dat = lat_file[i].split()[-1]
	s_lat = float(lat_file[i].split()[2])
	s_lon = float(lon_file[i].split()[2])
	s_hei = float(rad_file[i].split()[2])

	points.append(Sample_conv("PHUK", parse_date(dat), [lat,lon,hei], [s_lat,s_lon,s_hei]))


f, axarr = plt.subplots(3, sharex=True)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')	
print(type(points[0].time))

for i in range(3):
	predict = linregress([(x.time-points[0].time).days for x in points], [x.pos[i] for x in points])
	axarr[i].axhline(y=0, color='k')
	axarr[i].set_xlim([min([x.time for x in points]), max([x.time for x in points])])
	axarr[i].errorbar([x.time for x in points], [x.pos[i] for x in points], yerr=[x.err[i] for x in points], fmt='x', elinewidth=0.1, markersize=0.55)
	axarr[i].plot([points[0].time, points[-1].time], [predict[1], predict[1]+predict[0]*(points[-1].time-points[0].time).days])
plt.show()