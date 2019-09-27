import json


def prettyprint(string):
    string = json.dumps(string, indent=4, sort_keys=True)
    print(string)


def sci_not_converter(info_tuple):
    """
    Scientific notation converter (ie standard form)
    for converting response
    :param info_tuple: tuple, first value is a number, (eg) if 4 meaning "e4" (ie power of 4), so we have to divide by
    10000 to get the true value. the number indicates the number of zeroes
    :return: the true value
    """
    power = int(str(info_tuple[0])[-1])

    x = "1"
    # convert single digit power to base 10
    for y in range(power):
        x += "0"
    x = int(x)  # convert to int to be used in calculation
    true_value = info_tuple[1] / x
    return true_value
