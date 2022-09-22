import tkinter as tk
from random import *
from tkinter import *
from functools import partial
from MineLogic import MineLogic as Logic

root = Tk()
root.title("Mine Dectector")                   # 타이틀 제목 설정

## 창 크기 설정 ##
Wid_size = [900,600]
Center_X = int(root.winfo_screenwidth())/2-Wid_size[0]/2
Center_Y = int(root.winfo_screenheight())/2-Wid_size[1]/2
root.geometry("%dx%d+%d+%d"%(Wid_size[0],Wid_size[1],Center_X, Center_Y))  # 가로 X 세로 + X좌표 + Y좌표 설정
root.resizable(False, False)  

frame1=tk.Frame(root, relief= SOLID, bd=2,padx=20, pady=20)
frame1.pack(side = TOP,pady=30)

frame2=tk.Frame(root, relief= SOLID, bd=2,padx=30, pady=30)
frame2.pack(side = BOTTOM,pady=30)

## 기본 행 열 값 설정 ##
row, col = 5, 5
r_num, c_num = 5, 5
Row_Int = tk.IntVar()
Column_Int = tk.IntVar()
MSG_Txt = tk.StringVar()
    
def Click(i):
    global row, col, r_num, c_num, Row_Int, Column_Int
    if i == 'row_up':
        row += 1
        r_num += 1
    elif i == 'row_down': 
        row -= 1
        r_num -= 1
    elif i == 'col_up':
        col += 1
        c_num += 1
    elif i == 'col_down': 
        col -= 1
        c_num -= 1
    elif i == 'Start':
        Matrix(Row_Int.get(),Column_Int.get())
        return
    Matrix(row, col)
    Ent_Col.delete(0,'end')
    Ent_Row.delete(0,'end')
    Ent_Col.insert(0,c_num)
    Ent_Row.insert(0,r_num)
    

MSG = tk.Message(root, textvariable=MSG_Txt, width = 500).pack()
## 조작 버튼 설정 ##
Button(frame1,text = "START",command= lambda:Click('Start')).grid(row = 0,column = 0)
Button(frame1,text = "▲",command= lambda:Click('row_up')).grid(row = 1,column = 2)
Button(frame1,text = "▼",command= lambda:Click('row_down')).grid(row = 1,column = 3)
Button(frame1,text = "▲",command= lambda:Click('col_up')).grid(row = 2,column = 2)
Button(frame1,text = "▼",command= lambda:Click('col_down')).grid(row = 2,column = 3)

## 행/열 설정 라벨 ## 
tk.Label(frame1,text = "Row").grid(row = 1,column = 0) 
tk.Label(frame1,text = "Column").grid(row = 2,column = 0)

## 행 개수 입력 창 ##
Ent_Row = tk.Entry(frame1, width=5, textvariable=Row_Int)
Ent_Row.delete(0,'end')
Ent_Row.insert(0,r_num)
Ent_Row.grid(column=1, row=1, padx=10)

## 열 개수 입력 창 ##
Ent_Col = tk.Entry(frame1, width=5, textvariable=Column_Int)
Ent_Col.delete(0,'end')
Ent_Col.insert(0,c_num)
Ent_Col.grid(column=1, row=2, padx=10)

def randindex(row, col):
    global list
    list = []
    for x in range(randint(2,round(row/3))):
        for y in range(randint(2,round(col/3))):
            list.append([x,y])
        for y in range(randint(2,round(col/3))):
            list.append([x,-y])
    for x in range(1,randint(2,round(row/3))):
        for y in range(randint(2,round(col/3))):
            list.append([-x,y])
        for y in range(randint(2,round(col/3))):
            list.append([-x,-y])

