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


def convolute(d,n):
    mask = np.ones(n)/n
    conv = np.convolve(d,mask,mode = "same")
    return conv


# def seismic_act(data,n,sl):
#     data = outlierdet(data,n,1)
#     events,steps = [],[]
#     d_conv = data[:,1]
#     for i in range(n,len(d_conv)-n):
#         steps.append(abs((d_conv[i] - d_conv[i-1])/(data[i,0] - data[i-1,0])))
#     ave_step = sum(steps)/len(steps)
#     std_step = np.std(steps)
#     for i,step in enumerate(steps):
#         if step > (ave_step + sl*std_step):
#             ind = i + n
#             events.append(data[ind,0])
#     events = np.column_stack((events,np.ones(len(events))))
#     print(events)
#     clustering = AffinityPropagation(damping = 0.6).fit(events)
#     quakes = clustering.cluster_centers_
#     quakes = np.delete(quakes, 0 ,axis = 0)
#     print(quakes)
#     return quakes[:,0]

def seismic_act(data,sl):
    data = outlierdet(data,50,0.1)
    events = []
    d = data[:,1]
    steps = d[1:] - d[:-1]
    ratios = 1. * steps[1:] / steps[:-1]
    jumps = ratios[1:] - ratios[:-1]
    print(len(jumps))
    print(len(d))
    jump_ave = sum(jumps)/len(jumps)
    jump_dev = np.std(jumps)
    for i,jump in enumerate(jumps):
        if abs(jump) > (jump_ave + sl*jump_dev):
            events.append(data[i,0])
    return events

        
    


if __name__ == "__main__":
    path = "C:\\Users\\Wim Jodehl\\Desktop\\TAaS\\Project2-Code\\conv"
    os.chdir(path)

    collection = parse_binary_llh(path + "\\KUAL.tseries.neu")
    series = sorted(collection,key = lambda x: x.time)

    locations,times = [],[]
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
        locations.append(deg(series[i].pos[1]))

    data = np.column_stack((times,locations))

    newdata = outlierdet(data,300,1)
    events  = seismic_act(data,1)
    
    # print(events)
	
    plt.subplot(2,1,1)
    plt.scatter(times,locations,s = 0.1)
    for event in events:
        plt.axvline(x=event,color = "k")
    plt.ylim(min(locations),max(locations))
    
    plt.subplot(2,1,2)
    plt.scatter(newdata[:,0],newdata[:,1],s = 0.4)
    # for event in events:
        # plt.axvline(x=event,color = "k")
    plt.ylim(min(newdata[:,1]),max(newdata[:,1]))
 
    plt.show()