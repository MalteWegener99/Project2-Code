#begin: plot starting locations of every station with time-series file
#move plotmap with ASDW-keys, zoom with IO-keys
import geoplotlib as gp
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv
import glob, os, sys, csv, fnmatch
from graphing import parse_binary_llh
from math import degrees as deg

#path to converted files
path = 'C:/Users/rdenb/Documents/tmp/conv'
os.chdir(path)

#get starting location of all stations from files
Locations = []
for file in os.listdir():
    if fnmatch.fnmatch(file, '*.neu'):
        Sname,T,N = file.split('.')
        Collection = parse_binary_llh(path+'/'+file)
        series = sorted(Collection, key=lambda x: x.time)
        #convert list with [phi, lambda, h] to [name, lat, lon]
        series[0].pos[0] = deg(series[0].pos[0])
        series[0].pos[1] = deg(series[0].pos[1])+180
        Locations.append([Sname,series[0].pos[0],series[0].pos[1]])

#path to SLOCs.csv
path = 'C:/Users/rdenb/Documents/Project2-Code'
os.chdir(path)

#empty SLOCs.csv
f = open("SLOCs.csv", "w+")
f.close()

#write csv to be read by geoplotlib
with open('SLOCs.csv', mode='w', newline='') as SLOCs:
    SLOCs = csv.writer(SLOCs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    SLOCs.writerow(['name', 'lat', 'lon'])
    for station in Locations:
        SLOCs.writerow([station[0], station[1], station[2]])

#plot stations
Plotdata = read_csv('SLOCs.csv')
gp.dot(Plotdata, color='red', point_size=1.5)
gp.labels(Plotdata, 'name', color='black', font_size=8, anchor_x='center')
gp.show()



#ToDo: fix longitude inconsistency errors