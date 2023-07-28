"""
Accepts a dictionary mapping characters (code words) to frequencies
Outputs a mapping of those characters to binary strings
"""


def huffman(list):
    """accepts a list of characters (code words) then
    generates a list of their frequencies and encodes them"""
    cw_map = {}
    for item in list:
        cw_map[item] = cw_map.get(item, 0) + 1
    return encode(cw_map)


def encode(map):
    """accepts a dictionary mapping characters (code words) to frequencies
    outputs a mapping of those characters to binary strings"""
    output_map = {}
    map = tupleize(map)

    while len(map) > 1:
        # take 2 lowest-probability symbols from map
        s1 = argmin(map)
        f1 = map[s1]
        del map[s1]
        s2 = argmin(map)
        f2 = map[s2]
        del map[s2]

        # combine them into one node and replace into map
        s_new = s1 + s2
        f_new = f1 + f2
        map[s_new] = f_new

        # update the output map
        for key in s1:
            output_map[key] = "1" + output_map.get(key, "")
        for key in s2:
            output_map[key] = "0" + output_map.get(key, "")

    return output_map


def tupleize(dict):
    new_dict = {}
    for key in dict:
        new_dict[(key,)] = dict[key]
    return new_dict


def argmin(dict):
    min_key = None
    min_val = float("inf")
    for key in dict:
        if dict[key] < min_val:
            min_val = dict[key]
            min_key = key
    return min_key


if __name__ == "__main__":
    d = {"e": 3330, "h": 1458, "l": 1067, "o": 1749, "p": 547, "t": 2474, "w": 266}
    o = huffman(d)

    for key in o:
        print("%s: %s" % (key, o[key]))
