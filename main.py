import sys

import matplotlib
import numpy as np
import time
from matplotlib import pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

def crossover(a, b, cross):
    return np.concatenate([a[:cross], b[cross:]])

def maximum(a, b):

    if a >= b:
        return a
    else:
        return b

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
Pop = 1000
drones = 4
d = 0
i = 0
j = 0
k = 1

next_location = np.array([0, 0])
location = np.array([0, 0])

len = drones*80
Instances_matrix = [0]
mu = 0.01
Gen = 200
ctr = 0
BI = int(Pop / 4)  # direkt aktarılacak nesil üyesi sayısı
bas_x = 0
bas_y = 0
sum = 0
baslangic = [bas_x, bas_y]
max_f1 = (area_x*area_y)-1
max_f2 = ((len - 1))*180
max_f3 = len - 1
best_instance = []
avg_instance = []
nf1 = []
nf2 = []
nf3 = []
location_matrix = np.zeros((drones, int(len/drones)), dtype=int)

start = time.time()#sayaç başlangıcı

Instances_matrix = np.round(np.random.rand(Pop, len)*7)#random sayılardan oluşan Pop kadar bireye sahip ilk jenerasyonun matrisi
Instances_matrix = Instances_matrix.astype(np.int64)
for f in range(drones):#tüm dronelarımız için başlangıcı ayarlayan kısım
    location_matrix[f,0] = bas_x*10+bas_y

