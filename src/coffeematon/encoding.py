"""Tools to estimate the entropy and complexity of the cellular automaton."""


import gzip
import bz2
import tempfile
from enum import Enum
from typing import Union

import numpy
from PIL import Image

save_images = True


class Compression(Enum):
    BZIP = "bzip"
    GZIP = "gzip"


def zip_array(array, compression: Compression = Compression.GZIP) -> int:
    return zip_string(write_string(array), compression.value)


def zip_string(string: str, compression: Union[Compression, str]) -> int:
    byte_string = bytearray(string, "ascii")
    if Compression(compression) is Compression.GZIP:
        return len(gzip.compress(byte_string))
    if Compression(compression) is Compression.BZIP:
        return len(bz2.compress(byte_string))


def write_string(array):
    return " ".join([" ".join([str(x) for x in row]) for row in array])


def save_image(array, filename, n):
    data = numpy.ravel(array)
    image = Image.new("L", (n, n))
    image.putdata(data, 255, 0)
    image.save(filename)
