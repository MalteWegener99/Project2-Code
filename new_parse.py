from Sample import Sample_conv
import datetime
import matplotlib.pyplot as plt

def parse_date(string):
	year = string[-2:]
	day = string[:2]
	month = string[2:5]
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
	return datetime.date(year, monthtonum[month], day)


lat_file = open("PHUK.latn").readlines()
lon_file = open("PHUK.lonn").readlines()
rad_file = open("PHUK.radn").readlines()

points = []

for i in range(len(lat_file)):
	lat = float(lat_file[i].split()[1])
	lon = float(lon_file[i].split()[1])
	hei = float(rad_file[i].split()[1])
	dat = lat_file[i].split()[-1]
	s_lat = float(lat_file[i].split()[2])
	s_lon = float(lon_file[i].split()[2])
	s_hei = float(rad_file[i].split()[2])

	points.append(Sample_conv("PHKT", dat, [lat,lon,hei], [s_lat,s_lon,s_hei]))

plt.scatter([x.time for x in points], [x.pos[0] for x in points])
plt.show()