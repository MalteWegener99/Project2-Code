import geoplotlib
from graphing import parse_binary_llh
import sys, os
from math import degrees
from geoplotlib.utils import read_csv

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
geoplotlib.dot(data)
geoplotlib.show()
