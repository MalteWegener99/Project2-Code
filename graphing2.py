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
import matplotlib.dates as mdates

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

def load_clean_set(path):
    data_set = parse_binary_llh(path)
    data_set = [convert_to_date(x) for x in data_set]
    data_set = list(sorted(data_set, key=lambda x: x.time))
    baseline = data_set[0].time
    #make data relative to baseline
    data_set = [date_relative_days(x,baseline) for x in data_set]
    #manufacture time series
    size = len(data_set)
    data = np.zeros([size,7])

    days = [x.time for x in data_set]
    ew = np.array([x.pos[0] for x in data_set])
    ns = np.array([x.pos[1] for x in data_set])
    ud = np.array([x.pos[2] for x in data_set])
    ewe = np.array([x.err[0] for x in data_set])
    nse = np.array([x.err[1] for x in data_set])
    ude = np.array([x.err[2] for x in data_set])

    data[:,0] = days
    data[:,1] = ew
    data[:,2] = ns
    data[:,3] = ud
    data[:,4] = ewe
    data[:,5] = nse
    data[:,6] = ude

    return outlierdet(data, 50, 20), baseline, data

def to_fit(x, a, b, c, d):
    return a + b*x + c*np.sin(2*math.pi/365 * x + d)

def to_fit2(x, a, b, c, d, e):
    x = (x-a)/e
    return a*np.sin(b*x)*np.cos(np.sqrt(c*x))+d

