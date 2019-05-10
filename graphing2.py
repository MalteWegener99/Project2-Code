from Sample import Sample_conv
import matplotlib.pyplot as plt
import numpy as np
import sys
import struct
import datetime
from math import cos, sin, sqrt
import math
from utils import average_over
from scipy.stats import linregress
from scipy.optimize import curve_fit
from outlier import outlierdet
from graphing import parse_binary_llh

# WGS 84
f = 1 / 298.257223563
e_2 = 2 * f - f**2
a = 6378137.  # SMA

def llhtoxyz(pos):
    phi, lam, h = pos
    N = a/(sqrt(1-e_2*sin(phi)**2))
    return np.array([
        (N+h)*cos(phi)*cos(lam),
        (N+h)*cos(phi)*sin(lam),
        ((1-e_2)*N+h)*sin(phi)
    ])

def convert_to_date(elem):
    year = elem.time//1000
    days = elem.time - year*1000
    date = datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + days - 1)
    elem.time = date
    return elem

def date_relative_days(elem, baseline):
    elem.time = (elem.time-baseline).days
    return elem
def to_fit(x, a, b, c, d):
    return a + b*x + c*np.sin(2*math.pi/(365) * x + d)

def load_clean_set(path):
    data_set = parse_binary_llh(path)
    data_set = [convert_to_date(x) for x in data_set]
    data_set = list(sorted(data_set, key=lambda x: x.time))
    baseline = data_set[0].time
    #make data relative to baseline
    data_set = [date_relative_days(x,baseline) for x in data_set]
    #manufacture time series
    size = len(data_set)
    data = np.zeros([size,4])

    days = [x.time for x in data_set]
    ew = np.array([x.pos[0] for x in data_set])
    ns = np.array([x.pos[1] for x in data_set])
    ud = np.array([x.pos[2] for x in data_set])

    data[:,0] = days
    data[:,1] = ew
    data[:,2] = ns
    data[:,3] = ud

    return outlierdet(data, 300, 2), baseline, data

def predict_plot(dataw, baseline, data):

    p0 = dataw[0,1:]
    lam, phi, h = p0
    p0 = llhtoxyz(p0)
    print(np.linalg.norm(p0))
    mat = np.array([
        [-1*sin(phi), cos(phi), 0],
        [-1*cos(phi)*sin(lam), -1*sin(phi)*sin(lam), cos(lam)],
        [cos(phi)*cos(lam), sin(phi)*cos(lam), sin(lam)]
    ])

    plotposw = np.array([np.matmul(mat, llhtoxyz(dataw[i,1:])-p0) for i in range(dataw.shape[0])])
    print(plotposw.shape)
    print(dataw.shape)
    
    p0 = data[0,1:]
    lam, phi, h = p0
    p0 = llhtoxyz(p0)
    print(np.linalg.norm(p0))
    mat = np.array([
        [-1*sin(phi), cos(phi), 0],
        [-1*cos(phi)*sin(lam), -1*sin(phi)*sin(lam), cos(lam)],
        [cos(phi)*cos(lam), sin(phi)*cos(lam), sin(lam)]
    ])
    f, axarr = plt.subplots(3,2, sharex=True)
    plotpos = np.array([np.matmul(mat, llhtoxyz(data[i,1:])-p0) for i in range(data.shape[0])])
    print(plotpos.shape)
    print(data.shape)
    

    north = linregress(dataw[:,0],dataw[:,2])
    east = linregress(dataw[:,0],dataw[:,1])
    up, away = curve_fit(to_fit,dataw[:,0],dataw[:,3])

    for i in range(0,3):
        axarr[i,0].axhline(y=0, color='k')
        axarr[i,0].set_ylim([min(plotposw[:,i]), max(plotposw[:,i])])
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i,0].scatter([baseline + datetime.timedelta(days=x) for x in dataw[:,0]], plotposw[:,i], s=0.1)
        axarr[i,0].set_ylabel('Displacement')
    for i in range(0,3):
        axarr[i,1].axhline(y=0, color='k')
        axarr[i,1].set_ylim([min(plotpos[:,i]), max(plotpos[:,i])])
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i,1].scatter([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], s=0.1)
        axarr[i,1].set_ylabel('Displacement')
    
    axarr[0,0].set_xlabel('East')
    axarr[0,1].set_xlabel('East')
    axarr[1,0].set_xlabel('North')
    axarr[1,1].set_xlabel('North')
    axarr[2,0].set_xlabel('Up')
    axarr[2,1].set_xlabel('Up')
   
    plt.show()


if __name__ == "__main__":
    predict_plot(*load_clean_set("conv/{}.tseries.neu".format(sys.argv[1])))
