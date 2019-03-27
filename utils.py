from Sample import Sample_conv
import numpy as np

def average_over(collection: list, n: int) -> list:
    collector = []
    for i in range(n-1,len(collection), n):
        pos = np.zeros([3])
        err = np.zeros([3])
        for j in range(0,n):
            pos += collection[i-j].pos
            err += collection[i-j].err
        collector.append(Sample_conv(collection[i].name, collection[i-3].time, pos/n, err/n))

    return collector

