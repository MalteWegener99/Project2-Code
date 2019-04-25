from graphing import parse_binary_llh
from outlier import outlierdet
import numpy as np
import sys
import datetime
import glob
import os
from matplotlib import pyplot as plt
from math import degrees as deg

def seismic_act(data,rng,sl):
    comp_data = data
    events,diffs = [],[]
    for i in range(rng//2,len(comp_data[:,1]) - rng//2):
        avs = []
        for j in range(1,rng//2):
            avs.append(abs(comp_data[i,1] - comp_data[i-j,1]))
            avs.append(abs(comp_data[i,1] - comp_data[i+j,1]))
        diffs.append(sum(avs)/len(avs))
    sdev = np.std(diffs)
    mean = sum(diffs)/len(diffs)
    for k,diff in enumerate(diffs):
        if diff > (mean + sl*sdev) or diff < (mean - sl*sdev):
            events.append(comp_data[k+rng//2,0])
    return events
    



        
    


if __name__ == "__main__":
    path = "C:\\Users\\Wim Jodehl\\Desktop\\TAaS\\Project2-Code\\conv"
    os.chdir(path)

    collection = parse_binary_llh(path + "\\MERS.tseries.neu")
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
        locations.append(deg(series[i].pos[0]))

    data = np.column_stack((times,locations))

    newdata = outlierdet(data,300,1)
    events  = seismic_act(data,50,9)
	
    plt.subplot(2,1,1)
    plt.scatter(times,locations,s = 0.1)
    for event in events:
        plt.axvline(x=event,color = "k")
    plt.ylim(min(locations),max(locations))
    
    plt.subplot(2,1,2)
    plt.scatter(newdata[:,0],newdata[:,1],s = 0.4)
    for event in events:
        plt.axvline(x=event,color = "k")
    plt.ylim(min(newdata[:,1]),max(newdata[:,1]))

    
    plt.show()