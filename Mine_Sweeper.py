import tkinter as tk
from tkinter import *
from random import *
from functools import partial
from MineLogic import generate_minesweeper_board, generate_random_indexes


# tkinter root instance 생성
root = tk.Tk()
root.title("Mine Sweeper")
Wid_size = [900,600]
Center_X = int(root.winfo_screenwidth()/2-Wid_size[0]/2)
Center_Y = int(root.winfo_screenheight()/2-Wid_size[1]/2)
root.geometry(f"{Wid_size[0]}x{Wid_size[1]}+{Center_X}+{Center_Y}")  # 가로 X 세로 + X좌표 + Y좌표 설정
root.resizable(False, False)  

# Frame 생성
frame1 = tk.Frame(root, relief="solid", bd=2, padx=20, pady=20)
frame1.pack(side="top", pady=30)

frame2 = tk.Frame(root, relief="solid", bd=2, padx=30, pady=30)
frame2.pack(side="bottom", pady=30)

## 기본 행 열 값 설정 ##
row, col = 5, 5
Row_Int = tk.IntVar()
Column_Int = tk.IntVar()
MSG_Txt = tk.StringVar()
MSG = tk.Message(root, textvariable=MSG_Txt, width = 500).pack()
# 최소값과 최대값 설정
MIN_ROW = 5
MAX_ROW = 10
MIN_COL = 5
MAX_COL = 19
## 행/열 설정 라벨 ## 
tk.Label(frame1,text = "Row").grid(row = 1,column = 0) 
tk.Label(frame1,text = "Column").grid(row = 2,column = 0)

## 행 개수 입력 창 ##
Ent_Row = tk.Entry(frame1, width=5, textvariable=Row_Int)
Ent_Row.delete(0,'end')
Ent_Row.insert(0,row)
Ent_Row.grid(column=1, row=1, padx=10)

## 열 개수 입력 창 ##
Ent_Col = tk.Entry(frame1, width=5, textvariable=Column_Int)
Ent_Col.delete(0,'end')
Ent_Col.insert(0,col)
Ent_Col.grid(column=1, row=2, padx=10)

## 조작 버튼 설정 ##
Button(frame1,text = "START",command= lambda : Click('Start')).grid(row = 0,column = 0)
def setbutton(row = row, col = col):
    if row > 5:
        Button(frame1,text = "▼",command= lambda : Click('row_down')).grid(row = 1,column = 3)
    elif row < 11:
        Button(frame1,text = "▲",command= lambda : Click('row_up')).grid(row = 1,column = 2)
    if col > 5:
        Button(frame1,text = "▼",command= lambda : Click('col_down')).grid(row = 2,column = 3)
    elif col < 20:
        Button(frame1,text = "▲",command= lambda : Click('col_up')).grid(row = 2,column = 2)

