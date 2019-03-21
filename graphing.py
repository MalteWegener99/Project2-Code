from Sample import Sample_conv
import matplotlib.pyplot as plt
import numpy as np
import sys
import struct
import datetime

def parse_binary_llh(path):
    name = path.split('/')[-1][0:4]
    collection = []

    with open(path, 'rb') as file:
        n = file.read(8)
        n = struct.unpack('<q', n)[0]

        for i in range(0,n):
            time = file.read(8)
            time = struct.unpack('<q', time)[0]
            print(time)
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

        return collection

def graph_series(series):
    series = sorted(series, key=lambda x: x.time)
    mindate = series[0].time

    positions = []
    times = []
    for elem in series:
        positions.append(list(elem.pos))
        year = elem.time//1000
        days = elem.time - year*1000
        print(days)
        times.append(datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + days - 1))

    positions = np.array(positions)
    f, axarr = plt.subplots(3, sharex=True)
    f.suptitle('Sharing X axis')
    axarr[0].plot(times, positions[:, 0])
    axarr[1].plot(times, positions[:, 1])
    axarr[2].plot(times, positions[:, 2])
    plt.show()

graph_series(parse_binary_llh(sys.argv[1]))