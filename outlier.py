from graphing import parse_binary_llh
import numpy as np
import sys
import datetime
import glob
import os
from matplotlib import pyplot as plt
from math import degrees as deg
from sklearn.cluster import AffinityPropagation
import matlab.engine
import matlab





def outlierdet(data,n,sl):
    dx = data[:,1]
    dy = data[:,2]
    dz = data[:,3]

    avg_mask = np.ones(n)/n

    d_ave_x = np.convolve(dx,avg_mask,mode = "same")
    d_ave_y = np.convolve(dy,avg_mask,mode = "same")
    d_ave_z = np.convolve(dz,avg_mask,mode = "same")

    diffx = []
    diffy = []
    diffz = []

    for j in range(n//2,len(data[:,1]) - n//2):
        diffx.append(abs(d_ave_x[j] - dx[j]))
        diffy.append(abs(d_ave_y[j] - dy[j]))
        diffz.append(abs(d_ave_z[j] - dz[j]))
    
    sdevx = np.std(diffx)
    sdevy = np.std(diffy)
    sdevz = np.std(diffz)

    count = 0

    for i in range(n//2,len(data[:,1]) - n//2):
        bool_x = (abs(d_ave_x[i] - dx[i]) > (sl * sdevx))
        bool_y = (abs(d_ave_y[i] - dy[i]) > (sl * sdevy))
        bool_z = (abs(d_ave_z[i] - dz[i]) > (sl * sdevz))

        if bool_x or bool_y or bool_z:
            data = np.delete(data,(i - count), axis = 0)
            count += 1


    return data

if __name__ == "__main__":
    path = "C:\\Users\\Wim Jodehl\\Desktop\\TAaS\\Project2-Code\\conv"
    os.chdir(path)

    collection = parse_binary_llh(path + "\\KUAL.tseries.neu")
    series = sorted(collection,key = lambda x: x.time)

    locationsx,locationsy,locationsz,times = [],[],[],[]
    init_time = series[0].time
    init_year = init_time//1000
    init_days = init_time - init_year*1000
    init_date = datetime.date.fromordinal(datetime.date(init_year,1,1).toordinal()+ init_days - 1)

    for i in range(len(series)):

        ts = series[i].time
        year = ts//1000
        days = ts - year*1000
        date = datetime.date.fromordinal(datetime.date(year,1,1).toordinal()+ days - 1)
        time = (date - init_date).total_seconds()
        times.append(time)
        locationsx.append(deg(series[i].pos[0]))
        locationsy.append(deg(series[i].pos[1]))
        locationsz.append(deg(series[i].pos[2]))

    data = np.column_stack((times,locationsx,locationsy,locationsz))

    newdata = outlierdet(data,300,1)

    
    
    plt.subplot(3,2,6)
    plt.scatter(times,locationsx,s = 0.1)
    plt.ylim(min(locationsx),max(locationsx))

    plt.subplot(3,2,4)
    plt.scatter(times,locationsy,s = 0.1)
    plt.ylim(min(locationsy),max(locationsy))
    
    plt.subplot(3,2,2)
    plt.scatter(times,locationsz,s = 0.1)
    plt.ylim(min(locationsz),max(locationsz))

    plt.subplot(3,2,5)
    plt.scatter(newdata[:,0],newdata[:,1],s = 0.4)
    plt.ylim(min(newdata[:,1]),max(newdata[:,1]))

    plt.subplot(3,2,3)
    plt.scatter(newdata[:,0],newdata[:,2],s = 0.4)
    plt.ylim(min(newdata[:,2]),max(newdata[:,2]))

    plt.subplot(3,2,1)
    plt.scatter(newdata[:,0],newdata[:,3],s = 0.4)
    plt.ylim(min(newdata[:,3]),max(newdata[:,3]))

    # plt.autoscale(enable=True,axis = "y",tight=True)
    plt.show()