def Matrix(row, col):
    Mine_Info, Mine_count = Logic(row, col, 4)
    randindex(row, col)
    #global First_Click ,Mistake_Count
    First_Click = 0     # 첫 클릭인지를 확인 하는 변수
    Mistake_Count = 0   # 지뢰 클릭 횟수를 카운트하는 변수
    tk.Label(frame1, text=f"총 지뢰 개수 : {Mine_count}").grid(row=0,column=4)
    MSG_Txt.set("지뢰찾기를 시작합니다.")

    for i in range(row):
        for j in range(col):

            def R_Click_Event(i,j,non):
                nonlocal First_Click ,Mistake_Count # 우클릭함수가 아닌 행렬함수의 변수를 사용
                ## 첫 클릭시 더 보여줌 ##
                if First_Click == 0 :
                    for v in range(len(list)):
                        if i+list[v][0] >= 0 and i+list[v][0] < row and j+list[v][1] >= 0 and j+list[v][1] < col :
                            if Mine_Info[f"Index_{i+list[v][0]}_{j+list[v][1]}"]['Mine'] == 0:
                                eval(f'B_{i+list[v][0]}_{j+list[v][1]}').config(text=Mine_Info[f"Index_{i+list[v][0]}_{j+list[v][1]}"]['Around_Mine_num'])
                            else :
                                eval(f'B_{i+list[v][0]}_{j+list[v][1]}').config(text="■")
                        First_Click += 1 

                ## 지뢰가 아닌 것을 클릭 시 주변 지뢰 개수를 출력함 ##    
                if Mine_Info[f"Index_{i}_{j}"]['Mine'] == 0:
                    eval(f'B_{i}_{j}').config(text=Mine_Info[f"Index_{i}_{j}"]['Around_Mine_num'])
                    MSG_Txt.set("지뢰가 아닙니다!")

                ## 지뢰를 클릭 시 지뢰 클릭 횟수가 카운트 됨 ##    
                else :
                    Mistake_Count += 1
                    tk.Label(frame1,text = f"지뢰 클릭 : {Mistake_Count}").grid(row=2,column=4)
                    MSG_Txt.set("지뢰입니다!")

            def L_Click_Event(i,j,a):
                ## 좌클릭시의 이벤트 설정 ##
                if eval(f'B_{i}_{j}').cget("text") == ' ':
                    eval(f'B_{i}_{j}').config(text = '■')

                elif eval(f'B_{i}_{j}').cget("text") == '■':
                    eval(f'B_{i}_{j}').config(text = '?')

                else :
                    eval(f'B_{i}_{j}').config(text = ' ')
            
            def M_Click_Event(i,j,a): 
                ## 미들 버튼 클릭시 이벤트 설정 ##
                """
                    클릭한 버튼이 지뢰가 아니고, 해당 버튼이 이미 선택된 버튼이여야하며, 난이도를 위한 확률을 설정한다.
                """
                if Mine_Info[f"Index_{i}_{j}"]['Mine'] == 0 and type(eval(f'B_{i}_{j}').cget("text")) == int and Mine_Info[f"Index_{i}_{j}"]['Pct'] <= 2:         
                    for v in range(8):
                        if i+t[v][0] >= 0 and i+t[v][0] <= row and j+t[v][1] >= 0 and j+t[v][1] <= col :
                            if Mine_Info[f"Index_{i+list[v][0]}_{j+list[v][1]}"]['Mine'] == 0:
                                eval(f'B_{i+list[v][0]}_{j+list[v][1]}').config(text=Mine_Info[f"Index_{i+list[v][0]}_{j+list[v][1]}"]['Around_Mine_num'])
                            else:
                                eval(f'B_{i+list[v][0]}_{j+list[v][1]}').config(text = '■')

            
            globals()[f'B_{i}_{j}'] = Button(frame2,relief = SOLID, borderwidth = 1, text = " ", width = 2 )  
            eval(f'B_{i}_{j}').bind("<Button-1>",partial(R_Click_Event,i,j))
            eval(f'B_{i}_{j}').bind("<Button-2>",partial(M_Click_Event,i,j))
            eval(f'B_{i}_{j}').bind("<Button-3>",partial(L_Click_Event,i,j))
            eval(f'B_{i}_{j}').grid(row = i,column=j) 

root.mainloop()

