import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time

S = [2.424595205726587e-01, 1.737226395065819e-01, 1.315612759386036e-01,
 1.022985539042393e-01, 7.905975891960761e-02, 5.717509542148174e-02,
 3.155886625106896e-02, -6.242228581847679e-03, -6.565183775481365e-02,
 -8.482380513926287e-02, -1.828677714588237e-02, 3.632382803076845e-02,
 7.654845872485493e-02, 1.152250132891757e-01, 1.631742367154961e-01,
 2.358469152696193e-01, 3.650430801728451e-01, 5.816044173713664e-01,
 5.827732223753571e-01, 3.686942505423780e-01]

POPULATION_SIZE = 50
F = 0.8
CR = 0.9
MAX_ITER = 10**4
N = 20
R0 = 15
ACCEPTABLE_SOLUTION = pow(10, -14)
D = 6

gen = np.zeros((POPULATION_SIZE, D))
# xa = x_abc[0]
# xb = x_abc[1]
# xc = x_abc[2]
x_abc = np.zeros((3, D))

best_solution = []
min_solution_x = []
min_solution_opt_value = 100


def calculate_x_y(i):
    val = 2*math.pi*i/N
    x = R0 * math.cos(val)
    y = R0 * math.sin(val)
    return x, y

# x = (Xp1, Yp1, Xp2, Yp2, A1, A2)
#       0    1    2    3    4   5
def opt_fun(x):
    xp1 = x[0]
    yp1 = x[1]
    xp2 = x[2]
    yp2 = x[3]
    a1 = x[4]
    a2 = x[5]

    cond1 = math.sqrt(pow(xp1, 2) + pow(yp1, 2))
    cond2 = math.sqrt(pow(xp2, 2) + pow(yp2, 2))

    if((cond1 >= R0) or (cond2 >= R0)):
        return 100

    sum = 0
    for i in range(0, N):
        xi, yi = calculate_x_y(i)
        si = S[i]

        first = a1 / math.sqrt(pow(xi - xp1, 2) + pow(yi - yp1, 2))
        second = a2 / math.sqrt(pow(xi - xp2, 2) + pow(yi - yp2, 2))

        expression = pow(first + second - si, 2)

        sum = sum + expression

    return sum

def generate_initial_gen():
    global gen
    minValue = -15
    maxValue = 15
    for i in range(0, POPULATION_SIZE):
        xp1 = minValue + (random.random() * (maxValue - minValue))
        yp1 = minValue + (random.random() * (maxValue - minValue))
        xp2 = minValue + (random.random() * (maxValue - minValue))
        yp2 = minValue + (random.random() * (maxValue - minValue))
        a1 = minValue + (random.random() * (maxValue - minValue))
        a2 = minValue + (random.random() * (maxValue - minValue))

        x = [xp1, yp1, xp2, yp2, a1, a2]
        gen[i] = x
    return

def differential_evolution_algorithm():
    global gen, best_solution, x_abc, min_solution_x, min_solution_opt_value
    iter_cnt = 0
    y = [0, 0, 0, 0, 0, 0] # potancijalni clan nove populacije

    while iter_cnt < MAX_ITER:
        iter_cnt = iter_cnt + 1

        for ind_index in range(0, POPULATION_SIZE):
            individual = gen[ind_index]
            opt_fun_value = opt_fun(individual)
            if opt_fun_value <= ACCEPTABLE_SOLUTION:
                best_solution = individual
                return True # nasli optimalno resneje

            # pamtimo minimalno nadjeno resenje cisto da bismo videli ukoliko se dostigla max iteracija koja je nadjena vrednost
            if opt_fun_value < min_solution_opt_value:
                min_solution_opt_value = opt_fun_value
                min_solution_x = individual

            # SELEKCIJA
            cnt = 0
            while cnt < 3:
                index = random.randint(0, POPULATION_SIZE - 1)
                if index == ind_index:
                    continue
                else:
                    x_tmp = gen[index]
                  #  if x_tmp == individual:
                  #      continue
                  #  for j in range(cnt):
                  #      if x_tmp == x_abc[j]:
                  #          continue
                    x_abc[cnt] = x_tmp
                    cnt = cnt + 1

            # MEDJURESENJE
            # x = xa + F * (xb - xc)
            z = x_abc[0] + F * (x_abc[1] - x_abc[2])

            # UKRSTANJE
            R = random.randint(0, D)
            for el_index in range(0, D):
                elemenet = individual[el_index]
                ri = random.random()
                if ri < CR or el_index == R:
                    y[el_index] = z[el_index]
                else:
                    y[el_index] = individual[el_index]

            # PRIHVATA SE BOLJE RESENJE NA NIVOU CLANA POPULACIJE
            # imamo resenje individual(tekuce) i y (novo resenje)
            if opt_fun(y) < opt_fun(individual):
                gen[ind_index] = y
            # else -> ostaje isto

    return False  # nismo nasli optimalno resenje

def main():
    global gen
    generate_initial_gen()
    found_solution = differential_evolution_algorithm()
    if found_solution:
        print("Nadjeno je prihvatljivo resenje: ")
        print("x = ", end="")
        print(best_solution)
        print("Vrednost optimizacione funkcije za pronadjeno resenje: ", end="")
        print(opt_fun(best_solution))
    else:
        print("Nije nadjeno prihvatljivo resenje. Algoritam je stao jer je dostignuto " + str(MAX_ITER) + "iteracija")
        print("Nadjeno x = ", end="")
        print(min_solution_x)
        print("Vrednost optimizacione funkcije za pronadjeno resenje: ", end="")
        print(min_solution_opt_value)


# ------------------------------
if __name__ == '__main__':
    main()