def Matrix(row, col):
    global frame2
    # frame2 초기화
    frame2.destroy()
    frame2 = tk.Frame(root, relief= SOLID, bd=2,padx=30, pady=30)
    frame2.pack(side = BOTTOM,pady=30)

    Mine_Info, Mine_count , t= generate_minesweeper_board(row, col, 4)
    random_list = generate_random_indexes(row, col)
    First_Click = True     # 첫 클릭인지를 확인 하는 변수
    Mistake_Count = 0   # 지뢰 클릭 횟수를 카운트하는 변수

    setbutton(row, col)
    tk.Label(frame1,text = f"지뢰 클릭 : {Mistake_Count}").grid(row=2,column=4)
    tk.Label(frame1, text = f"총 지뢰 개수 : {Mine_count}").grid(row=0,column=4)
    MSG_Txt.set("지뢰찾기를 시작합니다.")
    
    IndexButton = [[Button(frame2, relief = SOLID, borderwidth = 1, text = " ", width = 1) for j in range(col)] for i in range(row)]

    for i in range(row):
        for j in range(col):
            def L_Click_Event(i, j, self):
                ## 첫 클릭 이벤트 ##
                nonlocal First_Click , Mistake_Count # 좌클릭함수가 아닌 행렬함수의 변수를 사용
                if First_Click :
                    for v in range(len(random_list)):
                        if i+random_list[v][0] >= 0 and i+random_list[v][0] < row and j+random_list[v][1] >= 0 and j+random_list[v][1] < col :
                            if Mine_Info[f"Index_{i+random_list[v][0]}_{j+random_list[v][1]}"]['Mine'] == False:
                                IndexButton[i+random_list[v][0]][j+random_list[v][1]].config(text=Mine_Info[f"Index_{i+random_list[v][0]}_{j+random_list[v][1]}"]['Around_Mine_num'])
                            else :
                                IndexButton[i+random_list[v][0]][j+random_list[v][1]].config(text="■")
                    First_Click = False

                ## 지뢰가 아닌 것을 클릭 시 주변 지뢰 개수를 출력함 ##    
                if Mine_Info[f"Index_{i}_{j}"]['Mine'] == False:
                    
                    IndexButton[i][j].config(text=Mine_Info[f"Index_{i}_{j}"]['Around_Mine_num'])
                    MSG_Txt.set("지뢰가 아닙니다!")

                ## 지뢰를 클릭 시 지뢰 클릭 횟수가 카운트 됨 ##    
                else :
                    Mistake_Count += 1
                    tk.Label(frame1,text = f"지뢰 클릭 : {Mistake_Count}").grid(row=2,column=4)
                    MSG_Txt.set("지뢰입니다!")

            ## 우클릭시의 이벤트 설정 ##
            def R_Click_Event(i, j, self):
                if IndexButton[i][j].cget("text") == ' ':
                    IndexButton[i][j].config(text = '■')

                elif IndexButton[i][j].cget("text") == '■':
                    IndexButton[i][j].config(text = '?')

                else :
                    IndexButton[i][j].config(text = ' ')
            
            ## 미들 버튼 클릭시 이벤트 설정 ##
            def M_Click_Event(i, j, self): 
                """
                    클릭한 버튼이 지뢰가 아니고, 해당 버튼이 이미 선택된 버튼이여야하며, 난이도를 위한 확률을 설정한다.
                """
                if Mine_Info[f"Index_{i}_{j}"]['Mine'] == False and type(IndexButton[i][j].cget("text")) == int and Mine_Info[f"Index_{i}_{j}"]['Pct'] <= 2:         
                    for v in range(8):
                        if i+t[v][0] >= 0 and i+t[v][0] <= row and j+t[v][1] >= 0 and j+t[v][1] <= col :
                            if Mine_Info[f"Index_{i+random_list[v][0]}_{j+random_list[v][1]}"]['Mine'] == False:
                                IndexButton[i+random_list[v][0]][j+random_list[v][1]].config(text=Mine_Info[f"Index_{i+random_list[v][0]}_{j+random_list[v][1]}"]['Around_Mine_num'])
                            else:
                                IndexButton[i+random_list[v][0]][j+random_list[v][1]].config(text = '■')

            
            IndexButton[i][j].bind("<Button-1>",partial(L_Click_Event,i,j))
            IndexButton[i][j].bind("<Button-2>",partial(M_Click_Event,i,j))
            IndexButton[i][j].bind("<Button-3>",partial(R_Click_Event,i,j))
            IndexButton[i][j].grid(row = i, column = j)

def Click(i):
    global row, col, Row_Int, Column_Int
    if i == 'row_up' and row < MAX_ROW:
        row += 1
    elif i == 'row_down' and row > MIN_ROW:
        row -= 1
    elif i == 'col_up' and col < MAX_COL:
        col += 1
    elif i == 'col_down' and col > MIN_COL:
        col -= 1
    elif i == 'Start' and row > 0 and col > 0:
        row = Row_Int.get()
        col = Column_Int.get()

    Ent_Row.delete(0,'end')
    Ent_Row.insert(0,row)
    Ent_Col.delete(0,'end')
    Ent_Col.insert(0,col)

    return Matrix(row, col)


root.mainloop()

