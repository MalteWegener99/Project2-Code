from Sample import Sample_conv
from graphing import parse_binary_llh
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import datetime
from utils import average_over
import numpy as np
from scipy.spatial import Delaunay
from math import sin, cos, sqrt, asin, acos
import scipy
import matplotlib.animation as animation
import types
from scipy.interpolate import interp1d
from scipy import signal
from outlier import outlierdet
import matplotlib

f = 1 / 298.257223563
e_2 = 2 * f - f**2
a = 6378137.  # SMA

def get_date(elem):
    year = elem.time//1000
    days = elem.time - year*1000
    date = datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + days - 1)
    return date

def make_spline(collection, start_date):
    collection = sorted(collection, key=lambda x: x.time)
    collection = average_over(collection, 7)
    dates = [0]
    phi = [collection[0].pos[0]]
    lam = [collection[0].pos[1]]
    h = [collection[0].pos[2]]
    for elem in collection:
        if (get_date(elem)-start_date).days >= 0:
            dates.append((get_date(elem)-start_date).days)
            phi.append(elem.pos[0])
            lam.append(elem.pos[1])
            h.append(elem.pos[2])
    s = 0
    smooth = 1000
    dev = 0.1
    cleanphi = outlierdet(np.array([dates,phi]).T,smooth,dev)
    cleanlam = outlierdet(np.array([dates,lam]).T,smooth,dev)
    n = 8
    return (scipy.interpolate.UnivariateSpline(cleanphi[:,0][::n], cleanphi[:,1][::n], k=2, s=s),scipy.interpolate.UnivariateSpline(cleanlam[:,0][::n], cleanlam[:,1][::n], k=2, s=s), scipy.interpolate.UnivariateSpline(dates, h, s=s), dates)

def load_set(file_name):
    stations_names = open(file_name).readlines()
    stations = dict()
    for name in stations_names:
        set = sorted(parse_binary_llh(r'conv/'+name[0:4]+'.tseries.neu'), key=lambda x: x.time)
        if (get_date(set[-1])-get_date(set[0])).days >= 1000:
            print(name[0:4])
            print(get_date(set[-1]))
            print(get_date(set[0]))
            stations[name[0:4]] = set
    
    min_date = max([get_date(stations[key][0]) for key in stations])
    max_date = min([get_date(stations[key][-1]) for key in stations])
    print(min_date)
    print(max_date)
    return stations, min_date, max_date

def make_spline_set(collection, min_date):
    col = []
    for key in collection:
        print(key)
        phi, lam, *throw = make_spline(collection[key], min_date)
        col.append([phi,lam])

    return col

def great_circle_dist(pos1, pos2):
    phi1, lam1 = pos1
    phi2, lam2 = pos2
    dellam = lam2-lam1
    t1 = cos(phi2)*cos(dellam)
    K = sin(phi2)*cos(phi1)-t1*sin(phi1)
    t2 = cos(phi2)*sin(dellam)
    cosc = sin(phi1)*sin(phi2)+t1*cos(phi1)
    sinc = sqrt(t2**2+K**2)
    psi = 0
    M = 0

    if sinc == 0:
        psi = 0
    else:
        L =asin(t2/sinc)
        if K>= 0:
            M = L
        elif K < 0:
            M = np.pi - L
        if M >= 0:
            psi = M
        else:
            psi = M + 2*np.pi

    c = asin(sinc)
    d = 0
    
    if cosc > 0:
        d = c
    else:
        cosc = -1*cosc
        d = np.pi-c
    
    return a * (d-f/4*((d+3*sinc)/(2*sin(d/2)**2)*(sin(phi1)-sin(phi2))**2+(d-3*sinc)/(1+cosc)*(sin(phi1)+sin(phi2))**2))


def analyse(file_name):
    #phi lam space
    data, start, stop = load_set(file_name)
    splines = make_spline_set(data, start)
    initial = np.zeros((len(splines), 2))
    print(len(splines))
    for i in range(initial.shape[0]):
        initial[i,0] = splines[i][0](1)
        initial[i,1] = splines[i][1](1)
    
    rng = (stop-start).days

    triangulation = Delaunay(initial)

    factor = 400000

    positions = np.zeros((initial.shape[0],initial.shape[1],rng))
    speed = np.zeros((initial.shape[0],initial.shape[1],rng))
    for t in range(1,rng-10,7):
        for i in range(0,positions.shape[0]):
            phi0 = initial[i,0]
            lam0 = initial[i,1]
            phi1 = splines[i][0](t)
            lam1 = splines[i][1](t)
            phiog = splines[0][0](t)-initial[0,0]
            lamog = splines[0][1](t)-initial[0,1]
            positions[i,0,t] = phi0 + factor*(phi1-phi0)#-phiog)
            positions[i,1,t] = lam0 + factor*(lam1-lam0)#-lamog)
            speed[i,0,t] = splines[i][0].derivative()(t)
            speed[i,1,t] = splines[i][1].derivative()(t)


    simplices = triangulation.simplices
    vertices = triangulation.points
    fig, ax = plt.subplots()
    print(positions.shape)
    speeds = [sqrt(speed[i,1,t]**2 + speed[i,0,t]**2) for i in range(0,speed.shape[0])]
    maxspeed = max(speeds)
    cmap = matplotlib.cm.get_cmap('rainbow')
    def animate(t):
        #ax.clear()
        date = start + datetime.timedelta(days=t)
        plt.title(date)
        plt.grid()
        plt.triplot(np.rad2deg(positions[:,1,t]),np.rad2deg(positions[:,0,t]),simplices, linewidth=1.0)
        plt.triplot(np.rad2deg(vertices[:,1]),np.rad2deg(vertices[:,0]),simplices, linewidth=0.5)
        plt.xlabel("Longitude [degrees]")
        plt.ylabel("Latitude [degrees]")
        print(speed[0,1,t], speed[0,0,t])
        for i in range(0,speed.shape[0]):
            mag = sqrt(speed[i,1,t]**2 + speed[i,0,t]**2)
            colr = cmap(mag/maxspeed)
            plt.quiver(np.rad2deg(positions[i,1,t]),np.rad2deg(positions[i,0,t]), speed[i,1,t], speed[i,0,t], colr, scale=0.8e-9)
        plt.axis('equal')

    #ani = animation.FuncAnimation(fig, animate, frames=range(1,rng-10,7), interval=100, save_count=500, blit=False)
    print(start)
    animate(50+28+91)#-91)
    #ani.save("move.mp4")
    plt.show()
        

    #cs = plt.contourf(xp.reshape(shape), yp.reshape(shape), cubic.reshape(shape),
                #30, cmap='plasma')

    #plt.colorbar(cs)
    #vertices = triangulation.points
    #simplices = triangulation.simplices
    #plt.triplot(vertices[:,1],vertices[:,0],simplices, linewidth=0.5)
    #plt.scatter(positions[:,1],positions[:,0], s=0.3)
    #plt.axis('equal')
    #plt.show()

if __name__ == "__main__":
    analyse(r'malaysia.txt')