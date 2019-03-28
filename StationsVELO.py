#plot starting positions of stations and add velocity vectors
#move plotmap with ASDW-keys, zoom with IO-keys
import geoplotlib as gp
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv
import glob, os, sys, csv, fnmatch
from graphing import parse_binary_llh
from math import degrees as deg
from splining import great_circle_dist

#path to converted files
path = os.path.dirname(os.path.realpath(__file__))+'/conv'
os.chdir(path)

#get starting location of all stations from files
Earth_radius = float(6378) #[m]
Locations = []
for file in os.listdir():
    if fnmatch.fnmatch(file, '*.neu'):
        Sname,T,N = file.split('.')
        Collection = parse_binary_llh(path+'/'+file)
        series = sorted(Collection, key=lambda x: x.time)
        #convert list with [phi, lambda, h] to [name, lat, lon]
        S_startlat = deg(series[0].pos[0])
        S_startlon = deg(series[0].pos[1])
        S_Starttime = series[0].time
        S_destilat = deg(series[100].pos[0])
        S_destilon = deg(series[100].pos[1])
        S_destitime = series[100].time
        lat_V = ((S_startlat-S_destilat)/(S_destitime-S_Starttime))*Earth_radius
        lon_V = ((S_startlon-S_destilon)/(S_destitime-S_Starttime))*Earth_radius
        V_destilat = S_startlat + ((S_destilat-S_startlat)*500000)
        V_destilon = S_startlon + ((S_destilon-S_startlon)*500000)
        Locations.append([Sname,S_startlat,S_startlon,V_destilat,V_destilon])



#path to VLOCs.csv
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#empty VLOCs.csv
f = open("VLOCs.csv", "w+")
f.close()

#write csv to be read by geoplotlib
with open('VLOCs.csv', mode='w', newline='') as VLOCs:
    VLOCs = csv.writer(VLOCs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    VLOCs.writerow(['name', 'S_lat', 'S_lon', 'D_lat', 'D_lon'])
    for station in Locations:
        VLOCs.writerow([station[0], station[1], station[2], station[3], station[4]])

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
Plotdata1 = read_csv('VLOCs.csv')
Plotdata2 = read_csv('SLOCs.csv')
gp.graph(Plotdata1, 'S_lat', 'S_lon', 'D_lat', 'D_lon', linewidth=3, color='cold')
gp.dot(Plotdata2, color='red', point_size=2)
#optional: gp.labels(Plotdata, 'name', color='black', font_size=8, anchor_x='center')
gp.tiles_provider('positron')

gp.show()