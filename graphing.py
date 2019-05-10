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
        # # series = average_over(series, 7)


        # times = []
        # locx = []
        # locy = []
        # locz = []
        # init_time = series[0].time
        # init_year = init_time//1000
        # init_days = init_time - init_year*1000
        # init_date = datetime.date.fromordinal(datetime.date(init_year,1,1).toordinal()+ init_days - 1)
        # i = 0

        # for elem in series:
        #     year = elem.time//1000
        #     days = elem.time - year*1000
        #     date = datetime.date.fromordinal(datetime.date(year,1,1).toordinal()+ days - 1)
        #     if not (datetime.date(1999,1,1) <= date < datetime.date(2012,1,1)):
        #         continue
        #     time = (date - init_date).total_seconds()
        #     times.append(time)
        #     locx.append(elem.pos[0])
        #     locy.append(elem.pos[1])
        #     locz.append(elem.pos[2])
            
    
        # datax = np.column_stack((times,locx))
        # datay = np.column_stack((times,locy))
        # dataz = np.column_stack((times,locz))

        # newdatax = outlierdet(datax,300,1)
        # newdatay = outlierdet(datay,300,1)
        # newdataz = outlierdet(dataz,300,1)

        # p0 = np.array([datax[0,1],datay[0,1],dataz[0,1]])
        # phi, lam, h = p0

        # mat = np.array([[-1*sin(lam),cos(lam), 0.],
        #                     [-1*cos(lam)*sin(phi), -1*sin(lam)*sin(phi), cos(phi)],
        #                     [cos(lam)*cos(phi), sin(lam)*cos(phi), sin(phi)]]).T

        # tmpx = []
        # tmpy = []
        # tmpz = []
        # for elem in newdatax[:,1]:
        #     tmpx.append(elem - p0[0])
        # tmpx = np.array(tmpx)
        # for elem in newdatay[:,1]:
        #     tmpy.append(elem - p0[1])
        # tmpy = np.array(tmpy)
        # for elem in newdataz[:,1]:
        #     tmpz.append(elem - p0[2])
        # tmpz = np.array(tmpz)
  
        # newdatax[:,1] = mat[0,0]*tmpx+mat[0,1]*tmpx+mat[0,2]*tmpx
        # newdatay[:,1] = mat[1,0]*tmpy+mat[1,1]*tmpy+mat[1,2]*tmpy
        # newdataz[:,1] = mat[2,0]*tmpz+mat[2,1]*tmpz+mat[2,2]*tmpz
        # ts2x = []
        # mindatex = newdatax[0,0]
        # for elem in newdatax[:,0]:
        #     ts2x.append(elem - mindatex)
        # ts2x = np.array(ts2x)
        # ts2y = []
        # mindatey = newdatay[0,0]
        # for elem in newdatay[:,0]:
        #     ts2y.append(elem - mindatey)
        # ts2y = np.array(ts2y)
        # ts2z = []
        # mindatez = newdataz[0,0]
        # for elem in newdataz[:,0]:
        #     ts2z.append(elem - mindatez)
        # ts2z = np.array(ts2z)
        
        # plps = [newdatax[:,1],newdatay[:,1],newdataz[:,1]]
        # plts = [newdatax[:,0],newdatay[:,0],newdataz[:,0]]
        
        # ts2 = [ts2x,ts2y,ts2z]


        # north = linregress(ts2x,newdatax[:, 1])
        # east = linregress(ts2y, newdatay[:, 1])
        # up, away = curve_fit(to_fit2, ts2z,newdataz[:, 1])
        # print("{} mm/y".format(north[0]*365*1000))
        # print("{} mm/y".format(east[0]*365*1000))
        # print("{} mm/y".format(up[1]*365*1000))
        # print(north)
        # print(east)
        # print(up)


        

        # plt.subplot(3,1,1)
        # plt.axhline(y=0, color='k')
        # plt.scatter([x/31536000 + 2001 for x in newdatax[:,0]],newdatax[:,1],s = 2)
        # plt.ylim(min(newdatax[:,1]),max(newdatax[:,1]))
        # plt.plot([mindatex/31536000 + 2001, plts[0][-1]/31536000 + 2001], [north[1], north[1] + north[0]*ts2[0][-1]], color='r')
         
        # plt.subplot(3,1,2)
        # plt.axhline(y=0, color='k')
        # plt.scatter([x/31536000 + 2001 for x in newdatay[:,0]],newdatay[:,1],s = 2)
        # plt.ylim(min(newdatay[:,1]),max(newdatay[:,1]))
        # plt.plot([mindatey/31536000 + 2001, plts[1][-1]/31536000 + 2001], [east[1], east[1] + east[0]*ts2[1][-1]], color='r')

        # plt.subplot(3,1,3)
        # plt.axhline(y=0, color='k')
        # plt.scatter([x/31536000 + 2001 for x in newdataz[:,0]],newdataz[:,1],s = 2)
        # plt.ylim(min(newdataz[:,1]),max(newdataz[:,1]))
        # plt.plot([x/31536000 + 2001 for x in plts[2]], [to_fit2( x, up[0], up[1], up[2], up[3]) for x in ts2z], color='r')
        # # gra[0].plot([plts[0][0], plts[0][-1]], [north[1], north[1] + north[0]*ts2x[-1]])
        # # gra[1].plot([plts[1][0], plts[1][-1]], [east[1], east[1] + east[0]*ts2y[-1]])
        # # gra[2].plot(plts[2][:], list(map(lambda x: to_fit(x, up[0], up[1], up[2], up[3]),ts2z)))
        # plt.show()
        return collection

