from random import *

def MainLogic(row, col, per):
    # 인덱스 생성 및 지뢰
    Mine_Info = {}
    t = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    Mine_count = 0
    Mine_spot = []
    for i in range(row):
        for j in range(col):
            Mine_Info[f"Index_{i}_{j}"] = {'row':i,'col':j,'Mine': False,'Around_Mine_num':0,'Pct':None}
            if randint(1,10) <= per:
                Mine_Info[f"Index_{i}_{j}"].update(Mine = True) 
                Mine_spot.append([i,j]) 
                # 지뢰 개수 카운트
                Mine_count += 1
    
    for i in range(row):
        for j in range(col):
            A_Mine_count = 0
            if Mine_Info[f"Index_{i}_{j}"]['Mine'] == False:
                Mine_Info[f"Index_{i}_{j}"].update({'Pct':randint(1,10)})
                for v in range(8):
                    if [i+t[v][0],j+t[v][1]] in Mine_spot:
                        A_Mine_count += 1
            Mine_Info[f"Index_{i}_{j}"].update({'Around_Mine_num' : A_Mine_count}) 
    return Mine_Info, Mine_count, t

def randindex(row, col):
    random_list = []
    for x in range(randint(2,round(row/3))):
        for y in range(randint(2,round(col/3))):
            random_list.append([x,y])
        for y in range(randint(2,round(col/3))):
            random_list.append([x,-y])
    for x in range(1,randint(2,round(row/3))):
        for y in range(randint(2,round(col/3))):
            random_list.append([-x,y])
        for y in range(randint(2,round(col/3))):
            random_list.append([-x,-y])
    return random_list