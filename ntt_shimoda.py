import pandas as pd
from numpy.random import *
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import copy

#仮想企業データ
week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
perm = pd.DataFrame({"対応人数":[np.random.uniform(2,3) for r in range(2)], "時給":1200,"Mon":np.random.uniform(-0.3, 0.3, 2), "Tue":np.random.uniform(-0.3, 0.3, 2), "Wed":np.random.uniform(-0.3, 0.3, 2), "Thu":np.random.uniform(-0.3, 0.3, 2), "Fri":np.random.uniform(-0.3, 0.3, 2), "Sat":np.random.uniform(-0.3, 0.3, 2), "Sun":np.random.uniform(-0.3, 0.3, 2)}) #契約社員
temp = pd.DataFrame({"対応人数":[np.random.uniform(1.0,2.0) for y in range(14)], "時給":950,"Mon":np.random.uniform(1.7, 2.3, 14), "Tue":np.random.uniform(1.7, 2.3, 14), "Wed":np.random.uniform(1.7, 2.3, 14), "Thu":np.random.uniform(1.7, 2.3, 14), "Fri":np.random.uniform(1.7, 2.3, 14), "Sat":np.random.uniform(-4.7, -5.3, 14), "Sun":np.random.uniform(-4.7, -5.3, 14)}) #派遣社員
h_data = perm.append(temp, ignore_index=True).sample(frac=1).reset_index()
h_map = h_data.drop(["対応人数","時給"], axis=1)

#シフト変更関数
def v_change(v):
   v2 = copy.deepcopy(v)
   p = random.randint(0, 15)
   v2_list = list(v2.iloc[p])
   #v23 = list(v22)
   hol = random.choice([i for i, x in enumerate(v2_list) if x == 0])
   work = random.choice([i for i, x in enumerate(v2_list) if x == 1])
   v2_list[hol], v2_list[work] = v2_list[work], v2_list[hol]
   v2.iloc[p,] = v2_list
   return v2

#満足度計算関数
def satis_func(x):
  return sum((h_map*x).sum(axis=1))

##利益計算
def P_func(xx):
   PP = []
   ee = []
   for ww in week:
       cus_c = sum(h_data["対応人数"] * xx[ww])
       for b in range(0, 19):
           cus = random.randint(14, 22)
           if cus_c <= cus:
               e = cus_c * 492.8
           else:
               e = cus * 492.8
           ee.append(e)
           f = e * 0.43
           uc = e * 0.07
           PP.append(e - (f + uc))
   return sum(PP) - 455000

#正規化
def min_max_h(y):
  min = 0.00008
  max =9.408
  result = (y-min)/(max-min)
  return result

def min_max_P(z):
  min2 = 0.00000128
  max2 =34265.532
  results = (z-min2)/(max2-min2)
  return results

#初期シフト
v_perm=[1]*5 + [0]*2
v_temp = [1]*4 + [0]*3
v1 =pd.DataFrame(columns=week)
for q in range(2):
  per = pd.Series(random.sample(v_perm,7), index=v1.columns)
  v1 = v1.append(per, ignore_index=True)
for q in range(14):
  tem = pd.Series(random.sample(v_temp,7), index=v1.columns)
  v1 = v1.append(tem, ignore_index=True)

#初期計算
h1=satis_func(v1)
P1=P_func(v1)

#パラメータ設定
T=100
cool=0.9999
count = 1

ph,pP,ht,Pt = [],[],[],[]

#最適化計算
while T > 0.00001:
    v2 = v_change(v1)
    h2= satis_func(v2)

    pp = math.exp(-abs(min_max_h(h2 - h1)) / T)
    ph.append(pp)
    r1 = random.random()
    if (h2 >= h1) or ((h2 < h1) and (pp > r1)):
        P2 = P_func(v2)
        ppp = math.exp(-abs(min_max_P(P2 - P1)) / T)
        pP.append(ppp)
        r2 = random.random()

        if (P2 >= P1) or ((P2 < P1) and (ppp > r1)):
            h1 = h2
            P1 = P2
            v1 = v2

            ht.append(h1)
            Pt.append(P2)
            T = T * cool
            count = count + 1

        elif ((P2 < P1) and (ppp < r2)):
            h1 = h1
            P1 = P1
            v1 = v1

            ht.append(h1)
            Pt.append(P1)
            T = T * cool
            count = count + 1
            continue

    elif (h2 < h1 and (pp < r1)):
        h1 = h1
        P1 = P1
        v1 = v1

        ht.append(h1)
        Pt.append(P1)
        T = T * cool
        count = count + 1
        continue


plt.figure(1)
plt.plot(ht)
plt.xlabel(count)
plt.ylabel("h")

plt.figure(2)
plt.plot(Pt)
plt.xlabel(count)
plt.ylabel("P")
plt.show()
