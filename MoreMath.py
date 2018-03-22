from fractions import Fraction
from functools import reduce

def nCk(n, k):
    return int(reduce(lambda x, y: x*y , (Fraction(n-i, i+1) for i in range(k)), 1))
