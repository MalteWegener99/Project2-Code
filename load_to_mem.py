'''
Loading XYZ files into memory
Use PEP8 for editing this file

'''

import numpy as np
import os
import re
import sys
import math
from Sample import Sample

"""
Files look like this:
Header
ID STATION STA [X,Y,Z] value +- devi
ID1 ID2 COV
if a line contains a '+-' its always a value
"""


def parse_file(file_name: str) -> []:
    '''
    Loads a file and returns a list of Sample
    '''

    time = int(file_name[-3:-1]) * 1000 + int(file_name[-7:-4])
    if time > 20000:
        time += 1900000
    else:
        time += 2000000

    collector = []
    file = open(file_name)
    lines = file.readlines()
    file.close()

    # remove header
    lines = lines[1:]
    n_stations = len(lines)//3//2

    # proceed in multiples of 3
    for i in range(0, n_stations * 3, 3):
        val = 4
        dev = 6
        xsplit = lines[i].split()
        ysplit = lines[i+1].split()
        zsplit = lines[i+2].split()
        name = xsplit[1]
        x = float(xsplit[val])
        y = float(ysplit[val])
        z = float(zsplit[val])
        xx = float(xsplit[dev])**2
        yy = float(ysplit[dev])**2
        zz = float(zsplit[dev])**2

        cov1split = lines[i + n_stations*3].split()
        cov2split = lines[i + n_stations*3 + 1].split()
        cov3split = lines[i + n_stations*3 + 2].split()

        xy = float(cov1split[2]) * math.sqrt(xx*yy)
        xz = float(cov2split[2]) * math.sqrt(xx*zz)
        yz = float(cov3split[2]) * math.sqrt(yy*zz)

        pos = np.array([x, y, z])
        covariance = np.array([[xx, xy, xz],
                               [xy, yy, yz],
                               [xz, yz, zz]])

        collector.append(Sample(name, time, pos, covariance))

    return collector


def save_tseries_bin(collection, output_folder):
    #collection = collection.sort(key=lambda x: x.time)
    print(type(collection))
    print(type(collection[0]))
    name = collection[0].name
    file = open(output_folder + "/" + name + ".tseries", 'wb')
    file.write(len(collection).to_bytes(8, byteorder='little'))
    for item in collection:
        file.write(item.time.to_bytes(8, byteorder='little'))
        for i in range(0, 3):
            item.pos[i].tofile(file)

        for i in range(0, 3):
            item.mat[:, i].tofile(file)

    file.close()


def load_folder(path) -> list:
    files = list(filter(lambda x: re.match(r'PZITRF08[0-9]{3}\.[0-9]{2}X$', x),
                   os.listdir(path)))

    collection = []
    dp = 1. / len(files)
    p = 0.
    for file in files:
        collection += (parse_file(path + '/' + file))
        p += dp
        print("{0:.2%} done".format(p))

    return collection


def split_into_series(collection) -> dict:
    stations = set()
    series = dict()
    for item in collection:
        stations.add(item.name)
    
    for station in stations:
        series[station] = list(filter(lambda x: x.name == station,
                                      collection))
    print("done")
    return series


def convert_folder(path, out):
    time_series = split_into_series(load_folder(path))

    for key in time_series:
        print(key)
        print(type(time_series[key]))
        save_tseries_bin(time_series[key], out)

if __name__ == "__main__":
    convert_folder(sys.argv[1], sys.argv[2])