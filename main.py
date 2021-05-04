import random
import statistics
import sys
import numpy as np
import time
from matplotlib import pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

def crossover(a, b, cross):
    return np.concatenate([a[:cross], b[cross:]])

hareket = [[0, 1],  # yukarı 0
           [-1, 1],  # sol üst 1
           [-1, 0],  # sol 2
           [-1, -1],  # sol alt 3
           [0, -1],  # aşağı 4
           [1, -1],  # sağ alt 5
           [1, 0],  # sağ 6
           [1, 1]]  # sağ üst 7

area_x = 9
area_y = 9
Pop = 500
drones = 4
d = 0
i = 0
j = 0
next_location = np.array([0, 0])
location = np.array([0, 0])
len = drones*20
Instances_matrix = [0]
mu = 0.01
cross = 0
Gen = 100
BK = int(Pop - Pop / 2)  # direkt aktarılacak nesil üyesi sayısı
bas_x = 0
bas_y = 0
sum = 0
baslangic = [bas_x, bas_y]
max_f1 = len-1
max_f2 = ((len - 1))*4
max_f3 = (len)*(drones)
best_instance = []
avg_instance = []
nf1 = []
nf2 = []
nf3 = []


start = time.time()#end koymayı unutma!!!!!

Instances_matrix = np.round(np.random.rand(Pop, len)*7)
Instances_matrix = Instances_matrix.astype(np.int64)
for i in range(Gen):
    f1 = np.zeros((Pop), dtype=int)
    f2 = np.zeros((Pop), dtype=int)
    f3 = np.zeros((Pop), dtype=int)
    for j in range(Pop):
        Area_matrix = np.zeros((area_x, area_y), dtype=int)
        instance = Instances_matrix[j]
        instance = np.array(instance)
        location = np.array([bas_x, bas_y])
        Area_matrix[bas_x, bas_y] = 1
        for k in range(int(len/drones)-1):
            for d in range(drones):
                next_location[0] = 0
                next_location[1] = 0
                next_location = np.add(location, hareket[instance[(int(len/drones) * d) + k]])
                if next_location[0] >= 0 and next_location[1] >= 0 and next_location[0] <= area_x - 1 and next_location[1] <= area_y - 1:
                    if Area_matrix[next_location[0], next_location[1]] != d+1 and Area_matrix[next_location[0], next_location[1]] != 0:
                        f3[j] += 1
                    location[0] = next_location[0]
                    location[1] = next_location[1]
                    Area_matrix[location[0], location[1]] = d+1
        for m in range(len - 1):
            instance_next = instance[m + 1]
            instance_curr = instance[m]
            sum = sum + (abs(4 - (abs(instance_next - instance_curr))))
        f2[j] = sum
        sum = 0
        f1[j] = np.count_nonzero(Area_matrix)
    #print(instance)
    #w = fitness
    #n_w = normalized_fitness
    #rn_w = selection
    normalized_f1 = f1 / max_f1
    nf1.append(np.mean(normalized_f1))
    #print("Norm_f1 ",i , normalized_f1)
    normalized_f2 = f2 / max_f2
    print(normalized_f2)
    nf2.append(np.mean(normalized_f2))
    #print("Norm_f2 ", i, normalized_f2)
    normalized_f3 = f3 / max_f3
    normalized_f3 = 1 - normalized_f3
    #normalized_f3 = 1 - normalized_f3
    nf3.append(np.mean(normalized_f3))
    '''plt.plot(nf1)
    plt.plot(nf2)
    plt.plot(nf3)'''
    #plt.plot(normalized_f3)
    #print("Norm_f3 ", i, normalized_f3)
    if drones != 1:
        fitness = normalized_f1+normalized_f2+normalized_f3
    else:
        fitness = normalized_f1 + normalized_f2
    normalized_fitness = fitness / np.sum(fitness)
    normalized_fitness = normalized_fitness/np.sum(normalized_fitness)
    indexes = np.argsort(normalized_fitness)
    indexes = indexes[::-1]
    selection = np.zeros(Pop, dtype = float)
    for l in range(Pop):
        selection[indexes[l]] = Pop - l
    selection = selection / np.sum(selection)
    best_index = indexes[0]
    avg_instance.append(np.mean(fitness))
    best_instance.append(fitness[best_index])
    chosen = np.random.choice(Pop, Pop, replace=True, p=selection)
    New_Instances = np.zeros((Pop, len), dtype=int)
    for n in range(int(Pop/2)-1):
        New_Instances1 = Instances_matrix[chosen[n]];
        New_Instances2 = Instances_matrix[chosen[n+int(Pop/2)]]
        cross = int(np.random.rand(1)*(len-3)+2)
        New_Instances[n] = crossover(New_Instances1, New_Instances2, cross)
        New_Instances[n+int(Pop/2)] = crossover(New_Instances2, New_Instances1, cross)
    Mutated_cells = np.random.rand(Pop, len) < mu
    for z in range(BK):
        index = indexes[z]
        New_Instances[index] = Instances_matrix[index]
    for x in range(Pop):
        for y in range(len):
            if Mutated_cells[x][y] <= mu:
                New_Instances[x][y] = np.round(np.random.rand(1, 1)*7)
    for z in range(BK):
        index = indexes[z]
        New_Instances[index] = Instances_matrix[index]
    Instances_matrix = New_Instances
    end_time = time.time()
    #print(end_time - start)
    #print(New_Instances)
    #print('********************************')
print(instance)
print(nf1)
print(nf2)
print(nf3)
#print(Instances_matrix[0])
#print(best_instance)
#print(avg_instance)
plt.plot(nf1)
plt.plot(nf2)
plt.plot(nf3)
#plt.plot(best_instance)
#plt.plot(avg_instance)
plt.show()




'''def turn_back(start, location):
    if location[0] >= start[0] and location[1] >= start[1]'''













