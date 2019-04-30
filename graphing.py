from Sample import Sample_conv
import matplotlib.pyplot as plt
import numpy as np
import sys
import struct
import datetime
from math import cos, sin
import math
from math import degrees as deg
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
        series = sorted(collection,key = lambda x: x.time)
        # series = average_over(series, 7)


        times = []
        locx = []
        locy = []
        locz = []
        init_time = series[0].time
        init_year = init_time//1000
        init_days = init_time - init_year*1000
        init_date = datetime.date.fromordinal(datetime.date(init_year,1,1).toordinal()+ init_days - 1)
        i = 0

        for elem in series:
            year = elem.time//1000
            days = elem.time - year*1000
            date = datetime.date.fromordinal(datetime.date(year,1,1).toordinal()+ days - 1)
            if not (datetime.date(1999,1,1) <= date < datetime.date(2012,1,1)):
                continue
            #time = (date - init_date).total_seconds()
            times.append(date)
            locx.append(elem.pos[0])
            locy.append(elem.pos[1])
            locz.append(elem.pos[2])
            
    
        datax = np.column_stack((times,locx))
        datay = np.column_stack((times,locy))
        dataz = np.column_stack((times,locz))

        newdatax = outlierdet(datax,300,1)
        newdatay = outlierdet(datay,300,1)
        newdataz = outlierdet(dataz,300,1)

        ts2x = []
        mindatex = newdatax[0,0]
        for elem in newdatax[:,0]:
            ts2x.append((elem - mindatex).days)
        #ts2x = np.array(ts2x)
        ts2y = []
        mindatey = newdatay[0,0]
        for elem in newdatay[:,0]:
            ts2y.append((elem - mindatey).days)
        #ts2y = np.array(ts2y)
        ts2z = []
        mindatez = newdataz[0,0]
        for elem in newdataz[:,0]:
            ts2z.append((elem - mindatez).days)
        #ts2z = np.array(ts2z)
        
        plps = [newdatax[:,1],newdatay[:,1],newdataz[:,1]]
        plts = [newdatax[:,0],newdatay[:,0],newdataz[:,0]]
        
        plts2 = [newdatax[:,0]-len(newdatax)*newdatax[0,0],newdatay[:,0]-len(newdatay)*newdatay[1,0],newdataz[:,0]-len(newdataz)*newdataz[2,0]]
        inl_x, inl_y, outl_x, outl_y = outlierdet(times,locations,0.45)
        print(len(ts2y))
        print(ts2y.shape)
        print(len(newdatay[:, 1]))
        print(newdatay[:, 1].shape)

        north = linregress(ts2x,newdatax[:, 1])
        print("h")
        input()
        east = linregress(ts2y, newdatay[:, 1])
        up, away = curve_fit(to_fit, ts2z,newdataz[:, 1])
        print("{} mm/y".format(north[0]*365*1000))
        print("{} mm/y".format(east[0]*365*1000))
        print("{} mm/y".format(up[1]*365*1000))


        f, gra = plt.subplots(3, sharex=True)
        f.suptitle('lat, lon, heigth')

        p0 = np.array([datax[0,1],datay[0,1],dataz[0,1]])
        phi, lam, h = p0

        mat = np.array([[-1*sin(lam),cos(lam), 0.],
                            [-1*cos(lam)*sin(phi), -1*sin(lam)*sin(phi), cos(phi)],
                            [cos(lam)*cos(phi), sin(lam)*cos(phi), sin(phi)]]).T

        for i in range(0,3):
            gra[i].axhline(y=0, color='k')
            gra[i].set_xlim([plts[i][0], plts[i][-1]])
            pos = []
            for j in range(len(plps[i])):
                temp = np.array(plps[i][j])-np.array(p0[i])
                pos.append(mat[0,i]*temp + mat[1,i]*temp + mat[2,i]*temp)
            gra[i].plot(plts[i], pos, linewidth=0.5)

        # plt.subplot(3,1,1)
        # plt.scatter(newdatax[:,0],newdatax[:,1],s = 2)
        # plt.ylim(min(newdatax[:,1]),max(newdatax[:,1]))
        #  # plt.scatter(times,d_ave)
        # plt.subplot(3,1,2)
        # plt.scatter(newdatay[:,0],newdatay[:,1],s = 2)
        # plt.ylim(min(newdatay[:,1]),max(newdatay[:,1]))
        # plt.subplot(3,1,3)
        # plt.scatter(newdataz[:,0],newdataz[:,1],s = 2)
        # plt.ylim(min(newdataz[:,1]),max(newdataz[:,1]))
        gra[0].plot([plts[0][0], plts[0][-1]], [north[1], north[1] + north[0]*ts2x[-1]])
        gra[1].plot([plts[1][0], plts[1][-1]], [east[1], east[1] + east[0]*ts2y[-1]])
        gra[2].plot(plts[2][:], list(map(lambda x: to_fit(x, up[0], up[1], up[2], up[3]),ts2z)))
        print(ts2x[-1])
        input()
        plt.show()
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
    print(len(times2))
    print(times2)
    print(len( plotpos[:, 0]))
    print( plotpos[:, 0].shape)
    print(plotpos[:, 0])
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
    
    