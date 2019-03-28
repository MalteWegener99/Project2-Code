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
from fatiando import gridder
import matplotlib.animation as animation
import types


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
    dates = []
    phi = []
    lam = []
    h = []
    for elem in collection:
        if (get_date(elem)-start_date).days >= 0:
            dates.append((get_date(elem)-start_date).days)
            phi.append(elem.pos[0])
            lam.append(elem.pos[1])
            h.append(elem.pos[2])

    return (CubicSpline(dates, phi),CubicSpline(dates, lam), CubicSpline(dates, h), dates)

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
    for i in range(initial.shape[0]):
        initial[i,0] = splines[i][0](0)
        initial[i,1] = splines[i][1](0)
    
    triangulation = Delaunay(initial)
    connections = []
    for simplex in triangulation.simplices:
        connections.append(list(sorted([simplex[0],simplex[1]])))
        connections.append(list(sorted([simplex[1],simplex[2]])))
        connections.append(list(sorted([simplex[0],simplex[2]])))
    
    connections = np.unique(np.array(connections), axis=0)
    initial_dist = []
    for i in range(connections.shape[0]):
        initial_dist.append(great_circle_dist(initial[connections[i,0],:],initial[connections[i,1],:]))
    initial_dist = np.array(initial_dist)

    rng = (stop-start).days
    strain = np.zeros((connections.shape[0],1,rng))

    for t in range(0,rng):
        for i in range(connections.shape[0]):
            phi1 = splines[connections[i,0]][0](t)
            lam1 = splines[connections[i,0]][1](t)
            phi2 = splines[connections[i,1]][0](t)
            lam2 = splines[connections[i,1]][1](t)
            strain[i,0,t] = great_circle_dist([phi1,lam1],[phi2,lam2])/initial_dist[i]
    
    positions = []
    for i in range(connections.shape[0]):
        phi1 = splines[connections[i,0]][0](t)
        lam1 = splines[connections[i,0]][1](t)
        phi2 = splines[connections[i,1]][0](t)
        lam2 = splines[connections[i,1]][1](t)
        positions.append([(phi1+phi2)/2,(lam1+lam2)/2])
    print(len(positions))

    positions = np.array(positions)
    shape = (500,500)

    xp, yp, cubic = gridder.interp(positions[:,1], positions[:,0], strain[:,0,-1], shape, algorithm='cubic', extrapolate=False)

    pics = []
    fig, ax = plt.subplots() 
    vertices = triangulation.points
    simplices = triangulation.simplices
    minstrain = np.amin(strain)
    maxstrain = np.amax(strain)
    cs = 0
    legend = None
    def animate(t):
        ax.clear()
        date = start + datetime.timedelta(days=t)
        ax.set_title(date)
        a,b,th = gridder.interp(positions[:,1], positions[:,0],  strain[:,0,t], shape, algorithm='cubic', extrapolate=False)
        cs = ax.contourf(xp.reshape(shape), yp.reshape(shape), th.reshape(shape),200, cmap='jet', vmin=minstrain, vmax=maxstrain)
        grid = ax.triplot(vertices[:,1],vertices[:,0],simplices, linewidth=0.5)
        ax.axis('equal')
        if t != 0:
            legend.remove()
        legend = fig.colorbar(cs)

    ani = animation.FuncAnimation(fig, animate, frames=range(0,rng,7), interval=80, save_count=500, blit=False)
    #ani.save("move.mp4")
    plt.show()
        

    # cs = plt.contourf(xp.reshape(shape), yp.reshape(shape), cubic.reshape(shape),
    #             30, cmap='plasma')

    # plt.colorbar(cs)
    # vertices = triangulation.points
    # simplices = triangulation.simplices
    # plt.triplot(vertices[:,1],vertices[:,0],simplices, linewidth=0.5)
    # plt.scatter(positions[:,1],positions[:,0], s=0.3)
    # plt.axis('equal')
    # plt.show()

if __name__ == "__main__":
    analyse(r'malaysia.txt')