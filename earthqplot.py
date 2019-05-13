import geoplotlib
from graphing import parse_binary_llh
from geoplotlib.layers import DelaunayLayer
import sys, os
from math import degrees
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv
import numpy as np

if __name__ == "__main__":
    path = sys.argv[1]
    files = os.listdir(path)
    stations = []
    for file in files:
        if file[-1] == 'u':
            stations.append(parse_binary_llh(path + '/' + file)[0])
            print(stations[-1].name)

    file = open('tmp.csv', 'w')
    file.write('name,lat,lon\n')
    for stat in stations:
        name, lon, lat = (stat.name, degrees(stat.pos[0]), degrees(stat.pos[1]))
        #print(name, lon, lat)
        file.write(','.join([name, str(lon), str(lat)]) + '\n')
    file.close()
    
    data = read_csv('tmp.csv')
    #print(type(data))

    earthquakes = read_csv('earthquakes.csv')
    #print(type(earthquakes))

    geoplotlib.dot(data)
    geoplotlib.labels(data, 'name', color=[0,0,255,255], font_size=7, anchor_x='center')

    geoplotlib.kde(earthquakes, bw=2, cut_below=1e-4)
    geoplotlib.set_smoothing(True)    
    geoplotlib.dot(earthquakes)
    geoplotlib.labels(earthquakes, 'name', color=[0,0,255,255], font_size=7, anchor_x='center')

    
    mags = np.genfromtxt("earthquakes.csv",skip_header=1,delimiter=',')[:,-1]
    print(mags)
    print(len(mags))
    #geoplotlib.markers(earthquakes, 'm.png')
    #geoplotlib.markers(earthquakes, 'm.png', f_tooltip=lambda r: r['name'])
    #for i in range(len(mags)):
    #    geoplotlib.markers(earthquakes, 'marker2.png')
    #    print(i)
        #, marker_preferred_size=(32*int(mags[i]/min(mags)))
    print('done')
    geoplotlib.show()
