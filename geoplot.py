import geoplotlib
from graphing import parse_binary_llh
from geoplotlib.layers import DelaunayLayer
import sys, os
from math import degrees
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv

if __name__ == "__main__":
    path = sys.argv[1]
    files = os.listdir(path)
    stations = []
    for file in files:
        stations.append(parse_binary_llh(path + '/' + file)[0])
        print(stations[-1].name)

    file = open('tmp.csv', 'w')
    file.write('name,lat,lon\n')
    for stat in stations:
        name, lon, lat = (stat.name, degrees(stat.pos[0]), degrees(stat.pos[1]))
        print(name, lon, lat)
        file.write(','.join([name, str(lon), str(lat)]) + '\n')
    file.close()
    
    data = read_csv('tmp.csv')
    print(type(data))
    geoplotlib.delaunay(data, cmap="hot_r")
    geoplotlib.labels(data, 'name', color=[0,0,255,255], font_size=10, anchor_x='center')
    geoplotlib.show()
