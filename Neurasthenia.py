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
btn_num = 16 # Total Button Number
btn_cret_cnter = 0 # record correct number
timer_cnter = 0 # timer second

recorder = []

lock = threading.Lock()

_row = 0 # Button Row Setting
_col = 0 # Button Column Setting

random_num = [] # record number in button array
click_freq = 0 # click button frequency
rcd_pos = [-1,-1] # record click button position

def game_reset():
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
    fi = open("neurasthenia_record.txt","r")
    for data in fi:
        recorder.append(data.strip("\n"))
    print(recorder)
    fi.close()
    recorder_show.config(text = "紀錄保持者：" + str(recorder[0]) + "   記錄秒數：" + str(recorder[1]))
    # print(recorder)
    game_reset()

def refresh_recorder_key(event):
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


def check_position(): # check data is correct in button array
    global btn_cret_cnter
    if random_num[rcd_pos[0]] == random_num[rcd_pos[1]]:
        btn_ary[rcd_pos[0]].config(text = random_num[rcd_pos[0]],highlightbackground = btn_dis_clr,state = "disabled")
        btn_ary[rcd_pos[1]].config(text = random_num[rcd_pos[1]],highlightbackground = btn_dis_clr,state = "disabled")
        btn_cret_cnter += 1
    else:
        btn_ary[rcd_pos[0]].config(text = "???",highlightbackground = btn_act_clr,state = "active")
        btn_ary[rcd_pos[1]].config(text = "???",highlightbackground = btn_act_clr,state = "active")

def return_position(pos): # record twice click position on button
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
    score_show = Label(textvariable = time_val)
    score_show.grid(row = 0,column = 0,columnspan = sqrt_num)
    random_distribute_number()
    for idx in range (btn_num):
        btn_ary.append(Button())
        if (idx % sqrt_num) == 0:
            _row += 1
            _col = 0
        else:
            _col += 1
        btn_ary[idx].config(text = "???",width = btn_wth,height = btn_hig,highlightbackground = btn_act_clr,command = lambda pos = idx:return_position(pos))
        btn_ary[idx].grid(row = _row,column = _col)
    recorder_show = Label()
    recorder_show.grid(row = _row+1,column = 0,columnspan = sqrt_num)
    name_entry = Entry(state = "disabled")
    name_entry.grid(row = _row+2,column = 0,columnspan = sqrt_num//2)
    game_btn = Button()
    game_btn.config(text = "RESET",width = 10,height = 4,state = "disabled",command = lambda:game_reset())
    game_btn.grid(row = _row+2,column = 3,columnspan = sqrt_num//2)
    run_tiemr()
    # get_k = Button(state = "active",width = 10,height = 5,command = lambda:get_data())
    # get_k.grid(row = _row+3,column = 2)
    record_holder()
    root.mainloop()
