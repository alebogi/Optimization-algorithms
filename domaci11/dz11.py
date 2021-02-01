import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time

# globals
NUM_OF_POINTS = 10000
D = 2

# tacke
points_no_cond = np.zeros((NUM_OF_POINTS, D))
points_cond = np.zeros((NUM_OF_POINTS, D))

# vrednost opt.fja u tackama
value_no_cond = np.zeros((NUM_OF_POINTS, D))
value_cond = np.zeros((NUM_OF_POINTS, D))

# 1 ako je dominatno resenje, 0 ako nije
dom_no_cond = []
dom_cond = []

def generate_points(cond):
    global points_no_cond, points_cond

    genrated = 0
    while genrated < NUM_OF_POINTS:
        x1 = random.uniform(-1, 1)
        x2 = random.uniform(-1, 1)
        if cond == True:
            prod = x1 * x2
            if prod + (1/4) < 0:
                continue

        if cond == False:
            points_no_cond[genrated] = [x1, x2]
        else:
            points_cond[genrated] = [x1, x2]

        genrated = genrated + 1

def f1(x):
    res = 2 * pow(x[0], 2) + pow(x[1], 2)
    return res

def f2(x):
    res = - pow(x[0] - x[1], 2)
    return res

def opt_fun(cond):
    global points_no_cond, points_cond, value_cond, value_no_cond
    for i in range(NUM_OF_POINTS):
        if cond == False:
            x = points_no_cond[i]
            value_no_cond[i] = [f1(x), f2(x)]
        else:
            x = points_cond[i]
            value_cond[i] = [f1(x), f2(x)]

def find_dom(cond):
    global points_no_cond, points_cond, value_cond, value_no_cond, dom_cond, dom_no_cond
    for i in range(NUM_OF_POINTS):
        if cond == False:
            curr = value_no_cond[i]
            not_dom = False
            for j in range(NUM_OF_POINTS):
                if i != j:
                    tmp = value_no_cond[j]
                    if tmp[0] < curr[0] and tmp[1] < curr[1]:
                        not_dom = True
                        break
            if not_dom == True:
                dom_no_cond[i] = 0
            else:
                dom_no_cond[i] = 1
        else:
            curr = value_cond[i]
            not_dom = False
            for j in range(NUM_OF_POINTS):
                if i != j:
                    tmp = value_cond[j]
                    if tmp[0] < curr[0] and tmp[1] < curr[1]:
                        not_dom = True
                        break
            if not_dom == True:
                dom_cond[i] = 0
            else:
                dom_cond[i] = 1
    return

def draw_graph(cond):
    global value_cond, value_no_cond, dom_cond, dom_no_cond

    if cond == False:
        plt.figure(1)
        x = []
        y = []
        x_dom = []
        y_dom = []
        for i in range(NUM_OF_POINTS):
            if dom_no_cond[i] == 0:
                x.append(value_no_cond[i][0])
                y.append(value_no_cond[i][1])
            else:
                x_dom.append(value_no_cond[i][0])
                y_dom.append(value_no_cond[i][1])
        plt.scatter(x, y, label='Resenja')
        plt.scatter(x_dom, y_dom, label='Pareto front')
    else:
        plt.figure(2)
        x = []
        y = []
        x_dom = []
        y_dom = []
        for i in range(NUM_OF_POINTS):
            if dom_cond[i] == 0:
                x.append(value_cond[i][0])
                y.append(value_cond[i][1])
            else:
                x_dom.append(value_cond[i][0])
                y_dom.append(value_cond[i][1])
        plt.scatter(x, y, label='Resenja')
        plt.scatter(x_dom, y_dom, label='Pareto front')


    # naming the x axis
    plt.xlabel('${f}_1(x)$')
    # naming the y axis
    plt.ylabel('${f}_2(x)$')

    # giving a title to my graph
    if cond == False:
        plt.title("Pareto front - bez dodatnog uslova")
    else:
        plt.title("Pareto front - sa dodatnim uslovom")

    # show grid
    plt.grid(b=True)

    # show a legend on the plot
    plt.legend()


def main():
    global dom_cond, dom_no_cond
    startTime = time.time()

    for i in range(NUM_OF_POINTS):
        dom_cond.append(0)
        dom_no_cond.append(0)

    generate_points(False)
    opt_fun(False)
    find_dom(False)
    draw_graph(False)

    generate_points(True)
    opt_fun(True)
    find_dom(True)
    draw_graph(True)

    endTime = time.time()
    print("Vreme izvrsavanja: ", end="")
    print(endTime - startTime)
    plt.show()

# ------------------------------
if __name__ == '__main__':
    main()