import numpy as np
import math
import random
import time

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# globals
A_POINT = Point(1, 5, 1)
B_POINT = Point(3, 2, 0)
C_POINT = Point(5, 7, 1)
D_POINT = Point(6, 3, 3)

g_best = np.array([0, 0, 0, 0, 0, 0])


g_best_value = float("inf")

W = 0.729
C1 = C2 = 1.494

NUM_OF_AGENTS = 50
D = 3

gen = np.zeros((NUM_OF_AGENTS, D))

MAX_ITER = 10000

class Agent:
    def __init__(self, point1, point2):
        self.curr = np.array([point1.x, point1.y, point1.z, point2.x, point2.y, point2.z])
        self.last_point = np.array([point1.x, point1.y, point1.z, point2.x, point2.y, point2.z])
        self.p_best = np.array([point1.x, point1.y, point1.z, point2.x, point2.y, point2.z])
        self.last_v = np.array([random.uniform(0, 0.2), random.uniform(0, 0.2), random.uniform(0, 0.2), random.uniform(0, 0.2), random.uniform(0, 0.2), random.uniform(0, 0.2)])
        self.curr_v = self.last_v

    def calculate_v(self):
        global W, C1, C2, g_best
        self.curr_v = W * self.last_v + C1 * random.random() * (self.p_best - self.last_point) + C2 * random.random() * (g_best - self.last_point)
        for i in self.curr_v:
            if i > 0.2:
                i = 0.2

    def set_new_position(self):
        self.last_point = self.curr
        self.calculate_v()
        self.curr = self.last_point + self.curr_v

    def set_new_p_best(self, best_point):
        self.p_best = np.array([best_point[0], best_point[1], best_point[2], best_point[3], best_point[4], best_point[5]])

# calculates distance between 2 points
def calculate_distance(p1, p2):
    dst = 0
    x_dst = pow(p1.x - p2.x, 2)
    y_dst = pow(p1.y - p2.y, 2)
    z_dst = pow(p1.z - p2.z, 2)
    dst = math.sqrt(x_dst + y_dst + z_dst)
    return dst

def opt_fun(points):
    s1 = Point(points[0], points[1], points[2])
    s2 = Point(points[3], points[4], points[5])
    a_s1_distance = calculate_distance(A_POINT, s1)
    b_s1_distance = calculate_distance(B_POINT, s1)
    c_s2_distance = calculate_distance(C_POINT, s2)
    d_s2_distance = calculate_distance(D_POINT, s2)
    s1_s2_distance = calculate_distance(s1, s2)
    distance = a_s1_distance + b_s1_distance + c_s2_distance + d_s2_distance + s1_s2_distance
    return distance

def generate_initial_gen():
    g = []
    minValue = 0
    maxValue = 10
    for i in range(0, NUM_OF_AGENTS):
        x = minValue + (random.random() * (maxValue - minValue))
        y = minValue + (random.random() * (maxValue - minValue))
        z = minValue + (random.random() * (maxValue - minValue))
        xx = minValue + (random.random() * (maxValue - minValue))
        yy = minValue + (random.random() * (maxValue - minValue))
        zz = minValue + (random.random() * (maxValue - minValue))
        point1 = Point(x, y, z)
        point2 = Point(xx, yy, zz)
        agent = Agent(point1, point2)
        g.append(agent)

    return g

def pso_algorithm():
    global gen, g_best_value, g_best
    iterr = 0
    while iterr < MAX_ITER:
        iterr = iterr + 1
        for a in range(0, NUM_OF_AGENTS):
            agent = gen[a]
            cf = opt_fun(agent.curr)

            if cf < opt_fun(agent.p_best):
                agent.p_best = agent.curr
            if cf < g_best_value:
                g_best_value = cf
                g_best = agent.curr

            agent.set_new_position()


    return

def main():
    global g_best, gen, g_best_value

    startTime = time.time()

    gen = generate_initial_gen()
    pso_algorithm()



    print("Optimalne koordinate: ")
    print("S1: (", end="")
    for i in range(3):
        if i < 2:
            print(g_best[i], end=", ")
        else:
            print(g_best[i], end=")\n")

    print("S2: (", end="")
    for i in range(3, 6):
        if i < 5:
            print(g_best[i], end=", ")
        else:
            print(g_best[i], end=")\n")


    print("Duzina puta za izracunate koordinate: ", end="")
    print(g_best_value)

    endTime = time.time()
    print("\n\nVreme izvrsavanja: ", end="")
    print(endTime - startTime)



# ------------------------------
if __name__ == '__main__':
    main()