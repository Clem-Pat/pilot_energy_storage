"""PROTOCOLE :
Placer un écran à un position de référence sur une règle graduée de 50cm.
Déplacer le capteur sur cette règle graduée.
Entrer la valeur de la position du capteur puis cliquer sur entrée.
Le programme crée des listes de ces valeurs successives et plot la tension rendue par le capteur en fonction de la distance réelle.
Trouver un programme pour créer une fonction qui approche la loi du capteur.
"""

import tkinter as tk
import pyfirmata
import matplotlib.pyplot as plt
import os
path = os.path.dirname(os.path.abspath(__file__))

from Create_excel_file import create_excel as create_excel

class tkinterEntry(tk.Entry):
    """boîtes d'entrée de texte pour consigne"""

    def __init__(self):
        tk.Entry.__init__(self, app)
        self.config(width=10, font='Arial 15')
        self.bind('<Return>', self.enter)

    def enter(self,state):
        global L_reel, L_capt, board

        value = float(self.get())
        L_reel.append(value)
        self.delete(0, 20)

        capt = board.analog[0].read()
        L_capt.append(capt)
        print(f'{value} : {capt} aquis')


def stop():
    global app, L_reel, L_capt
    app.destroy()

    plt.plot(L_reel,L_capt,'g+')
    plt.show()
    create_excel(L_reel,L_capt,path)


def main():
    global L_reel, L_capt, app, board
    app = tk.Tk()

    L_reel = []
    L_capt = []

    board = pyfirmata.Arduino('COM7')
    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    board.analog[0].enable_reporting()

    entry_box = tkinterEntry()
    Button_stop = tk.Button(app, text='STOP', cursor='hand2', bg='red',font='Arial 10 bold', command=stop)
    label = tk.Label(app, cursor='hand2',font='Arial 10 bold')

    entry_box.place(x=20,y=10)
    label.place(x=20, y=40)
    Button_stop.place(x=20,y=100)

    while True:
        try:
            label.config(text=board.analog[0].read())
            app.update()
        except:
            break


if __name__=='__main__':
    main()
