from Sample import Sample_conv
import matplotlib.pyplot as plt
import numpy as np
import sys
import struct
import datetime
from math import cos, sin
import math
from utils import average_over
from scipy.stats import linregress
from scipy.optimize import curve_fit
from outlier import outlierdet

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
            ncol = collection[1,2]
            ncol = outlierdet(ncol,300,1)
            collection[1] = ncol[0]
            collection[2] = ncol[1]
        return collection

def to_fit(x, a, b, c, d):
    return a + b*x + c*np.sin(2*math.pi/365 * x + d)

def graph_series(series):
    series = sorted(series, key=lambda x: x.time)
    series = average_over(series, 7)
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
        date = datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + days - 1)
        if not (datetime.date(1999,1,1) <= date < datetime.date(2012,1,1)):
            continue
        times.append(date)
        tmp = elem.pos - p0
        positions.append(np.matmul(mat, tmp))
        print(np.matmul(mat, tmp))
        pos = np.zeros([3])
        errors.append(elem.err)

    plotpos = np.array(positions)
    ploterr = np.array(errors)
    errors = np.array(errors)
    
    times2 = []
    mindate = times[0]
    for elem in times:
        times2.append((elem - mindate).days)
    

    north = linregress(times2, plotpos[:, 0])
    east = linregress(times2, plotpos[:, 1])
    up, away = curve_fit(to_fit, times2, plotpos[:, 2])
    print("{} mm/y".format(north[0]*365*1000))
    print("{} mm/y".format(east[0]*365*1000))
    print("{} mm/y".format(up[1]*365*1000))
    print(north)

    f, axarr = plt.subplots(3, sharex=True)
    f.suptitle('DAMn')
    # for i in range(0,3):
    #     axarr[i].axhline(y=0, color='k')
    #     axarr[i].set_xlim([times[0], times[-1]])
    #     axarr[i].errorbar(times, plotpos[:, i], yerr=errors[:,i], linewidth=0.5, fmt='x', markersize=0.81)

    for i in range(0,3):
        axarr[i].axhline(y=0, color='k')
        axarr[i].set_xlim([times[0], times[-1]])
        axarr[i].plot(times, plotpos[:, i], linewidth=0.5)

    axarr[0].plot([mindate, times[-1]], [north[1], north[1] + north[0]*times2[-1]])
    axarr[1].plot([mindate, times[-1]], [east[1], east[1] + east[0]*times2[-1]])
    axarr[2].plot(times, list(map(lambda x: to_fit(x, up[0], up[1], up[2], up[3]), times2)))

    plt.show()

if __name__ == "__main__":
    graph_series(parse_binary_llh(sys.argv[1]))