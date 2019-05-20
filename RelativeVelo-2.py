import numpy as np
import glob, os, sys, csv, fnmatch
import datetime
from math import cos, sin,atan
import math
import matplotlib.dates as dates
import matplotlib.pyplot as plt

def Trans_Velo_csv(fname):
    OGcsv = np.genfromtxt(fname,dtype=str,skip_header = 1,delimiter=',')
    namel = OGcsv[:,0] 
    OGcsv = np.genfromtxt(fname,dtype=float,skip_header = 1,delimiter=',')
    longl = (OGcsv[:,2])
    latl = (OGcsv[:,1])
    tl = (OGcsv[:,5])
    
    vell = [] #Name, Vlat, Vlong, Date
 
    
    for i in range(1,OGcsv[:,0].size):
        if namel[i] == namel[i-1]:
            vlat = (latl[i]-latl[i-1])/(tl[i]-tl[i-1])
            vlong = (longl[i]-longl[i-1])/(tl[i]-tl[i-1])
            vell.append([namel[i],vlat,vlong,tl[i]])

    #path to SLOCs.csv
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    #empty SLOCs.csv
    f = open("Trans_Velo.csv", "w+")
    f.close()

    #write csv to be read by geoplotlib
    with open("Trans_Velo.csv", mode='w', newline='') as Trans:
        Trans = csv.writer(Trans, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Trans.writerow(['name', 'Vlat', 'Vlong', 'timestamp'])
        for station in vell:
            Trans.writerow(station)

    return min(tl),max(tl)

def Trans_Avg_Velo_csv():
    OGcsv = np.genfromtxt("Trans_Velo.csv",dtype=str,skip_header = 1,delimiter=',')
    namel = OGcsv[:,0] 
    OGcsv = np.genfromtxt("Trans_Velo.csv",dtype=float,skip_header = 1,delimiter=',')
    longl = (OGcsv[:,2])
    latl = (OGcsv[:,1])
    tl = (OGcsv[:,3])   

    step = (31*24*60*60)
    velal = []
    for i in range(int(min(tl)),int(max(tl)),step):
        latsum = []
        longsum = []
        for j in range(longl.size):
            if tl[j] > i and tl[j]<(i+step):
                latsum.append(latl[j])
                longsum.append(longl[j])
        velal.append([(sum(latsum)/len(latsum)),(sum(longsum)/len(longsum)),i])

    #path to SLOCs.csv
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    #empty SLOCs.csv
    f = open("Trans_Avg_Velo.csv", "w+")
    f.close()

    #write csv to be read by geoplotlib
    with open("Trans_Avg_Velo.csv", mode='w', newline='') as Trans:
        Trans = csv.writer(Trans, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Trans.writerow(['VAlat', 'VAlong', 'timestamp'])
        for station in velal:
            Trans.writerow(station)

def Rel_Vel():
    OGcsv = np.genfromtxt("Trans_Avg_Velo.csv",dtype=float,skip_header = 1,delimiter=',')#VAlat,VAlong,timestamp
    longlavg = (OGcsv[:,1])
    latlavg = (OGcsv[:,0])
    tlavg = (OGcsv[:,2]) 
    
    OGcsv = np.genfromtxt("Trans_Velo.csv",dtype=str,skip_header = 1,delimiter=',')
    namel = OGcsv[:,0] 
    OGcsv = np.genfromtxt("Trans_Velo.csv",dtype=float,skip_header = 1,delimiter=',')
    longl = (OGcsv[:,2])
    latl = (OGcsv[:,1])
    tl = (OGcsv[:,3])
    
    vrell = []
    for i in range(namel.size):
        check = []
        for j in range(longlavg.size):
            check.append(abs(tlavg[j]-tl[i]))
        pos = check.index(min(check)) 
        vrell.append([namel[i],latl[i]-latlavg[pos],longl[i]-longlavg[pos],tl[i]])

    #path to SLOCs.csv
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    #empty SLOCs.csv
    f = open("Trans_Rel_Velo.csv", "w+")
    f.close()

    #write csv to be read by geoplotlib
    with open("Trans_Rel_Velo.csv", mode='w', newline='') as Trans:
        Trans = csv.writer(Trans, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Trans.writerow(['Name','VRlat', 'VRlong', 'timestamp'])
        for station in vrell:
            Trans.writerow(station)

def plot_rel(s_name): 
    OGcsv = np.genfromtxt("Trans_Rel_Velo.csv",dtype=str,skip_header = 1,delimiter=',')
    namel = OGcsv[:,0]
 
    
    OGcsv = np.genfromtxt("Trans_Rel_Velo.csv",dtype=float,skip_header = 1,delimiter=',')#VAlat,VAlong,timestamp
    longlrel = (OGcsv[:,2])
    latlrel = (OGcsv[:,1])
    
    OGcsv = np.genfromtxt("Trans_Rel_Velo.csv",dtype=int,skip_header = 1,delimiter=',')
    tlrel = (OGcsv[:,3])     

    latl = []
    longl = []
    interval = []
    rotation = []
    magl = []
    tl = []
    for i in range(1,namel.size):
        if s_name == s_name: #namel[i-1]
            latl.append(latlrel[i-1]*60*60*24*365)
            longl.append(longlrel[i-1]*60*60*24*365)
            magl.append(math.sqrt((longlrel[i-1]*60*60*24*365)**2 + (latlrel[i-1]*60*60*24*365)**2))
            tl.append(datetime.date.fromtimestamp(tlrel[i-1]))
            #print(tl[i])


    plt.close('all')
    fig, ax = plt.subplots(1,1)
    ax.plot(tl, magl, linewidth=0.3)    
    #fig = plt.scatter(tl, magl, linewidth=0.3, color = (0.8,0,0.6))
    #.plot(tl,longl, linewidth=0.3,color='y')
    ax.set_xlabel('Dates')
    ax.set_ylabel('latitudinal velocity')
    #ax2.set_xlabel('Dates')
    #ax2.set_ylabel('longitudinal velocity')
    # rotate and align the tick labels so they look better
    #fig.autofmt_xdate()

    # use a more precise date string for the x axis locations in the
    # toolbar
    import matplotlib.dates as mdates
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    #ax2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.title('Relative displacement per unit time')
    plt.show()


"""MAIN CODE"""
fname = 'conv\SLOCs.csv'
s_name = 'BAKO'
#Trans_Velo_csv(fname)
#Trans_Avg_Velo_csv()
#Rel_Vel()
plot_rel(s_name)
