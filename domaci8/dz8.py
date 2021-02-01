import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time

# definisemo konstante
s = [173669, 275487, 1197613, 1549805, 502334, 217684, 1796841, 274708, 631252, 148665, 150254, 4784408, 344759, 440109,
     4198037, 329673, 28602, 144173, 1461469, 187895, 369313, 959307, 1482335, 2772513, 1313997, 254845, 486167,
     2667146, 264004, 297223, 94694, 1757457, 576203, 8577828, 498382, 8478177, 123575, 4062389, 3001419, 196884,
     617991, 421056, 3017627, 131936, 1152730, 2676649, 656678, 4519834, 201919, 56080, 2142553, 326263, 8172117,
     2304253, 4761871, 205387, 6148422, 414559, 2893305, 2158562, 465972, 304078, 1841018, 1915571]

MEM_SIZE = pow(2, 26)
D = 64
MAX_NUM_OF_ITER = 100000
MAX_NUM_OF_GEN = 50
POPULATION_SIZE = 2000
NUM_OF_REPETITIONS = 20
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.1

# promenljive
x = [] # (polazne/tekuce) tacke

gen = []#np.zeros((2000, 64)) # jedna generacija je 2000 nizova duzine 64
new_gen = []#np.zeros((POPULATION_SIZE, D))
parents_for_new_gen = [] # np.zeros((400, 64)) # 1/5 * 2000

min_per_gen = np.zeros((20, 50)) #nad ovim nizom se radi kum.min i avg.min
# [[...50...], ->prvo pokretanje, ima 50 generacija i 50 minimuma
#   [...50...]x20]  ->drugo pokretanje itd, 20 pokretanja
# x_for_min_per_gen = np.zeros((20, 50))
x_for_min_per_gen = [[0*64]*50 for i in range(20)]

cost_values_per_iter = np.zeros((20, MAX_NUM_OF_ITER))
best_c_per_iter = np.zeros((20, MAX_NUM_OF_ITER))
min_f = MEM_SIZE

best_min = MEM_SIZE #najbolje resenje od svih pokretanja
best_x = [] # x za najbolje resenje od svih pokretanja

class Jedinka:
  def __init__(self, x, costFunction):
    self.x = x
    self.costFunction = costFunction



# optimizaciona funkcija koja nam govori koliko je ostalo prostora nepopunjeno
# arg: x -> niz velicine 64 koji se sastoji od 0 i 1
def cost_function(x):
    sum = 0
    for i in range(0, 64):
        product = x[i] * s[i]
        sum += product
    result = MEM_SIZE - sum
    if (result >= 0):
        return result # u granicama memorije smo
    else:
        return MEM_SIZE # preterali smo


# generise pocetni niz x
def generate_initial_gen():
    g = []
    for i in range(0, POPULATION_SIZE):
        x = []
        for i in range(0, 64):
            x.append(random.randint(0, 1))
        c = cost_function(x)
        jed = Jedinka(x, c)
        g.append(jed)
    return g

# proces selekcije - decimacija - sortiranje jedinki po opt.fji i biranje 1/5 najboljih
def selection(g, rep, gen_num):
    global parents_for_new_gen
    global min_per_gen
    global x_for_min_per_gen
    global cost_values_per_iter
    global best_c_per_iter
    global min_f

    g_cost_fun = []

    i = 0
    for jedinka in g:
        f = jedinka.costFunction
        if(f < min_f):
            min_f = f
        best_c_per_iter[rep][gen_num*2000 + i] = min_f
        i = i + 1


    #sortiramo niz
    for i in range(2000):
        already_sorted = True
        for j in range(2000 - i - 1):
            if g[j].costFunction > g[j + 1].costFunction:
                g[j], g[j + 1] = g[j + 1], g[j]
                already_sorted = False
        if already_sorted:
            break


    min_per_gen[rep][gen_num] = g[0].costFunction
    x_for_min_per_gen[rep][gen_num] = g[0].x

    # uzimamo prvih 400
    #pg = []
    for i in range(400):
        jed = Jedinka(g[i].x, g[i].costFunction)
        parents_for_new_gen.append(jed)
    #parents_for_new_gen = pg


    return


def mutation(child):
    prob = random.random()
    if(prob < MUTATION_PROBABILITY):
        ind = random.sample(range(1, 63), 1)[0]
        if(child[ind] == 0):
            child[ind] = 1
        elif (child[ind] == 1):
            child[ind] = 0

    return child

