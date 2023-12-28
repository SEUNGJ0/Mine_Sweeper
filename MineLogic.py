from random import *

def generate_minesweeper_board(row, col, per):
    # 인덱스 생성 및 지뢰
    Mine_Info = {}
    t = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    Mine_count = 0
    Mine_spot = []
    for i in range(row):
        for j in range(col):
            Index = f"Index_{i}_{j}"
            Mine_Info[Index] = {'row':i,'col':j,'Mine': False,'Around_Mine_num':0,'Pct':None}
            if randint(1,10) <= per:
                Mine_Info[Index]['Mine'] = True
                Mine_spot.append([i,j]) 
                # 지뢰 개수 카운트
                Mine_count += 1
    
    for i in range(row):
        for j in range(col):
            Index = f"Index_{i}_{j}"
            A_Mine_count = 0
            if not Mine_Info[Index]['Mine'] :
                Mine_Info[Index]['Pct'] = randint(1,10)
                for v in range(8):
                    if [i+t[v][0],j+t[v][1]] in Mine_spot:
                        A_Mine_count += 1
            Mine_Info[Index]['Around_Mine_num'] = A_Mine_count

    return Mine_Info, Mine_count, t

def generate_random_indexes(row, col):
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