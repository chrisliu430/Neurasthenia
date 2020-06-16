from tkinter import *
import threading
import time
import random
import math

btn_ary = [] # Button Object Array

btn_wth = 10 # Button Width
btn_hig = 5 # Button Height 
btn_act_clr = "#AAAEEE" # Active Button Color
btn_dis_clr = "#000555" # Disable Button Color
btn_num = 16 # 按鈕總數
btn_cret_cnter = 0 # 記錄正確數對的數量
timer_cnter = 0 # 初始時間秒數

recorder = []

lock = threading.Lock()

_row = 0 # Button Row Setting
_col = 0 # Button Column Setting

random_num = [] # 紀錄每次亂數產生的數字，直到結束
click_freq = 0 # click button frequency
rcd_pos = [-1,-1] # record click button position

def game_reset():
    # 如果按鈕全部失效，可以呼叫此凾式來更新介面
    global btn_cret_cnter,timer_cnter
    timer_cnter = 0
    btn_cret_cnter = 0
    name_entry.delete(0,200)
    name_entry.config(state = "disabled")
    for i in range (len(random_num)):
        del random_num[0]
    # print(random_num)
    random_distribute_number()
    run_tiemr()
    for idx in range (btn_num):
        btn_ary[idx].config(state = "active",text = "???",width = btn_wth,height = btn_hig,highlightbackground = btn_act_clr,command = lambda pos = idx:return_position(pos))
    game_btn.config(state = "disabled")
    # record_holder()

def record_holder():
    # 查看紀錄保持者並顯示
    fi = open("neurasthenia_record.txt","r")
    for data in fi:
        recorder.append(data.strip("\n"))
    print(recorder)
    fi.close()
    recorder_show.config(text = "紀錄保持者：" + str(recorder[0]) + "   記錄秒數：" + str(recorder[1]))
    game_reset()

def refresh_recorder_key(event):
    # 更新紀錄保持者(鍵盤ENTER更新)
    if event.char == '\r':
        fo = open("neurasthenia_record.txt","w")
        recorder_name = name_entry.get()
        print(recorder_name)
        print(recorder_name,"\n",str(timer_cnter),file = fo)
        fo.close()
        del recorder[1]
        del recorder[0]
        record_holder()

def refresh_recorder_mouse(event):
    # 更新紀錄保持者(滑鼠更新)
    global btn_cret_cnter,timer_cnter
    if int(recorder[1]) > timer_cnter:
        fo = open("neurasthenia_record.txt","w")
        recorder_name = name_entry.get()
        print(recorder_name)
        print(recorder_name,"\n",str(timer_cnter),file = fo)
        fo.close()
    del recorder[1]
    del recorder[0]
    record_holder()

def run_tiemr():
    # 每秒會呼叫一次凾式
    global btn_cret_cnter,timer_cnter
    time_val.set(str(timer_cnter))
    timer_cnter += 1
    timer = threading.Timer(1,run_tiemr)
    if (btn_cret_cnter < btn_num//2):
        timer = threading.Timer(1,run_tiemr)
        timer.start()
    if (btn_cret_cnter == btn_num//2):
        timer.cancel()
        game_btn.config(state = "active")
        if int(recorder[1]) > timer_cnter:
            name_entry.config(state = "normal")
            name_entry.focus_set()
            name_entry.bind("<Key>",refresh_recorder_key)
            game_btn.bind("<Button-1>",refresh_recorder_mouse)

def check_position():
    # 確認已翻開的牌中的資料是否一致
    # 如果是，將按鈕設定成不能使用
    # 不是，則回到一開始設定
    global btn_cret_cnter
    if random_num[rcd_pos[0]] == random_num[rcd_pos[1]]:
        btn_ary[rcd_pos[0]].config(text = random_num[rcd_pos[0]],highlightbackground = btn_dis_clr,state = "disabled")
        btn_ary[rcd_pos[1]].config(text = random_num[rcd_pos[1]],highlightbackground = btn_dis_clr,state = "disabled")
        btn_cret_cnter += 1
    else:
        btn_ary[rcd_pos[0]].config(text = "???",highlightbackground = btn_act_clr,state = "active")
        btn_ary[rcd_pos[1]].config(text = "???",highlightbackground = btn_act_clr,state = "active")

def return_position(pos):
    # 紀錄已翻開的按鈕位置及判斷是否已滿足兩個資料
    # 如滿足就進入判斷是否成立資料一致性
    global click_freq
    if (click_freq == 0):
        rcd_pos[click_freq] = pos
        btn_ary[pos].config(text = random_num[pos],highlightbackground = btn_dis_clr,state = "disabled")
        click_freq += 1
    elif (click_freq == 1):
        rcd_pos[click_freq] = pos
        click_freq = 0
        btn_ary[pos].config(text = random_num[pos],highlightbackground = btn_dis_clr,state = "disabled")
        root.update()
        time.sleep(1)
        check_position()
        for idx in range (len(rcd_pos)):
            rcd_pos[idx] = -1

def random_distribute_number():
    # 分配數字給陣列位置
    counter = 0
    for idx in range (btn_num):
        random_num.append(0)
    for idx in range (1,btn_num//2+1):
        while (1):
            pos = random.randint(0,btn_num-1)
            if random_num[pos] == 0:
                random_num[pos] = idx
                counter += 1
            if counter == 2:
                counter = 0
                break

if __name__ == "__main__":
    root = Tk()
    root.title("神經衰弱")
    sqrt_num = int(math.sqrt(btn_num))
    time_val = StringVar()
    time_val.set(str(timer_cnter))
    # 計時設定
    score_show = Label(textvariable = time_val)
    score_show.grid(row = 0,column = 0,columnspan = sqrt_num)
    # 分配數字給陣列
    random_distribute_number()
    # 按鈕陣列
    for idx in range (btn_num):
        btn_ary.append(Button())
        if (idx % sqrt_num) == 0:
            _row += 1
            _col = 0
        else:
            _col += 1
        # 設定按鈕命令及外觀、位置
        btn_ary[idx].config(text = "???",width = btn_wth,height = btn_hig,highlightbackground = btn_act_clr,command = lambda pos = idx:return_position(pos))
        btn_ary[idx].grid(row = _row,column = _col)
    # 紀錄保持者顯示欄位
    recorder_show = Label()
    recorder_show.grid(row = _row+1,column = 0,columnspan = sqrt_num)
    # 新紀錄保持者姓名輸入
    name_entry = Entry(state = "disabled")
    name_entry.grid(row = _row+2,column = 0,columnspan = sqrt_num//2)
    # 重新遊戲按鈕設置
    game_btn = Button()
    game_btn.config(text = "RESET",width = 10,height = 4,state = "disabled",command = lambda:game_reset())
    game_btn.grid(row = _row+2,column = 3,columnspan = sqrt_num//2)
    # 遊戲時間凾式呼叫
    run_tiemr()
    # 讀取紀錄保持者資料
    record_holder()
    root.mainloop()
