from Sample import Sample_conv
import matplotlib.pyplot as plt
import numpy as np
import sys
import struct
import datetime
from math import cos, sin
import math

def parse_binary_llh(path):
    name = path.split('/')[-1][0:4]
    collection = []

    with open(path, 'rb') as file:
        n = file.read(8)
        n = struct.unpack('<q', n)[0]

        for i in range(0,n):
            time = file.read(8)
            time = struct.unpack('<q', time)[0]
            pos = np.zeros([3])
            mat = np.zeros([3])
            for i in range(0, 3):
                tmp = file.read(8)
                tmp = struct.unpack('<d', tmp)[0]
                pos[i] = tmp

            for i in range(0, 3):
                tmp = file.read(8)
                tmp = struct.unpack('<d', tmp)[0]
                mat[i] = tmp

            pos_f = file.tell()
            collection.append(Sample_conv(name, time, pos, mat))

        return collection


def graph_series(series):
    series = sorted(series, key=lambda x: x.time)
    mindate = series[0].time
    p0 = np.array(series[0].pos)
    phi, lam, h = p0
    mat = np.array([[-1*sin(lam),cos(lam), 0.],
                        [-1*cos(lam)*sin(phi), -1*sin(lam)*sin(phi), cos(phi)],
                        [cos(lam)*cos(phi), sin(lam)*cos(phi), sin(phi)]]).T

    positions = []
    errors = []
    times = []
    i = 0
    for elem in series:
        year = elem.time//1000
        days = elem.time - year*1000
        times.append(datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + days - 1))
        tmp = p0 - elem.pos
        positions.append(np.matmul(mat, tmp))
        pos = np.zeros([3])
        errors.append(elem.err)


    plotpos = np.array(positions)
    ploterr = np.array(errors)
    errors = np.array(errors)
    f, axarr = plt.subplots(3, sharex=True)
    f.suptitle('DAMn')
    for i in range(0,3):
        axarr[i].errorbar(times, plotpos[:, i], yerr=errors[:,i], linewidth=0.5, fmt='o', markersize=0.1)
    plt.show()

graph_series(parse_binary_llh(sys.argv[1]))