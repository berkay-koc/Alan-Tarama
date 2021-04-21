import sys
import numpy as np
import time
np.set_printoptions(threshold=sys.maxsize)
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
Pop = 10
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
Gen = 1
cross = 1
BK = Pop - Pop / 2  # direkt aktarılacak nesil üyesi sayısı
B = np.zeros((Pop, len), dtype=int)
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
            for a in range(len-1):
                instance_next = instance[a+1]
                instance_curr = instance[a]
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
    normalized_fitness = np.sort(normalized_fitness)
    normalized_fitness = normalized_fitness[::-1]
    indexes = indexes[::-1]
    selection[]
    print(normalized_fitness)
    print(indexes)
    for i in range(Pop):
        selection[indexes[i]] = 10-i
    print(selection)
    best_index = indexes[0]
    avg_instance[i] = np.mean(fitness)
    best_instance[i] = fitness[best_index]















