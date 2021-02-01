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
NUM_OF_REPETITIONS = 20
INITAL_TEMP = 32*1024*1024
A_FOR_NEW_TEMP = 0.95
H_MAX = 32
H_MIN = 1

# promenljive
x = [] # (polazne/tekuce) tacke
c_per_rep = []
x_for_c_per_rep = [[]]


cost_values_per_iter =np.zeros((20, MAX_NUM_OF_ITER)) # cost_values_per_iter[0] = [vrednosti cost funkcija za 100000 iteracija prvog ponavljanja]
best_c_per_iter = np.zeros((20, MAX_NUM_OF_ITER))

avg_c_per_iter = [] # 100 000 tacaka

# generise pocetni niz x
def generate_initial_x():
    x = []
    for i in range(0, 64):
        x.append(random.randint(0, 1))
    return x

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


def hem_dist(i):
    result = ((H_MIN - H_MAX)/(MAX_NUM_OF_ITER - 1)) * (i - 1) + H_MAX
    return result

# prelazak na novu tacku
def generate_new_x(i):
    global x
    x_new = x.copy()

    h = hem_dist(i)
    indexes = random.sample(range(64), int(h))
    for j in range(0, 64):
        for index in indexes:
            if j == index:
                if(x_new[index] == 0):
                    x_new[index] = 1
                elif (x_new[index] == 1):
                    x_new[index] = 0

    return  x_new

def simulated_annealing(rep):
    global x
    global c_per_rep
    global best_c_per_iter

    # FORMIRANJE POLAZNE TACKE
    curr_temp = INITAL_TEMP
    x = generate_initial_x()

    # IZRACUNAVANJE OPT.FJE
    current_cost_function_value = cost_function(x)
    min_cost_function_value = current_cost_function_value
    x_for_min_cost_function_value = x

    cost_values_per_iter[rep][0] = current_cost_function_value

    for iter in range(1, MAX_NUM_OF_ITER):
        # ako smo dobili da je cost funkcija == 0 mozemo da stanemo
        if (min_cost_function_value == 0):
            break

        # GENERISANJE NAREDNE TACKE I RACUNANJE OPT.FJE U NJOJ
        new_x = generate_new_x(iter)
        new_cost_function_value = cost_function(new_x)
        cost_values_per_iter[rep][iter] = new_cost_function_value

        # ako imamo najbolje resenje do sada, zapamtimo ga
        if (new_cost_function_value < min_cost_function_value):
            min_cost_function_value = new_cost_function_value
            x_for_min_cost_function_value = new_x
            best_c_per_iter[rep][iter] = min_cost_function_value
        else:
            best_c_per_iter[rep][iter] = min_cost_function_value

        # DA LI PRELAZIMO NA NOVU TACKU
        if (new_cost_function_value < current_cost_function_value):
            # sigurno prelazimo
            x = new_x
            current_cost_function_value = new_cost_function_value
        else:
            # prelazimo sa verovatnocom
            exp_value = current_cost_function_value - new_cost_function_value
            exp_value /= curr_temp
            p = math.exp(exp_value) # verovatnoca, broj izmedju 0 i 1
            rand_num = random.random()
            if (rand_num < p):
                # prelazimo
                x = new_x
                current_cost_function_value = new_cost_function_value
            elif (rand_num >= p):
                # ne prelazimo
                x = x
        
        # FORMIRANJE SLEDECE TEMPERATURE
        curr_temp *= A_FOR_NEW_TEMP

    return min_cost_function_value, x_for_min_cost_function_value


def graph_for_opt_flow():
    global cost_values_per_iter

    x = np.arange(0, MAX_NUM_OF_ITER) #100000

    for rep in range(0, NUM_OF_REPETITIONS):
        repNum = rep + 1
        labelName = "Run #" + str(repNum)
        plt.figure(1)
        plt.plot(x, cost_values_per_iter[rep], label=labelName)


    plt.yscale("log")
    plt.xscale("log")
    # naming the x axis
    plt.xlim(1, MAX_NUM_OF_ITER)
    plt.xlabel('Broj iteracije')
    # naming the y axis
    plt.ylabel('Optimizaciona funkcija')

    # giving a title to my graph
    plt.title("Tok optimizacije")

    # show grid
    plt.grid(b=True)

    # show a legend on the plot
    plt.legend()

    # function to show the plot
#    plt.show()


def graph_for_cumulative_minimum():
    global best_c_per_iter

    x = np.arange(0, MAX_NUM_OF_ITER)

    for rep in range(0, NUM_OF_REPETITIONS):
        repNum = rep + 1
        labelName = "Run #" + str(repNum)
        plt.figure(2)
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

    # function to show the plot
 #   plt.show()

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

    plt.figure(3)
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

    # function to show the plot
  #  plt.show()



def main():
    global x
    global c_per_rep
    global x_for_c_per_rep

    start = time.time()

    # inicijalizacija niza
    for rep in range(0, NUM_OF_REPETITIONS):
        c_per_rep.append(0)
        x_for_c_per_rep.append([0])

    for rep in range(0, NUM_OF_REPETITIONS):
        c_per_rep[rep], x_for_c_per_rep[rep] = simulated_annealing(rep)

    graph_for_opt_flow()
    graph_for_cumulative_minimum()
    graph_for_avarage_cumulative_minimum()

    best_min_cost_function = MEM_SIZE
    for rep in range(0, NUM_OF_REPETITIONS):
        if(c_per_rep[rep] < best_min_cost_function):
            best_min_cost_function = c_per_rep[rep]
            best_x = x_for_c_per_rep[rep]
    print("Najbolje resenje:")
    print("Min cost funkcija: ", end="")
    print(best_min_cost_function)
    print("Najbolje x: ", end="")
    print(best_x)

    end = time.time()
    print("Vreme izvrsavanja: ", end="")
    print(end-start)
    plt.show()

# ------------------------------
if __name__ == '__main__':
    main()

