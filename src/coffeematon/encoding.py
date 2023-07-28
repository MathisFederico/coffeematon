"""Tools to estimate the entropy and complexity of the cellular automaton."""

import numpy
import os
import random
from PIL import Image

save_images = True


def zip_array(array, compression="gzip"):
    return zip_string(write_string(array), compression)


def zip_string(string, compression="gzip"):
    if compression == "bzip":
        return compressed_size(string, "bzip2", "bz2")
    if compression == "gzip":
        return compressed_size(string, "gzip", "gz")
    if compression == "compress":
        return compressed_size(string, "compress -f", "Z")


def compressed_size(string, cmd, ext):
    path = "temp" + str(random.randrange(1000))
    f = open(path, "w")
    f.write(string)
    f.close()
    os.system(cmd + " " + path)
    size = os.path.getsize(path + "." + ext)
    os.remove(path + "." + ext)
    return size


def write_string(array):
    return " ".join([" ".join([str(x) for x in row]) for row in array])


def save_image(array, filename, n):
    data = numpy.ravel(array)
    if 2.0 in data:
        scale = 127
    else:
        scale = 255
    image = Image.new("L", (n, n))
    image.putdata(data, scale, 0)
    image.save(filename)
