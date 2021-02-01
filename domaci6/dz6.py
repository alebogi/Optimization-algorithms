import math
import numpy as np
import scipy.optimize as so

# prvo definisemo uslove koji su neophodni za resavanje zadatka:

# Uslovi za maksimalan broj servera po ormarima:
# x11 + x12 + x13 + x14 <= 10
# x21 + x22 + x23 + x24 <= 16
# x31 + x32 + x33 + x34 <= 8

# Uslovi za maksimalnu snagu po ormarima:
# 480*x11 + 650*x12 + 580*x13 + 390*x14 <= 6800
# 480*x21 + 650*x22 + 580*x23 + 390*x24 <= 8700
# 480*x31 + 650*x32 + 580*x33 + 390*x34 <= 4300

# Uslovi za broj servera na raspolaganju:
# x11 + x21 + x31 <= 18
# x12 + x22 + x32 <= 15
# x13 + x23 + x33 <= 23
# x14 + x24 + x34 <= 12

# Iz ovih nejednacina dobijamo matrice uslova:

# Jedan red je oblika [x11, x12, x13, x14,  x21, x22, x23, x24,  x31, x32, x33, x34]
# A predstavlja levu stranu uslova
A = np.array([
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [480, 650, 580, 390, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 480, 650, 580, 390, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 480, 650, 580, 390],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
])

# b predstavlja desnu stranu uslova
b = np.array([
    [10],
    [16],
    [8],
    [6800],
    [8700],
    [4300],
    [18],
    [15],
    [23],
    [12]
])

# treba maksimizirati
capacity = np.array([310, 380, 350, 285, 310, 380, 350, 285, 310, 380, 350, 285])

# Funkcija koja proverava da li je uslov ispunjen
def meets_the_condition(x):
    res = True;
    for i in range(0, 10):
        prod = np.matmul(A[i], x)
        if (prod > b[i]):
            res = False;
    return res

# Funkcija koja racuna kapacitet
def count_capacity(x):
    prod = np.matmul(capacity, x)
    return prod

#----- main -----

result = so.linprog(-capacity, A, b)
# dobijamo resenje sa realnim brojevima
x_real = result.x
max_capacity_real = result.fun

print("Realno resenje:")
print("Optimalan raspored servera po ormarima:")
print("(", end="")
for i in range(0, 12):
    print(x_real[i], end="")
    if((i % 4) == 3):
        if (i != 11):
            print(",  ", end="")
        else:
            print(")")
    else:
        print(", ", end="")
print("Maksimalni ostvareni racunarski kapacitet sistema: ", -max_capacity_real, "\n\n----------------\n")

x_int = [] # sadrzi samo int brojeve, finalno resenje
x_real_int = x_real.copy() # sadrzi i real i int brojeve, sluzi dok pronalazimo resenje
my_max_capacity_with_ints = 0 # za racunanje kapaciteta pri pronalazenju novog resenja

# Za sve realne brojeve vece od nule treba proveriti tri manja i tri veca cela broja
# x_real je oblika [x11, x12, x13, x14,  x21, x22, x23, x24,  x31, x32, x33, x34]

# Ukoliko je iza decimalne tacke broj manji od 10e-7 to mozemo smatrati celim brojem i zaokruziti ga
for i in range(0, 12):
    tek = x_real[i] #broj koji trenutno obradjujemo
    if (math.modf(tek)[0] <= 10e-7): # math.modf vraca tuple oblika (fractional, whole), a nama treba fractional deo
        x_real_int[i] = int(round(x_real[i]))

# print("X-real-int", x_real_int)
# Rezultat naredbe:
# [ 0.         10.          0.          0.          0.          3.14859997
#   8.63875793  4.2126421   0.          1.85140003  3.67703154  2.47156843]

# Za ostale brojeve koji nisu zaokruzeni moramo da gledamo okolinu (+-3), i da proveravamo da li i dalje ispunjavaju uslov
# To su brojevi sa indeksima 5, 6, 7, 9, 10, 11
# int ce zaokruziti broj na donju cifru, i potom gledamo range od -3 do +3 broja
for i in range(int(x_real[5])-3, int(x_real[5])+4):
    for j in range(int(x_real[6])-3, int(x_real[6])+4):
        for k in range(int(x_real[7])-3, int(x_real[7])+4):
            for l in range(int(x_real[9])-3, int(x_real[9])+4):
                for m in range(int(x_real[10])-3, int(x_real[10])+4):
                    for n in range(int(x_real[11])-3, int(x_real[11])+4):
                        x_real_int[5] = i
                        x_real_int[6] = j
                        x_real_int[7] = k
                        x_real_int[9] = l
                        x_real_int[10] = m
                        x_real_int[11] = n
                        if(meets_the_condition(x_real_int)):
                             tmp_capacity = count_capacity(x_real_int)
                             if(my_max_capacity_with_ints < tmp_capacity):
                                 my_max_capacity_with_ints = tmp_capacity
                                 x_int = x_real_int.copy()



# Kada bih uradila samo print(x_int), onda bi lepo ispisao sve brojeve, a kada radim ispis kao trenutni (ispisujem posebno svaki x_int[i]), tada
# iako je vec celobrojni broj, iz nekog razloga sam imala problema.
# Ne znam zasto uporno neke brojeve zapisuje kao npr 9.9999999 umesto 10.0 (verovatno zbog onog problema sa smestanjem realnih brojeva u racunaru),
# a pri pokusaju kastovanja kastuje u 9, a ne u 10.
# Tako da za svaki slucaj radim round u petlji.
# Inace ispis naredbe print(x_int) je:
# [ 0. 10.  0.  0.  0.  2. 10.  4.  0.  3.  2.  3.]
# ali sam zelela da stilizujem ispis.

print("Celobrojno resenje:")
print("Optimalan raspored servera po ormarima:")
print("(", end="")
for i in range(0, 12):
    x_int[i] = round(x_int[i])
    print(x_int[i], end="")
    if((i % 4) == 3):
        if (i != 11):
            print(",  ", end="")
        else:
            print(")")
    else:
        print(", ", end="")

my_max_capacity_with_ints = count_capacity(x_int)
print("Maksimalni ostvareni racunarski kapacitet sistema: ", my_max_capacity_with_ints)