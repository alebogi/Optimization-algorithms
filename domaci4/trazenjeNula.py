import numpy as np
import scipy.special as ss


# spherical Bessel function, n = 1 or n = 2
def f(n, x):
    return ss.spherical_jn(n, x)

def bisection(a, b, tolerance, n):
    xleft = a
    xright = b
    while (np.abs(xleft - xright) >= tolerance):
        c = (xleft + xright) / 2.0
        product1 = f(n, xleft)*f(n, c)
        product2 = f(n, xright) * f(n, c)
        if (product1 < 0):
            xright = c
        elif (product2 < 0):
            xleft = c
    return c

# main:
tolerance = 10e-12

# Za n=1, gledajuci grafik, zakljucujemo da se prva nula nalazi izmedju 2.5 i 5
# n=1, p=1 :
n1p1 = bisection(2.5, 5.0, tolerance, 1)
# Za n=1, gledajuci grafik, zakljucujemo da se druga nula nalazi izmedju 7.5 i 8
# n=1, p=2
n1p2 = bisection(7.5, 8.0, tolerance, 1)

print("Red funkcije n=1, redni broj nule p=1: ", n1p1)
print("Red funkcije n=1, redni broj nule p=2: ", n1p2)

# Za n=2, gledajuci grafik, zakljucujemo da se prva nula nalazi izmedju 5.0 i 7.5
# n=2, p=1 :
n2p1 = bisection(5.0, 7.5, tolerance, 2)
# Za n=2, gledajuci grafik, zakljucujemo da se druga nula nalazi izmedju 7.5 i 10
# n=2, p=2
n2p2 = bisection(7.5, 10.0, tolerance, 2)

print("Red funkcije n=2, redni broj nule p=1: ", n2p1)
print("Red funkcije n=2, redni broj nule p=2: ", n2p2)