import sys
import re
import os
import math
from math import sin,cos
import numpy as np
import time
import struct
from Sample import Sample, Sample_conv

# WGS 84
f = 1 / 298.257223563
e_2 = 2 * f - f**2
a = 6378137.  # SMA


def save_tseries_bin_llh(collection, output_folder):
    #collection = collection.sort(key=lambda x: x.time)
    name = collection[0].name
    file = open(output_folder + "/" + name + ".tseries.neu", 'wb')
    file.write(struct.pack('<q', len(collection)))
    for item in collection:
        file.write(struct.pack('<q', item.time))
        for i in range(0, 3):
            file.write(struct.pack('<d', item.pos[i]))

        for i in range(0, 3):
            file.write(struct.pack('<d', item.err[i]))

    file.close()


# https://gssc.esa.int/navipedia/index.php/Ellipsoidal_and_Cartesian_Coordinates_Conversion 
def xyz2llh(pos):
    # [phi, lambda, h]
    x, y, z = pos
    lam = math.atan(y/x)

    p = math.sqrt(x**2 + y**2)

    # inital calculation
    phi = math.atan(z/((1-e_2) * p))
    h = 0

    for i in range(10):
        N = a/(math.sqrt(1-e_2*((math.sin(phi))**2)))
        h = p/(math.cos(phi)) - N
        denom = 1-e_2*N/(N+h)
        phi = math.atan(z/(denom*p))

    return np.array([phi, lam, h])


def parse_binary(path) -> list:
    name = path.split('/')[-1][0:4]
    collection = []

    with open(path, 'rb') as file:
        n = file.read(8)
        n = struct.unpack('<q', n)[0]

        while True:
            time = file.read(8)
            time = struct.unpack('<q', time)[0]
            pos = np.zeros([3])
            mat = np.zeros([3, 3])
            for i in range(0, 3):
                tmp = file.read(8)
                tmp = struct.unpack('<d', tmp)[0]
                pos[i] = tmp

            for i in range(0, 3):
                for j in range(0, 3):
                    tmp = file.read(8)
                    tmp = struct.unpack('<d', tmp)[0]
                    mat[i, j] = tmp

            pos_f = file.tell()
            collection.append(Sample(name, time, pos, mat))
            if not file.read(1):
                return collection
            else:
                file.seek(pos_f)


def transform_list(collection) -> list:
    collector = []
    for item in collection:
        new_pos = xyz2llh(item.pos)
        phi, lam, h = new_pos
        mat = np.array([[-1*sin(lam), -1*sin(phi)*cos(lam), cos(phi)*cos(lam)],
                        [cos(lam), -1*sin(phi)*sin(lam), cos(phi)*sin(lam)],
                        [0, cos(phi), sin(phi)]])
        error = np.matmul(np.matmul(mat.T, item.mat), mat)
        error = np.matmul(error, new_pos)
        collector.append(Sample_conv(item.name, item.time, new_pos, error))
    return collector


def convert_file(file, output):
    save_tseries_bin_llh(transform_list(parse_binary(file)), output)


def convert_folder(path, output):
    files = list(filter(lambda x: re.match(r'[A-Z]{4}\.tseries$', x),
                   os.listdir(path)))

    dp = 1. / len(files)
    p = 0.
    for file in files:
        save_tseries_bin_llh(transform_list(parse_binary(path + '/' + file)), output)
        p += dp
        print("{0:.2%} done".format(p))


def main(argv):
    if argv[0] == '-f' or argv[0] == '--file':
        convert_file(argv[1], argv[2])
    else:
        start = time.time()
        convert_folder(argv[0], argv[1])
        print(time.time() - start)


if __name__ == "__main__":
    main(sys.argv[1:])