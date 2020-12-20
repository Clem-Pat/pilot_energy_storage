import pyfirmata
import keyboard
import time
import tkinter as tk
import numpy as np

try:
    board=pyfirmata.Arduino('COM7') #On définit la carte Arduino qui est branchée sur le port COM8
    iter8 = pyfirmata.util.Iterator(board)  #On accepte de soutirer des infos à la carte
    iter8.start()   #On démarre la lecture des données (itérative cad qu'on actualise la lecture des données)

    dt = board.get_pin('d:3:i')
    clk = board.get_pin('d:4:i')
    sw = board.get_pin('d:2:i')
except:
    board, dt, clk, sw = None, None, None, None

app = tk.Tk()
text1 = tk.Label(app, text = '0', fg='black')
text1.place(x=10, y=10)
text2 = tk.Label(app, text = '0', fg='black')
text2.place(x=10, y=50)
text_sw = tk.Label(app, text = '0', fg='blue')
text_sw.place(x=100, y=10)
text3 = tk.Label(app, text = '0', fg='red')
text3.place(x=10, y=100)

count = 0
old_clk, old_dt = 1, 1
while not keyboard.is_pressed('ctrl'):
    if board != None :
        now_dt = dt.read()
        now_clk = clk.read()

        if not now_clk and now_clk!=old_clk:
            if not now_dt : count += 1
            else: count -= 1

        now_sw = sw.read()
        if not now_sw:
            count = 0
        old_clk, old_dt = now_clk, now_dt
        try:
            text1.config(text=f'clk     : {now_clk}')
            text2.config(text=f'dt      : {now_dt}')
            text3.config(text=f'counter : {count}')
            text_sw.config(text=f'sw : {now_sw}')
            app.update()
        except:
            break
    else:
        print('no arduino')
        break
