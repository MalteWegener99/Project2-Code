from graphing import parse_binary_llh
from outlier import outlierdet
import numpy as np
import sys
import datetime
import glob
import os
from matplotlib import pyplot as plt
from math import degrees as deg
from sklearn.cluster import AffinityPropagation
import matlab.engine
import scipy.io



def convolute(d,n):
    mask = np.ones(n)/n
    conv = np.convolve(d,mask,mode = "same")
    return conv


def seismic_act(data):
<<<<<<< HEAD
=======
    data = outlierdet(data,50,0.75)
>>>>>>> origin/vlad
    scipy.io.savemat("data.mat",{'data':data})
    eng = matlab.engine.start_matlab()
    eng.quakedet()
    quakes = scipy.io.loadmat("earthquakes.mat")['earthquakes']
    return quakes
    


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
<<<<<<< HEAD

    data = np.column_stack((times,locationsx,locationsy,locationsz))

    newdata = outlierdet(data,300,1)
    os.chdir("..")
    events  = seismic_act(data)

    print(events)
    
    # plt.subplot(3,2,6)
    # plt.scatter(times,locationsx,s = 0.1)
    # plt.ylim(min(locationsx),max(locationsx))
    # for event in events[0,:]:
    #     plt.axvline(event)

    # plt.subplot(3,2,4)
    # plt.scatter(times,locationsy,s = 0.1)
    # plt.ylim(min(locationsy),max(locationsy))
    # for event in events[0,:]:
    #     plt.axvline(event)
    
    # plt.subplot(3,2,2)
    # plt.scatter(times,locationsz,s = 0.1)
    # plt.ylim(min(locationsz),max(locationsz))
    # for event in events[0,:]:
    #     plt.axvline(event)

    # plt.subplot(3,2,5)
    # plt.scatter(newdata[:,0],newdata[:,1],s = 0.4)
    # plt.ylim(min(newdata[:,1]),max(newdata[:,1]))
    # for event in events[0,:]:
    #     plt.axvline(event)

    # plt.subplot(3,2,3)
    # plt.scatter(newdata[:,0],newdata[:,2],s = 0.4)
    # plt.ylim(min(newdata[:,2]),max(newdata[:,2]))
    # for event in events[0,:]:
=======

    data = np.column_stack((times,locationsx,locationsy,locationsz))

    newdata = outlierdet(data,50,0.75)
    os.chdir("..")
    events  = seismic_act(data)

    print(events)
    
    plt.subplot(2,1,1)
    plt.scatter(times,locationsx,s = 0.1)
    plt.ylim(min(locationsy),max(locationsy))
    for event in events[:,0]:
        plt.axvline(event)

    # plt.subplot(3,2,4)
    # plt.scatter(times,locationsy,s = 0.1)
    # plt.ylim(min(locationsy),max(locationsy))
    # for event in events[:,0]:
    #     plt.axvline(event)
    
    # plt.subplot(3,2,2)
    # plt.scatter(times,locationsz,s = 0.1)
    # plt.ylim(min(locationsz),max(locationsz))
    # for event in events[:,0]:
    #     plt.axvline(event)

    plt.subplot(2,1,2)
    plt.scatter(newdata[:,0],newdata[:,2],s = 0.4)
    plt.ylim(min(newdata[:,2]),max(newdata[:,2]))
    for event in events[:,0]:
        plt.axvline(event)

    # plt.subplot(3,2,3)
    # plt.scatter(newdata[:,0],newdata[:,2],s = 0.4)
    # plt.ylim(min(newdata[:,2]),max(newdata[:,2]))
    # for event in events[:,0]:
>>>>>>> origin/vlad
    #     plt.axvline(event)

    # plt.subplot(3,2,1)
    # plt.scatter(newdata[:,0],newdata[:,3],s = 0.4)
    # plt.ylim(min(newdata[:,3]),max(newdata[:,3]))
<<<<<<< HEAD
    # for event in events[0,:]:
    #     plt.axvline(event)

    # plt.autoscale(enable=True,axis = "y",tight=True)
    # plt.show()
=======
    # for event in events[:,0]:
    #     plt.axvline(event)

    # plt.autoscale(enable=True,axis = "y",tight=True)
    plt.show()
>>>>>>> origin/vlad
