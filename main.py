import numpy as np
import time

hareket = [[0, 1],  # yukarı
           [-1, 1],  # sol üst
           [-1, 0],  # sol
           [-1, -1],  # sol alt
           [0, -1],  # alt
           [1, -1],  # sağ alt
           [1, 0],  # sağ
           [1, 1]]  # sağ üst

alan_x = 9
alan_y = 9
Alan_matrix = np.zeros((alan_x, alan_y), dtype=int)
Pop = 5000
uzunluk = alan_x * alan_y - 1
mu = 0.01
Nesil = 200
cross = 1
BK = Pop - Pop / 2  # direkt aktarılacak nesil üyesi sayısı
B = np.zeros((Pop, uzunluk), dtype=int)
bas_x = 0
bas_y = 0
baslangic = [bas_x, bas_y]
max_f1 = uzunluk + 1
max_f2 = 180 * (uzunluk - 1)
best_instance = np.zeros((1, Nesil))
avg_instance = best_instance

start = time.time()#end koymayı unutma!!!!!

Instances = np.round(np.random.rand(Pop, uzunluk)*7)
print("B matrisi\n", Instances)