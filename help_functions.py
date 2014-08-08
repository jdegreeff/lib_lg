
import math


def calc_euclidean_distance(x, y):
    """ euclidean distance between x and y
    """
    if len(x) != len(y):
        raise ValueError, "vectors must be same length"
    total = 0
    for i in range(len(x)):
        total += ( x[i] -y[i])**2
    return math.sqrt(total)