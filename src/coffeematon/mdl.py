"""
Library to compute the approximate sophistication of a binary string
using a two-part coding algorithm from Evans, Saulnier, and Bush.
"""


from coffeematon.encoding import write_string
from coffeematon.huffman import huffman, argmin
from math import log


def encoded_sizes(array):
    string = write_string(array)

    (model, encoded_string) = oscr_encode(string)
    code = huffman(encoded_string)

    # size of OSCR codebook (the sum of the symbol and Huffman codeword sizes)
    # is the "useful" information in the string, an approximation of sophistication.
    model_size = sum([len(x) for x in model.values()])
    code_size = sum([len(x) for x in code.values()])
    soph = model_size + code_size

    # size of string itself is the "incidental" information of the string.
    # sum of incidental and useful information is an approximation of
    # Kolmogorov complexity.
    k = len(encoded_string) + soph

    return (soph, k)


def oscr_encode(string):
    model = {}  # mapping from indices to original substrings
    i = 0  # next available replacement symbol
    encoded = [string]
    min_symbol_len = 2
    max_symbol_len = 400

    while has_binary(encoded):
        # find all substrings for all strings left in encoded
        counts = substring_counts(encoded, min_symbol_len, max_symbol_len)

        # compute SCRs for each of the substrings; pick one with lowest SCR
        scrs = {}
        for substring in counts:
            scrs[substring] = scr(substring, counts[substring], len(string))
        best_substring = argmin(scrs)
        # debug
        if len(best_substring) >= 50:
            print(len(best_substring))

        # if there are no more symbols with length > 1 that will improve
        # the compression factor, use length 1 symbols
        if (best_substring is None) or (
            scrs[best_substring] >= 1 and min_symbol_len == 2
        ):
            min_symbol_len = 1
            max_symbol_len = 1
            continue

        # replace best substring in the encoded string, and add to model
        new = []
        for symbol in encoded:
            if not isinstance(symbol, str):
                new += [symbol]
            else:
                new += replace_list(symbol, best_substring, i)
        encoded = new
        model[i] = best_substring
        i += 1

    return (model, encoded)


def scr(symbol, r, L):
    return (r * (log(L / 2.0, 2) - log(r, 2)) + len(symbol)) / (float(len(symbol)) * r)


def replace_list(string, substring, replace):
    ret = []
    buf = ""
    while len(string) >= len(substring):
        if string[0 : len(substring)] == substring:
            if len(buf) != 0:
                ret += [buf]
            ret += [replace]
            string = string[len(substring) :]
            buf = ""
        else:
            buf += string[0]
            string = string[1:]
    if len(string) > 0:
        buf += string
    if len(buf) != 0:
        ret += [buf]
    return ret


def substring_counts(string_list, min_len, max_len):
    # generate the set of all substrings that exist in the string list
    substring_set = {}
    for string in string_list:
        if not isinstance(string, str):
            continue
        for length in range(min_len, min(len(string), max_len) + 1):
            substrs = substrings(string, length)
            for substring in substrs:
                substring_set[substring] = True
    # count the number of non-overlapping repetitions of those strings
    counts = {}
    for string in string_list:
        if not isinstance(string, str):
            continue
        for substring in substring_set:
            counts[substring] = counts.get(substring, 0) + string.count(substring)
    return counts


def has_binary(list):
    for item in list:
        if isinstance(item, str):
            return True
    return False


def substrings(string, length):
    return [string[i : i + length] for i in range(len(string) - length + 1)]


##########
## MAIN ##
##########

if __name__ == "__main__":
    x = ("1" * 200) + ("0" * 200)
    # print encoded_sizes(x)
    print(scr("1111", 50, 400))
    print(scr("11111111", 25, 400))
    print(scr("1111111111111111111111111", 8, 400))