def one_point_crossover(children_cnt):
    global parents_for_new_gen
    global new_gen

    p_indexes = random.sample(range(400), 2)
    p1_index = p_indexes[0]
    p2_index = p_indexes[1]

    p1 = parents_for_new_gen[p1_index].x
    p2 = parents_for_new_gen[p2_index].x

    # sa verovatnocom od 0.8 ovi roditelji ce se razmnoziti
    prob = random.random()
    if(prob > CROSSOVER_PROBABILITY):
        return children_cnt

    ind_for_crossover = random.sample(range(1, 63), 1)[0]
    p1_part1 = []
    p2_part1 = []
    p1_part2 = []
    p2_part2 = []
    for i in range(0, ind_for_crossover):
        p1_part1.append(p1[i])
        p2_part1.append(p2[i])
    for i in range(ind_for_crossover, 64):
        p1_part2.append(p1[i])
        p2_part2.append(p2[i])

    child1 = p1_part1 + p2_part2
    child2 = p2_part1 + p1_part2

    child1 = mutation(child1)
    child2 = mutation(child2)

    #ng = []
    #for i in range(0, children_cnt):
     #   ng.append(new_gen[i])
    new_gen.append(Jedinka(child1, cost_function(child1)))
    new_gen.append(Jedinka(child2, cost_function(child2)))
    #new_gen = ng
    children_cnt = children_cnt + 2

    return children_cnt



def genetic_algotithm(rep):
  #  print("-------REP:",end="")
   # print(rep,end="")
   # print("------------")
    global gen, new_gen, parents_for_new_gen
    global min_per_gen

    gen = generate_initial_gen() # pocetni niz

    #max pravimo 50 generacija
    for gen_num in range(0, 50):
 #       print("gen num-",end="")
 # print(gen_num, end=" ")
        # SELEKCIJA
        selection(gen, rep, gen_num)

  #      print("->min: ", end="")
  #      print(min_per_gen[rep][gen_num])

        # ako je opt fja generacije == 0 -> mozemo da zavrsimo, nema potrebe za razmnozavanjem
        if (min_per_gen[rep][gen_num] == 0):
            break;

        #  UKRSTANJE I MUTACIJA
        children_cnt = 0
        while(children_cnt < 2000):
            children_cnt = one_point_crossover(children_cnt)

        # novonastala generacija postaje tekuca
        gen = new_gen
        new_gen = []
        parents_for_new_gen = []

    return

def find_min():
    global min_per_gen
    global x_for_min_per_gen
    global best_min
    global best_x

    for rep in range(20):
        for g in range(50):
            min_temp = min_per_gen[rep][g]
            x_temp = x_for_min_per_gen[rep][g]
            if(min_temp < best_min):
                best_min = min_temp
                best_x = x_temp

def graph_for_cumulative_minimum():
    global best_c_per_iter

    x = np.arange(0, MAX_NUM_OF_ITER)

    for rep in range(0, NUM_OF_REPETITIONS):
        repNum = rep + 1
        labelName = "Run #" + str(repNum)
        plt.figure(1)
        plt.plot(x, best_c_per_iter[rep], label=labelName)

    plt.yscale("log")
    plt.xscale("log")
    # naming the x axis
    plt.xlim(1, MAX_NUM_OF_ITER)
    plt.xlabel('Broj iteracije')
    # naming the y axis
    plt.ylabel('Kumulativni minimum (optimizaciona funkcija)')

    # giving a title to my graph
    plt.title("Kumulativni minimum")

    # show grid
    plt.grid(b=True)

    # show a legend on the plot
    plt.legend()


def calculate_avg_c_per_iter():
    global best_c_per_iter
    y = [None]*MAX_NUM_OF_ITER
    for i in range(0, MAX_NUM_OF_ITER):
        sum = 0
        for j in range(0, NUM_OF_REPETITIONS):
            num = best_c_per_iter[j][i]
            sum += num
        res = sum / NUM_OF_REPETITIONS
        y[i] = res
    return y

def graph_for_avarage_cumulative_minimum():
    global avg_c_per_iter
    avg_c_per_iter = calculate_avg_c_per_iter()

    x = np.arange(0, MAX_NUM_OF_ITER)

    plt.figure(2)
    plt.plot(x, avg_c_per_iter, label="avg")

    plt.yscale("log")
    plt.xscale("log")
    # naming the x axis
    plt.xlim(1, MAX_NUM_OF_ITER)
    plt.xlabel('Broj iteracije')
    # naming the y axis
    plt.ylabel('Prosecni kumulativni minimum (optimizaciona funkcija)')

    # giving a title to my graph
    plt.title("Srednje najbolje resenje")

    # show grid
    plt.grid(b=True)

    # show a legend on the plot
    plt.legend()


def main():
    global best_x
    global best_min
    global min_f

    start = time.time()

    for rep in range(0, NUM_OF_REPETITIONS):
        min_f = MEM_SIZE
        genetic_algotithm(rep)

    graph_for_cumulative_minimum()
    graph_for_avarage_cumulative_minimum()

    find_min()
    print("Najbolje resenje:")
    print("Min cost funkcija: ", end="")
    print(best_min)
    print("Najbolje x: ", end="")
    print(best_x)

    end = time.time()
    print("Vreme izvrsavanja: ", end="")
    print(end-start)
    plt.show()

# ------------------------------
if __name__ == '__main__':
    main()