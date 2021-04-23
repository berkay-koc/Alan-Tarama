import random
import sys
import numpy as np
import time
np.set_printoptions(threshold=sys.maxsize)

def crossover(a, b, cross):
    return np.concatenate([a[:cross], b[cross:]])

hareket = [[0, 1],  # yukarı
           [-1, 1],  # sol üst
           [-1, 0],  # sol
           [-1, -1],  # sol alt
           [0, -1],  # alt
           [1, -1],  # sağ alt
           [1, 0],  # sağ
           [1, 1]]  # sağ üst

area_x = 9
area_y = 9
Pop = 50
drones = 2
d = 0
i = 0
j = 0
next_location = np.array([0, 0])
location = np.array([0, 0])
len = 0
len = drones*(area_x * area_y - 1)
Instances_matrix = [0]
mu = 0.01
cross = 0
Gen = 20
BK = int(Pop - Pop / 2)  # direkt aktarılacak nesil üyesi sayısı
bas_x = 4
bas_y = 4
sum = 0
baslangic = [bas_x, bas_y]
max_f1 = len + 1
max_f2 = 180 * (len - 1)
max_f3 = (area_y*area_x) - 1
best_instance = np.zeros((1, Gen))
avg_instance = np.zeros((1, Gen))

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
        location = np.array([bas_x, bas_y]);
        Area_matrix[bas_x, bas_y] = 1
        for d in range(drones):
            for k in range((area_x*area_y)-1):
                next_location = np.add(location,hareket[instance[(((area_x*area_y)-1)*d) + k]])
                if next_location[0] >= 0 and next_location[1] >= 0 and next_location[0] <= area_x-1 and next_location[1] <= area_y-1:
                    if Area_matrix[next_location[0], next_location[1]] != 0 and Area_matrix[next_location[0], next_location[1]] != d+1:
                        f3[j] += 1
                    location = next_location
                Area_matrix[location[0], location[1]] = d+1

            f1[j] = np.count_nonzero(Area_matrix)
            for m in range(len-1):
                instance_next = instance[m+1]
                instance_curr = instance[m]
                sum = sum + (180-(abs(instance_next-instance_curr)*45))
            f2[j] = sum
            sum = 0
    #w = fitness
    #n_w = normalized_fitness
    #rn_w = selection
    normalized_f1 = f1 / max_f1
    normalized_f2 = f2 / max_f2
    normalized_f3 = f3 / max_f3
    normalized_f3 = 1 - normalized_f3
    fitness = normalized_f2+normalized_f1+normalized_f3

    normalized_fitness = fitness / np.sum(fitness)
    indexes = np.argsort(normalized_fitness)
    indexes = indexes[::-1]
    selection = np.zeros(Pop, dtype = float)
    i = 0
    for l in range(Pop):
        selection[indexes[l]] = Pop - l
    selection = selection / np.sum(selection)
    best_index = indexes[0]
    '''avg_instance[i] = np.mean(fitness)'''
    best_instance = fitness[best_index]
    chosen = np.random.choice(Pop, Pop, replace=True, p=selection)
    New_Instances = np.zeros((Pop, len), dtype=int)
    for n in range(int(Pop/2)-1):
        New_Instances1 = Instances_matrix[chosen[n]];
        New_Instances2 = Instances_matrix[chosen[n+int(Pop/2)]]
        cross = int(np.random.rand(1)*(len-3)+2)
        New_Instances[n] = crossover(New_Instances1, New_Instances2, cross)
        New_Instances[n+int(Pop/2)] = crossover(New_Instances2, New_Instances1, cross)
    Mutated_cells = np.random.rand(Pop, len)<mu
    for x in range(Pop):
        for y in range(len):
            if Mutated_cells[x][y] <= mu:
                New_Instances[x][y] = np.round(np.random.rand(1, 1)*7)
    New_Instances[indexes[:BK]] = Instances_matrix[indexes[:BK]]
    Instances_matrix = New_Instances
    print(best_instance)



'''def turn_back(start, location):
    if location[0] >= start[0] and location[1] >= start[1]'''













