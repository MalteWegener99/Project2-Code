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
from graphing import parse_binary_llh


def convert_to_date(elem):
    year = elem.time//1000
    days = elem.time - year*1000
    date = datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + days - 1)
    elem.time = date
    return elem

def date_relative_days(elem, baseline):
    elem.time = (elem.time-baseline).days
    return elem

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

    data_plot = [0,0,0]
    data_plot[0] = ew_data
    data_plot[1] = ns_data
    data_plot[2] = ud_data

    return data_plot, baseline

def change_p(pe, ni, s):
    p = pe.copy()
    p[ni] = s
    return p

def predict_plot(data, baseline):

    p0 = sum([np.array([data[0][x,1],data[1][x,1],data[2][x,1]]) for x in range(10)])/10
    phi, lam, h = p0
    mat = np.array([[-1*sin(lam),cos(lam), 0.],
                        [-1*cos(lam)*sin(phi), -1*sin(lam)*sin(phi), cos(phi)],
                        [cos(lam)*cos(phi), sin(lam)*cos(phi), sin(phi)]]).T
    f, axarr = plt.subplots(3, sharex=True)
    for i in range(0,3):

        pos = [np.dot(mat[:,i], np.array()) for x in data[i][:,1]]
        axarr[i].axhline(y=0, color='k')
        axarr[i].set_ylim([min(pos), max(pos)])
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i].scatter([baseline + datetime.timedelta(days=x) for x in data[i][:, 0]], pos, s=0.1)

    plt.show()


if __name__ == "__main__":
    predict_plot(*load_clean_set(r"conv/PHKT.tseries.neu"))
