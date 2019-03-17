from Sample import Sample
from xyz2llh import parse_binary
import matplotlib.pyplot as plt
import numpy as np


def graph_series(series):
    series = sorted(series, key=lambda x: x.time)
    mindate = series[0].time
    for elem in series:    
        elem.time -= mindate
    positions = []
    times = []
    for elem in series:
        positions.append(list(elem.pos))
        times.append(elem.time)

    positions = np.array(positions)
    f, axarr = plt.subplots(3, sharex=True)
    f.suptitle('Sharing X axis')
    axarr[0].plot(times, positions[:, 0])
    axarr[1].plot(times, positions[:, 1])
    axarr[2].plot(times, positions[:, 2])
    plt.show()

graph_series(parse_binary(r'/home/malte/Desktop/project/t_conv/MERU.tseries_llh'))