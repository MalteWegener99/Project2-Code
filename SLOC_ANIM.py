#begin: animate when stations supplied data to the time-series at least once a week
#move plotmap with ASDW-keys, zoom with IO-keys
import geoplotlib as gp
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv
from geoplotlib.layers import BaseLayer
from geoplotlib.core import BatchPainter
import glob, os, sys, csv, fnmatch
from graphing import parse_binary_llh
from math import degrees as deg
import numpy as np

#outlier func, n=800, sl=0.5
def outlierdet(data,n,sl,On = True):
    if On == True:
        d = data[:,1]
        avg_mask = np.ones(n)/n
        d_ave = np.convolve(d,avg_mask,mode = "same")
        diff = []
        for j in range(n//2,len(data[:,1]) - n//2):
            diff.append(abs(d_ave[j] - d[j]))
        sdev = np.std(diff)
        count = 0
        for i in range(n//2,len(data[:,1]) - n//2):
            if abs(d_ave[i] - d[i]) > (sl * sdev):
                data = np.delete(data,(i - count), axis = 0)
                count += 1

    return data

def conv_data(data,n):
    conv_mat = np.ones(n)/n
    d = data[:,1]
    d_ave = np.convolve(d,conv_mat,mode = "same")
    return ""

#path to converted files
path = os.path.dirname(os.path.realpath(__file__))+'/conv'
os.chdir(path)

#get locations and scaled velocity line of all stations from files
Locations = []
for file in os.listdir():
    if fnmatch.fnmatch(file, '*.neu'):
        Sname,T,N = file.split('.')
        Collection = parse_binary_llh(path+'/'+file)
        series = sorted(Collection, key=lambda x: x.time)
        #apply outlier detection and paste data into array
        Lat_locations,Lon_locations,times = [],[],[]
        for i in range(len(series)):

            ComT = series[i].time
            Year = (ComT-(ComT%1000))/1000
            Day = ComT%1000
            Year_len = 365*24*3600 + 5*3600 + 48*60 + 46
            Day_len = 23*3600 + 56*60 + 4
            Timestamp = int(((Year-1970)*Year_len) + (Day*Day_len))
            times.append(Timestamp)
            Lat_locations.append(deg(series[i].pos[0]))
            Lon_locations.append(deg(series[i].pos[1]))

        Lat_data = np.column_stack((times,Lat_locations))
        Lat_newdata = outlierdet(Lat_data,100,1,False)  
        Lon_data = np.column_stack((times,Lon_locations))
        Lon_newdata = outlierdet(Lon_data,100,1,False)

        Det_Dat = []
        for Tstamp in range(len(Lat_newdata)):
            if Lat_newdata[Tstamp][0] in Lon_newdata:
                Occ = np.where(Lon_newdata == Lat_newdata[Tstamp][0])[0][0]
                Det_Dat.append([Lat_newdata[Tstamp][0],Lat_newdata[Tstamp][1],Lon_newdata[Occ][1]])  
    
        for i in range(len(Det_Dat)):
            if 1 <= Det_Dat[i][1] <= 9 and 95 <= Det_Dat[i][2] <= 110:

                Timestamp = int(Det_Dat[i][0])

                S_startlat = Det_Dat[i][1]
                S_startlon = Det_Dat[i][2]
                lat_L,lon_L = [],[]
                for j in range(min(50, len(Det_Dat)-i-1)):
                    lat_L.append(Det_Dat[i+j+1][1])
                    lon_L.append(Det_Dat[i+j+1][2])
                S_destilat = np.mean(lat_L)
                S_destilon = np.mean(lon_L)
                scaled_S_destilat = S_startlat + ((S_destilat-S_startlat)*5000000)
                scaled_S_destilon = S_startlon + ((S_destilon-S_startlon)*5000000)

                Locations.append([Sname,S_startlat,S_startlon,scaled_S_destilat,scaled_S_destilon,Timestamp])

#path to SLOCs.csv
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#empty SLOCs.csv
f = open("SLOCs.csv", "w+")
f.close()

#write csv to be read by geoplotlib
with open('SLOCs.csv', mode='w', newline='') as SLOCs:
    SLOCs = csv.writer(SLOCs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    SLOCs.writerow(['name', 'Slat', 'Slon', 'Flat', 'Flon', 'timestamp'])
    for station in Locations:
        SLOCs.writerow(station)

#plot stations
class TrailsLayer(BaseLayer):

    def __init__(self):
        self.data = read_csv('SLOCs.csv')
        self.cmap = colorbrewer(self.data['name'], alpha=220)
        self.t = self.data['timestamp'].min()
        self.painter = BatchPainter()


    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        self.painter = BatchPainter()
        df = self.data.where((self.data['timestamp'] > self.t) & (self.data['timestamp'] <= self.t + 24*3600)) #set minimum time interval
        
        for name in set(df['name']):
            grp = df.where(df['name'] == name)
            self.painter.set_color('blue') #set color, default: self.cmap[name]
            x0, y0 = proj.lonlat_to_screen(grp['Slon'], grp['Slat'])
            x1, y1 = proj.lonlat_to_screen(grp['Flon'], grp['Flat'])
            self.painter.points(x0, y0, 3)
            self.painter.lines(x0,y0,x1,y1,width=2)

        self.t += 24*3600 #set animation step size

        if self.t > self.data['timestamp'].max():
            self.t = self.data['timestamp'].min()

        self.painter.batch_draw()
        ui_manager.info(epoch_to_str(self.t))


    def bbox(self):
        return BoundingBox(north=9, west=110, south=1, east=95) #set boundingbox


gp.add_layer(TrailsLayer())
gp.show()