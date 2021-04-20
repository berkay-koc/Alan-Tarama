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
drones = 4
i = 0
j = 0
next_location = np.array([0, 0])
location = np.array([0, 0])
len = drones*(area_x * area_y - 1)
Instances_matrix = [0]
mu = 0.01
Gen = 1
cross = 1
BK = Pop - Pop / 2  # direkt aktarılacak nesil üyesi sayısı
B = np.zeros((Pop, len), dtype=int)
bas_x = 0
bas_y = 0
baslangic = [bas_x, bas_y]
max_f1 = len + 1
max_f2 = 180 * (len - 1)
best_instance = np.zeros((1, Gen))
avg_instance = best_instance

start = time.time()#end koymayı unutma!!!!!

Instances_matrix = np.round(np.random.rand(Pop, len)*7)
Instances_matrix = Instances_matrix.astype(np.int64)
for i in range(Gen):
    f1 = np.zeros((1, Pop), dtype=int)
    f2 = np.zeros((1, Pop), dtype=int)
    for j in range(Pop):
        Area_matrix = np.zeros((area_x, area_y), dtype=int)
        instance = Instances_matrix[j]
        instance = np.array(instance)
        location = np.array([bas_x, bas_y]);
        Area_matrix[bas_x, bas_y] = 1
        for k in range(len):
            next_location = np.add(location,hareket[instance[k]])
            if next_location[0] >= 0 and next_location[1] >= 0 and next_location[0] <= area_x-1 and next_location[1] <= area_y-1:
                location = next_location
            Area_matrix[location[0], location[1]] = k+1
print(Area_matrix)