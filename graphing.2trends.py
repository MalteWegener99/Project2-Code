from Sample import Sample_conv
import matplotlib.pyplot as plt
import numpy as np
import sys
import struct
import datetime
from math import cos, sin, sqrt
import math
from math import degrees as deg
from utils import average_over
from scipy.stats import linregress
from scipy.optimize import curve_fit
from outlier import outlierdet
import statistics as st

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
        # series = average_over(series, 7)


        return collection

def to_fit(x, a, b, c, d):
    return a + b*x + c*np.sin(2*math.pi/(365) * x + d)

def to_fit2(x, a, b, c, d):
    return a + b*x/(24*3600) + c*np.sin(2*math.pi/(365*24*3600) * x + d)

def graph_series(series):
    series = sorted(series, key=lambda x: x.time)
    
    times = []
    locx = []
    locy = []
    locz = []
    init_time = series[0].time
    init_year = init_time//1000
    init_days = init_time - init_year*1000
    init_date = datetime.date.fromordinal(datetime.date(init_year,1,1).toordinal()+ init_days - 1)
    i = 0

#With outlier detection

    for elem in series:
        year = elem.time//1000
        days = elem.time - year*1000
        date = datetime.date.fromordinal(datetime.date(year,1,1).toordinal()+ days - 1)
        if not (datetime.date(1999,1,1) <= date < datetime.date(2012,1,1)):
            continue
        time = (date - init_date).total_seconds()
        times.append(time)
        locx.append(elem.pos[0])
        locy.append(elem.pos[1])
        locz.append(elem.pos[2])
    
    datax = np.column_stack((times,locx))
    datay = np.column_stack((times,locy))
    dataz = np.column_stack((times,locz))

    newdatax = outlierdet(datax,300,1)
    newdatay = outlierdet(datay,300,1)
    newdataz = outlierdet(dataz,300,1)

    p0 = np.array([datax[0,1],datay[0,1],dataz[0,1]])
    phi, lam, h = p0

    mat = np.array([[-1*sin(lam),cos(lam), 0.],
                        [-1*cos(lam)*sin(phi), -1*sin(lam)*sin(phi), cos(phi)],
                        [cos(lam)*cos(phi), sin(lam)*cos(phi), sin(phi)]]).T

    tmpx = []
    tmpy = []
    tmpz = []
    for elem in newdatax[:,1]:
        tmpx.append(elem - p0[0])
    tmpx = np.array(tmpx)
    for elem in newdatay[:,1]:
        tmpy.append(elem - p0[1])
    tmpy = np.array(tmpy)
    for elem in newdataz[:,1]:
        tmpz.append(elem - p0[2])
    tmpz = np.array(tmpz)
    
    newdatax[:,1] = mat[0,0]*tmpx+mat[0,1]*tmpx+mat[0,2]*tmpx
    newdatay[:,1] = mat[1,0]*tmpy+mat[1,1]*tmpy+mat[1,2]*tmpy
    newdataz[:,1] = mat[2,0]*tmpz+mat[2,1]*tmpz+mat[2,2]*tmpz

    
    ts2x = []
    mindatex = newdatax[0,0]
    for elem in newdatax[:,0]:
        ts2x.append(elem - mindatex)
    ts2x = np.array(ts2x)
    ts2y = []
    mindatey = newdatay[0,0]
    for elem in newdatay[:,0]:
        ts2y.append(elem - mindatey)
    ts2y = np.array(ts2y)
    ts2z = []
    mindatez = newdataz[0,0]
    for elem in newdataz[:,0]:
        ts2z.append(elem - mindatez)
    ts2z = np.array(ts2z)
    
    plps = [newdatax[:,1],newdatay[:,1],newdataz[:,1]]
    plts = [newdatax[:,0],newdatay[:,0],newdataz[:,0]]
    
    ts2 = [ts2x,ts2y,ts2z]

    placex  = 0 
    placey = 0
    px = []
    py = [] 
    devx = st.stdev(newdatax[:,1])
    for i in range(2,len(newdatax[:,1])-1):
        a = newdatax[i, 1]
        b = newdatax[i+1, 1]
        s = abs(b-a)
        if s > devx:
            px.append(i)
    placex = max(px)
    devy = st.stdev(newdatay[:,1])
    for i in range(2,len(newdatay[:,1])-1):
        a = newdatay[i, 1]
        b = newdatay[i+1, 1]
        s = abs(b-a)
        if s > devy:
            py.append(i)
    placey = max(py)
    print(px,py)



    north1 = linregress(ts2x[:placex+1],newdatax[:placex+1, 1])
    north2 = linregress(ts2x[placex+1:],newdatax[placex+1:, 1])
    east1 = linregress(ts2y[:placey+1],newdatay[:placey+1, 1])
    east2 = linregress(ts2y[placey+1:],newdatay[placey+1:, 1])
    up1, away1 = curve_fit(to_fit2, ts2z,newdataz[:, 1])
    print("{} mm/y".format(north1[0]*365*1000))
    print("{} mm/y".format(north2[0]*365*1000))
    print("{} mm/y".format(east1[0]*365*1000))
    print("{} mm/y".format(east2[0]*365*1000))
    print("{} mm/y".format(up1[1]*365*1000))
    print(north1)
    # print(east)(ts2[0][-1]-ts2[0][place]
    # print(up)plts[0][place+1]/31536000 + 2001