def to_fit(x, a, b, c, d):
    return a + b*x + c*np.sin(2*math.pi/(365) * x + d)

def to_fit2(x, a, b, c, d):
    return a + b*x/(24*3600) + c*np.sin(2*math.pi/(365*24*3600) * x + d)

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
        tmp = p0 - elem.pos
        positions.append(np.matmul(mat, tmp))
        print(np.matmul(mat, tmp))
        pos = np.zeros([3])
        errors.append(elem.err)

    plotpos = np.array(positions)
    ploterr = np.array(errors)
    errors = np.array(errors)
    print(plotpos[:,2])
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

    f, axarr = plt.subplots(3, sharex=True)
    f.suptitle(sys.argv[1].split("/")[1][:4])
    # for i in range(0,3):
    #     axarr[i].axhline(y=0, color='k')
    #     axarr[i].set_xlim([times[0], times[-1]])
    #     axarr[i].errorbar(times, plotpos[:, i], yerr=errors[:,i], linewidth=0.5, fmt='x', markersize=0.81)

    for i in range(0,3):
        axarr[i].axhline(y=0, color='k')
        axarr[i].set_xlim([times[0], times[-1]])
        data = np.zeros([len(times), 2])
        t = [t.toordinal() for t in times]
        data[:, 0] = t
        data[:, 1] = plotpos[:,1]
        data = outlierdet(data, 3000, 1)
        axarr[i].scatter(data[:, 0], data[:, i], s=0.1)#, yerr=errors[:,i], linewidth=0.5, fmt='x', markersize=0.81)

    axarr[0].plot([mindate, times[-1]], [north[1], north[1] + north[0]*times2[-1]])
    axarr[1].plot([mindate, times[-1]], [east[1], east[1] + east[0]*times2[-1]])
    axarr[2].plot(times, list(map(lambda x: to_fit(x, up[0], up[1], up[2], up[3]), times2)))
    axarr[0].set_ylabel("North (m)")
    axarr[1].set_ylabel("East (m)")
    axarr[2].set_ylabel("Up (m)")

    plt.show()

if __name__ == "__main__":
    graph_series(parse_binary_llh(sys.argv[1]))
    
    