def predict_plot(data, baseline, datao):

    p0 = data[0,1:4]
    print(p0)
    lam, phi, h = p0
    p0 = llhtoxyz(p0)
    mat = np.array([
        [-1*sin(phi), cos(phi), 0],
        [-1*cos(phi)*sin(lam), -1*sin(phi)*sin(lam), cos(lam)],
        [cos(phi)*cos(lam), sin(phi)*cos(lam), sin(lam)]
    ])
    f, axarr = plt.subplots(3,2, sharex=True)
    plotpos = np.array([np.matmul(mat, llhtoxyz(data[i,1:4])-p0) for i in range(data.shape[0])])

    #make subseries for plotting
    split = (datetime.date(2004,12,26)-baseline).days
    splitindex = 0
    for i in range(data.shape[0]):
        if data[i,0] < split:
            splitindex = i
        else:
            break
    # Plotting of the actual stuff
    f.suptitle(sys.argv[1])
    axarr[0,0].set_title("East [m]")
    axarr[1,0].set_title("North [m]")
    axarr[2,0].set_title("Up [m]")

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    for i in range(3):
        axarr[i,0].xaxis.set_major_locator(years)
        axarr[i,0].xaxis.set_major_formatter(yearsFmt)
        axarr[i,0].xaxis.set_minor_locator(months)

    for i in range(0,2):
        predict = linregress(data[:splitindex,0], plotpos[:splitindex,i])
        print("Before:", predict[0]*365*1000, "mm/yr")
        predict2, away = 0,0#curve_fit(to_fit2, data[:splitindex,0], plotpos[:splitindex,i])
        #print("After:", predict2[0]*365*1000, "mm/yr")
        axarr[i,0].axhline(y=0, color='k')
        axarr[i,0].set_ylim([min(plotpos[:,i]), max(plotpos[:,i])])
        axarr[i,0].axvline(x=datetime.datetime(2004,12,26))
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i,0].plot([baseline + datetime.timedelta(days=data[0,0]), baseline + datetime.timedelta(days=data[splitindex-1,0])], [predict[1], predict[1]+predict[0]*(data[splitindex-1,0]-data[0,0])], 'r--')
        #axarr[i].plot([baseline + datetime.timedelta(days=x) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], [to_fit2(x, *predict2) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], 'r--')
        axarr[i,0].errorbar([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], yerr=10*data[:, 4+i], fmt='x', elinewidth=0.1, markersize=0.5)
        #axarr[i].scatter([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], s=0.1)
    
    for i in range(2,3):
        up, away = curve_fit(to_fit, data[:splitindex,0], plotpos[:splitindex,i])
        up2, away = curve_fit(to_fit, data[splitindex+1:,0], plotpos[splitindex+1:,i])
        axarr[i,0].axhline(y=0, color='k')
        axarr[i,0].set_ylim([min(plotpos[:,i]), max(plotpos[:,i])])
        axarr[i,0].axvline(x=datetime.datetime(2004,12,26))
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i,0].plot([baseline + datetime.timedelta(days=x) for x in np.arange(data[0,0], data[splitindex,0], 1)], [to_fit(x, *up) for x in np.arange(data[0,0], data[splitindex,0], 1)], 'r--')
        axarr[i,0].plot([baseline + datetime.timedelta(days=x) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], [to_fit(x, *up2) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], 'r--')
        axarr[i,0].errorbar([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], yerr=10*data[:, 4+i], fmt='x', elinewidth=0.1, markersize=0.5)
    
    
    data = datao
    p0 = data[0,1:4]
    print(p0)
    lam, phi, h = p0
    p0 = llhtoxyz(p0)
    mat = np.array([
        [-1*sin(phi), cos(phi), 0],
        [-1*cos(phi)*sin(lam), -1*sin(phi)*sin(lam), cos(lam)],
        [cos(phi)*cos(lam), sin(phi)*cos(lam), sin(lam)]
    ])
    plotpos = np.array([np.matmul(mat, llhtoxyz(data[i,1:4])-p0) for i in range(data.shape[0])])

    #make subseries for plotting
    split = (datetime.date(2004,12,26)-baseline).days
    splitindex = 0
    for i in range(data.shape[0]):
        if data[i,0] < split:
            splitindex = i
        else:
            break
    # Plotting of the actual stuff
    f.suptitle(sys.argv[1])
    axarr[0,1].set_title("East [m]")
    axarr[1,1].set_title("North [m]")
    axarr[2,1].set_title("Up [m]")

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    for i in range(3):
        axarr[i,1].xaxis.set_major_locator(years)
        axarr[i,1].xaxis.set_major_formatter(yearsFmt)
        axarr[i,1].xaxis.set_minor_locator(months)

    
    for i in range(0,2):
        predict = linregress(data[:splitindex,0], plotpos[:splitindex,i])
        print("Before:", predict[0]*365*1000, "mm/yr")
        predict2, away = 0,0#curve_fit(to_fit2, data[:splitindex,0], plotpos[:splitindex,i])
        #print("After:", predict2[0]*365*1000, "mm/yr")
        axarr[i,1].axhline(y=0, color='k')
        axarr[i,1].set_ylim([min(plotpos[:,i]), max(plotpos[:,i])])
        axarr[i,1].axvline(x=datetime.datetime(2004,12,26))
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i,1].plot([baseline + datetime.timedelta(days=data[0,0]), baseline + datetime.timedelta(days=data[splitindex-1,0])], [predict[1], predict[1]+predict[0]*(data[splitindex-1,0]-data[0,0])], 'r--')
        #axarr[i].plot([baseline + datetime.timedelta(days=x) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], [to_fit2(x, *predict2) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], 'r--')
        axarr[i,1].errorbar([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], yerr=10*data[:, 4+i], fmt='x', elinewidth=0.1, markersize=0.5)
        #axarr[i].scatter([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], s=0.1)
    
    for i in range(2,3):
        up, away = curve_fit(to_fit, data[:splitindex,0], plotpos[:splitindex,i])
        up2, away = curve_fit(to_fit, data[splitindex+1:,0], plotpos[splitindex+1:,i])
        axarr[i,1].axhline(y=0, color='k')
        axarr[i,1].set_ylim([min(plotpos[:,i]), max(plotpos[:,i])])
        axarr[i,1].axvline(x=datetime.datetime(2004,12,26))
        #axarr[i].set_xlim([baseline, baseline+datetime.timedelta(days=data[i][-1,0])])
        axarr[i,1].plot([baseline + datetime.timedelta(days=x) for x in np.arange(data[0,0], data[splitindex,0], 1)], [to_fit(x, *up) for x in np.arange(data[0,0], data[splitindex,0], 1)], 'r--')
        axarr[i,1].plot([baseline + datetime.timedelta(days=x) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], [to_fit(x, *up2) for x in np.arange(data[splitindex+1,0], data[-1,0], 1)], 'r--')
        axarr[i,1].errorbar([baseline + datetime.timedelta(days=x) for x in data[:,0]], plotpos[:,i], yerr=10*data[:, 4+i], fmt='x', elinewidth=0.1, markersize=0.5)
    plt.show()


if __name__ == "__main__":
    predict_plot(*load_clean_set("conv/{}.tseries.neu".format(sys.argv[1])))