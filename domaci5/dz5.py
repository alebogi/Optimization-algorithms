import matplotlib.pyplot as plt
import math
import numpy as np
import scipy.optimize as so

# Mreza treba da predstavlja aproksimaciju funkcije Ytraining
def y_training(x_in):
    res = math.sin(math.pi * x_in) / 2
    return res

# aktivaciona funkcija svakog cvora
def a(x):
    res = math.tanh(x)
    return res

def x(x_in, w):
    res = x_in * w
    return res

# vrednost na izlazu mreze
def y_out(x_in, Wlocal):
    sum = 0
    for k in range(1, 6):
        temp = a(x(x_in, Wlocal[k - 1])) * Wlocal[k + 5 - 1] # dodajemo -1 jer indeks niza krece od 0
        sum += temp
    res = a(sum)
    return res

# optimizaciona funkcija
def f_opt(w):
    # dif = y_out - y_training
    dif = 0.0
    # sq_dif = dif^2
    sq_dif = 0.0
    sum = 0.0
    res = 0.0
    # penalty - ako je w<-10 ili w>10 -> dodaj +200
    penalty = 200
    x_range = np.arange(-1, 1, 0.1)
    for x_in in x_range:
        dif = y_out(x_in, w) - y_training(x_in)
        sq_dif = dif * dif
        sum += sq_dif
    res = math.sqrt(sum)
    for w_k in w:
        if (w_k <= -10) or (w_k >= 10) :
            res += penalty
    return res

# --------------------------------------------
# main

# pocetne vrednosti
W = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]

result = so.minimize(f_opt, W, method='Nelder-Mead')
while (result.fun >= (10**-2)):
    result = so.minimize(f_opt, result.x, method='Nelder-Mead')

W = result.x

print("Koeficijenti:")

cnt = 1
for w_k in W:
    print("w", cnt, "=", end=" ")
    cnt += 1
    print("{:1.15f}".format(w_k))

print("\n w=(", end=" ")
cnt = 0
for w_k in W:
    print("{:1.15f}".format(w_k), end=" ")
    if (cnt < 9):
        print(", ", end="")
    else:
        print(")")
    cnt += 1


print("\nVrednost minimalne pronadjene optimizacione funkcije: ", result.fun)

# crtanje grafa:

#ulaz f-je za x-osu
plt.xlim(-1, 1)
x_range = np.arange(-1, 1, 0.01)

# iscrtavamo izlaz trening funkcije
line1 = []
for x_in in x_range:
    line1.append(y_training(x_in))
plt.plot(x_range, line1, label='${y}_{training}(x)$')

# iscrtavamo izlaz neuralne mreze
line2 = []
for x_in in x_range:
    line2.append(y_out(x_in, W))
plt.plot(x_range, line2, label='${y}_{out}(x)$')

# naming the x axis
plt.xlabel('x')
# naming the y axis
plt.ylabel('y')

# giving a title to my graph
plt.title("")

# show grid
plt.grid(b=True)

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()
