"""Tools to estimate the entropy and complexity of the cellular automaton."""


import gzip
import bz2
from enum import Enum
from typing import Union
import numpy as np

save_images = True


class Compression(Enum):
    BZIP = "bzip"
    GZIP = "gzip"


def zip_array(
    array: np.ndarray, compression: Union[Compression, str] = Compression.GZIP
) -> int:
    return zip_bytes(array.tobytes(), compression)


def zip_string(
    string: str, compression: Union[Compression, str] = Compression.GZIP
) -> int:
    byte_string = bytearray(string, "ascii")
    return zip_bytes(byte_string, compression)


def zip_bytes(bytes: bytes, compression: Union[Compression, str]) -> int:
    if Compression(compression) is Compression.GZIP:
        return len(gzip.compress(bytes))
    if Compression(compression) is Compression.BZIP:
        return len(bz2.compress(bytes))


def write_string(array):
    return " ".join([" ".join([str(x) for x in row]) for row in array])