for i in range(Gen):
    f1 = np.zeros((Pop), dtype=int) #taranan alan miktarını bulan fitness fonksiyonu
    f2 = np.zeros((Pop), dtype=int) #açıları iyileştirmemiz ve dönüş miktarını azaltmak için kullandığımız fitness fonksiyonu
    f3 = np.zeros((Pop), dtype=int) #droneların oldukça farklı yerlere gitmelerini sağlayan fitness fonksiyonu
    for j in range(Pop):
        Area_matrix = np.zeros((area_x, area_y), dtype=int)
        instance = Instances_matrix[j]#işlem yapmak için ilk bireyi instance dizisinde tutuyoruz
        instance = np.array(instance)
        Area_matrix[bas_x, bas_y] = 1#başlangıç noktasını işaretledik
        for k in range(int(len/drones)-1):#droneların sırayla hareket etmelerini sağlayacak for döngüleri
            for d in range(drones):
                next_location[0] = 0#hareket edilecek yönün x indisi
                next_location[1] = 0#hareket edilecek yönün y indisi
                location[0] = int(location_matrix[d,k] / 10)#bir önceki lokasyonun x indisine dönüştürülmesi
                location[1] = location_matrix[d,k] - location[0]*10#bir önceki lokasyonun y indisine dönüştürülmesi
                next_location = np.add(location, hareket[instance[(int(len/drones) * d) + k]])#yeni lokasyonun hesaplanması
                if next_location[0] >= 0 and next_location[1] >= 0 and next_location[0] <= area_x - 1 and next_location[1] <= area_y - 1:#yeni lokasyonun matrisin içinde kalıp kalmadığını kontrol etme
                    if Area_matrix[next_location[0], next_location[1]] != d+1 and Area_matrix[next_location[0], next_location[1]] != 0:#eğer gidilecek lokasyon daha önce başka bir drone tarafından gezildiyse fitness3 fonksiyonunun arttırılması
                        f3[j] += 1
                    location_matrix[d,k+1] = next_location[0]*10+next_location[1]#yeni lokasyonun lokasyon matrisine eklenmesi
                    Area_matrix[next_location[0], next_location[1]] = d + 1#gezilen yerin drone numarası ile işaretlenmesi
                else:
                    location_matrix[d,k+1] = location_matrix[d,k]#eğer drone dışarı çıkıyorsa matrisin
        for m in range(len - 1):#fitness2 fonksiyonunu hesaplamamız için her iki ardışık hareket arasındaki açı farkını buluyoruz.
            instance_next = instance[m + 1]
            instance_curr = instance[m]
            sum = sum + (abs(4 - (abs(instance_next - instance_curr))))*45#iki yön arasındaki açıyı bulup tüm instance dizisi için bunu kümülatif şekilde yapıyoruz
        f2[j] = sum
        sum = 0
        f1[j] = np.count_nonzero(Area_matrix)#matrisimizde taranan hücre sayısını buluyoruz

    normalized_f1 = f1 / max_f1#fitness fonksiyonlarımızı normalize ediyoruz.
    normalized_f2 = f2 / max_f2
    normalized_f3 = f3 / max_f3
    normalized_f3 = 1 - normalized_f3#f3 istemediğimiz halde olduğu için tam tersini bulup onunla işlem yapmak için 1'den çıkartıyoruz.
    if drones != 1:  #eğer drone sayımız 1 ise f3 fonksiyonumuzu hesaba katmamalıyız! üçünü de hesaba katan fitness fonksiyonumuzu buluyoruz
        fitness = normalized_f1+normalized_f2+normalized_f3
    else:
        fitness = normalized_f1 + normalized_f2
    normalized_fitness = fitness / np.sum(fitness)  # fitness fonksiyonumuzu normalize ediyoruz
    normalized_fitness = normalized_fitness/np.sum(normalized_fitness)  # ??????
    indexes = np.argsort(normalized_fitness)  #normalize fitness dizimizdeki bireylerin ideal olanlarını kullanmak için indexlerini sıralıyoruz
    indexes = indexes[::-1]  #büyükten küçüğe sıralı olması için diziyi tersine çeviriyoruz
    selection = np.zeros(Pop, dtype = int)  #bireylerin iyiliklerine göre ağırlıklarını içinde tutacak olan selection fonksiyonu

    for l in range(Pop):
        selection[indexes[l]] = Pop - l#büyükten küçüğe sıralı index değerlerini en büyükten başlayacak şekilde selectionun içerisine yerleştiriyoruz
    selection = selection / np.sum(selection)#selectionları choice fonksiyonuna hazır etmek için normalize ediyoruz. böylece ağırlıklarına göre seçim yapabileceğiz
    best_index = indexes[0]  # en iyi bireyi alıyoruz
    avg_instance.append(np.mean(fitness))  # bireylerin ortalamasını alıyoruz
    best_instance.append(fitness[best_index])  # her jenerasyonun en iyi bireyini bir diziye atıyoruz
    chosen = np.random.choice(Pop, Pop, replace=True, p=selection)  # choice fonksiyonundan yararlanarak rulet tekeri yöntemiyle seçim yapıyoruz
    New_Instances = np.zeros((Pop, len), dtype=int) #  Yeni bireylerin yer alacağı matrisi oluşturuyoruz

    for n in range(int(Pop/2)-1):  #  tek noktadan crossover yapacağımız for döngüsü
        New_Instances1 = Instances_matrix[chosen[n]];  #ilk bireyi alıyoruz
        New_Instances2 = Instances_matrix[chosen[n+int(Pop/2)]]  #ortadan ilk bireyi alıyoruz
        cross = int(np.random.rand(1)*(len-3)+2)  #crossover yapılacak noktayı random olarak seçiyoruz
        New_Instances[n] = crossover(New_Instances1, New_Instances2, cross)  #tek noktadan crossover, en başta tanımlanan crossover fonksiyonunu çağırır
        New_Instances[n+int(Pop/2)] = crossover(New_Instances2, New_Instances1, cross)  #2. tek noktadan crossover
    Mutated_cells = np.random.rand(Pop, len) < mu  #mutasyona uğrayacak bireylerin hangi elemanlarının değişeceğini belirliyoruz

    for x in range(Pop):
        for y in range(len):
            if Mutated_cells[x][y] <= mu:
                New_Instances[x][y] = np.round(np.random.rand(1, 1)*7)  #mutasyona uğrayacak hücreleri random şekilde değiştiriyoruz

    for z in range(BI):
        index = indexes[z]  # en iyi bireylerin yarısını yeni bireylerimizin yarısına transfer ediyoruz
        New_Instances[BI] = Instances_matrix[index]  # yeni bireyler matrisine belirlenen bireyler atılıyor
        BI += 1

    BI = int(Pop / 2)
    Instances_matrix = New_Instances #yeni bireylerimizi kullandığımız matrise aktarıyoruz
    end_time = time.time()
    print(ctr, end_time - start)
    ctr += 1
Area_matrix = np.zeros((area_x, area_y), dtype=int) #matrisi çizdirmek için alan matrisimizi 0'lıyoruz

for b in range(drones): # alan matrisini her drone için çizdirmeye yarayan iç içe 2 for döngüsü
    for z in range(int(len/drones)):
        location[0] = int(location_matrix[b, z] / 10)
        location[1] = location_matrix[b, z] - location[0] * 10
        Area_matrix[location[0], location[1]] = 1
        plt.clf()
        cmap = matplotlib.colors.ListedColormap(np.random.rand(256, 3))
        plt.imshow(Area_matrix, cmap= cmap)
    Area_matrix = np.zeros((area_x, area_y), dtype=int)
    plt.pause(10)
    plt.clf()
plt.show()













