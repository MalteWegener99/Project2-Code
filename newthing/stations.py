lines = open("coordinates.txt").readlines()[2:]
names, lon, lat = [], [], []
for line in lines:
	split = lines.split()
	names.append(split[0])
	lon.append(float(split[1]))
	lat.append(float(split[2]))