#Without outlier detection
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
        #print(np.matmul(mat, tmp))
        pos = np.zeros([3])
        errors.append(elem.err)

    plotpos = np.array(positions)
    ploterr = np.array(errors)
    errors = np.array(errors)
    # print(plotpos[:,2])
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
    print(east)

#Graphs

    f, axarr = plt.subplots(3,2)
    f.suptitle('With outlier vs without')
    axarr[0,0].axhline(y=0, color='k')
    axarr[0,0].scatter([x/31536000 + 2001 for x in newdatax[:,0]],newdatax[:,1],s = 2)
    axarr[0,0].set_ylim(min(newdatax[:,1]),max(newdatax[:,1]))
    axarr[0,0].set_ylabel('Displacement')
    #axarr[0,0].set_xlabel('Years')
    axarr[0,0].plot([mindatex/31536000 + 2001, plts[0][placex]/31536000 + 2001], [north1[1], north1[1] + north1[0]*ts2[0][placex]], color='r', label= "{} mm/y".format(north1[0]*365*1000))
    axarr[0,0].plot([plts[0][placex+1]/31536000 + 2001, plts[0][-1]/31536000 + 2001], [north2[1] +north2[0]*ts2[0][placex+1], north2[1] + north2[0]*ts2[0][-1]], color='m', label="{} mm/y".format(north2[0]*365*1000))
    axarr[0,0].legend(loc="lower right")

    axarr[1,0].axhline(y=0, color='k')
    axarr[1,0].scatter([x/31536000 + 2001 for x in newdatay[:,0]],newdatay[:,1],s = 2)
    axarr[1,0].set_ylim(min(newdatay[:,1]),max(newdatay[:,1]))
    axarr[1,0].set_ylabel('Displacement')
    #axarr[1,0].set_xlabel('Years')
    axarr[1,0].plot([mindatey/31536000 + 2001, plts[1][placey]/31536000 + 2001], [east1[1], east1[1] + east1[0]*ts2[1][placey]], color='r')
    axarr[1,0].plot([plts[1][placey+1]/31536000 + 2001, plts[1][-1]/31536000 + 2001], [east2[1] +east2[0]*ts2[1][placey+1], east2[1] + east2[0]*ts2[1][-1]], color='m')

    axarr[2,0].axhline(y=0, color='k')
    axarr[2,0].scatter([x/31536000 + 2001 for x in newdataz[:,0]],newdataz[:,1],s = 2)
    axarr[2,0].set_ylim(min(newdataz[:,1]),max(newdataz[:,1]))
    axarr[2,0].set_ylabel('Displacement')
    #axarr[2,0].set_xlabel('Years')
    axarr[2,0].plot([x/31536000 + 2001 for x in plts[2]], [to_fit2( x, up1[0], up1[1], up1[2], up1[3]) for x in ts2z], color='r')

    for i in range(0,3):
        axarr[i,1].axhline(y=0, color='k')
        axarr[i,1].set_xlim([times[0], times[-1]])
        axarr[i,1].plot(times, plotpos[:, i], linewidth=0.5)
        axarr[i,0].set_ylabel('Displacement')
        axarr[i,0].set_xlabel('Years')

    axarr[0,1].plot([mindate, times[-1]], [north[1], north[1] + north[0]*times2[-1]])
    axarr[1,1].plot([mindate, times[-1]], [east[1], east[1] + east[0]*times2[-1]])
    axarr[2,1].plot(times, list(map(lambda x: to_fit(x, up[0], up[1], up[2], up[3]), times2)))

    plt.show()

if __name__ == "__main__":
    graph_series(parse_binary_llh(sys.argv[1]))
    
    