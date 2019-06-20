from Sample import Sample_conv
import datetime
import matplotlib.pyplot as plt
import sys
import matplotlib.dates as mdates
from scipy.stats import linregress
from scipy.optimize import curve_fit
import numpy as np

def to_fit2(x, a, c, d, t, b, poop):
    print(b)
    return a + b*x + -1*c*np.log(1+(x-poop)/t)

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

	points.append(Sample_conv(sys.argv[1], parse_date(dat), [lat,lon,hei], [s_lat,s_lon,s_hei]))

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
print(type(points[0].time))

split = datetime.datetime(2004,12,26)
splitindex = 0
for i in range(len(points)):
    if points[i].time < split:
        splitindex = i
    else:
        break
splitindex += 40
baseline = points[0].time
fittime = [(x.time - points[0].time).days for x in points[splitindex:]]
fitdata = np.array([points[i].pos[1] for i in range(splitindex, len(points))])
pretime = [(x.time - points[0].time).days for x in points[:splitindex]]
predata = np.array([points[i].pos[1] for i in range(splitindex)])

pretimespeed = linregress(pretime, predata)[0]

print(pretimespeed)
to_fit2_real = lambda x, a, c, d, t: to_fit2(x, a, c, d, t, pretimespeed, splitindex-40)
#fitted = curve_fit(to_fit2_real, fittime, fitdata)[0]
plt.scatter(fittime, fitdata)
plt.show()
