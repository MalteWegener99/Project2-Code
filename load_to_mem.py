'''
Loading XYZ files into memory
Use PEP8 for editing this file

'''

import numpy as np

"""
Files look like this:
Header
ID STATION STA [X,Y,Z] value +- devi
ID1 ID2 COV
if a line contains a '+-' its always a value
"""


class Sample:
    '''
    Container for saving a sample in time
    time: uint: dayE2 + Year(last 2 digits)
    '''
    def __init__(self, name, time, xyz, mat):
        self.name = name
        self.time = time
        self.xyz = xyz
        self.mat = mat

    def __str__(self):
        return "{} was on position {} on {} \r\n with deviations: \r\n{}"\
                .format(self.name, self.xyz, self.time, self.mat)


def parse_file(file_name: str) -> []:
    '''
    Loads a file and returns a list of Sample
    '''

    time = int(file_name[-3:-1]) + int(file_name[-7:-4]) * 100

    collector = []
    file = open(file_name)
    lines = file.readlines()

    # remove header
    lines = lines[1:]
    n_stations = len(lines)//3//2

    # proceed in multiples of 3
    for i in range(0, n_stations * 3, 3):
        val = 4
        dev = 6
        xsplit = lines[i].split()
        ysplit = lines[i+1].split()
        zsplit = lines[i+2].split()
        name = xsplit[1]
        x = float(xsplit[val])
        y = float(ysplit[val])
        z = float(zsplit[val])
        xx = float(xsplit[dev])
        yy = float(ysplit[dev])
        zz = float(zsplit[dev])

        cov1split = lines[i + n_stations*3].split()
        cov2split = lines[i + n_stations*3 + 1].split()
        cov3split = lines[i + n_stations*3 + 2].split()

        xy = float(cov1split[2])
        xz = float(cov2split[2])
        yz = float(cov3split[2])

        pos = np.array([x, y, z])
        covariance = np.array([[xx, xy, xz],
                               [xy, yy, yz],
                               [xz, yz, zz]])

        collector.append(Sample(name, time, pos, covariance))

    return collector

parsed = parse_file("/home/malte/Desktop/project/data/PZITRF08361.06X")
for parse in parsed:
    print(parse)

