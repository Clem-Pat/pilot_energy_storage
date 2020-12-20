"""PROTOCOLE :
Placer un écran à un position de référence sur une règle graduée de 50cm.
Déplacer le capteur sur cette règle graduée.
Entrer la valeur de la position du capteur puis cliquer sur entrée.
Le programme crée des listes de ces valeurs successives et plot la tension rendue par le capteur en fonction de la distance réelle.
Il crée également un fichier excel pour stocker les valeurs de façon lisibile et interprétable. NE PAS UTILISER LA CROIX ROUGE POUR FERMER mais le boutton stop !!!
Trouver un programme pour créer une fonction qui approche la loi du capteur.
"""
import tkinter as tk
import pyfirmata
import matplotlib.pyplot as plt
import os
from Create_excel_file import create_excel as create_excel

"""sensor pin A0"""

class tkinterApp():
    def __init__(self, board):
        self.board = board
        self.fen = tk.Tk()
        self.button = tkinterButton(self)
        self.entry = tkinterEntry(self)
        self.label = tkinterLabel(self)
        self.place_all_objects()

        self.L_reel = []
        self.L_capt = []
        self.path = os.path.dirname(os.path.abspath(__file__))

        self.fen.bind('<Control_L>z', self.back)

    def place_all_objects(self):
        self.button.place(x=20,y=100)
        self.entry.place(x=20,y=10)
        self.label.place(x=20, y=40)

    def back(*args):
        self = args[0]
        if self.L_reel != [] and self.L_capt != []:
            print('###')
            print(str(self.L_reel[-1]) + " : " + str(self.L_capt[-1]) + ' destroyed')
            print('###')
            self.L_reel.pop(-1)
            self.L_capt.pop(-1)
        else:
            print('les listes sont vides')

    def create_excel_file(self):
        create_excel(self.L_reel,self.L_capt,self.path)


class tkinterButton(tk.Button):
    def __init__(self, app):
        tk.Button.__init__(self, app.fen)
        self.app = app
        self.config(text='STOP', cursor='hand2', bg='red',font='Arial 10 bold', command=self.stop)

    def stop(self):
        self.app.fen.destroy()

        if self.app.board.arduinoboard != None:
            plt.plot(self.app.L_reel, self.app.L_capt,'g+')
            plt.show()

            self.app.create_excel_file()


class tkinterEntry(tk.Entry):
    """boîtes d'entrée de texte pour consigne"""

    def __init__(self, app):
        tk.Entry.__init__(self, app.fen)
        self.app = app
        self.config(width=10, font='Arial 15')
        self.bind('<Return>', self.enter)

    def enter(self,state):
        if self.app.board.arduinoboard != None:
            value = float(self.get())
            self.app.L_reel.append(value)
            self.delete(0, 20)

            capt = self.app.board.arduinoboard.analog[0].read()
            self.app.L_capt.append(capt)
            print(f'{value} : {capt} aquis')

        else:
            self.delete(0, 20)
            print('Pas de carte Arduino branchée !!')


class tkinterLabel(tk.Label):
    def __init__(self, app):
        tk.Label.__init__(self, app.fen)
        self.app = app
        self.config(text='None', font='Arial 10 bold')


class Board():
    def __init__(self, port):
        try :
            self.arduinoboard = pyfirmata.Arduino(port)
            iter8 = pyfirmata.util.Iterator(self.arduinoboard)
            iter8.start()
            self.arduinoboard.analog[0].enable_reporting()
        except:
            self.arduinoboard = None
            print('Pas de carte Arduino branchée !!')


def main():
    board = Board('COM7')
    app = tkinterApp(board)

    while True:
        try:
            if board.arduinoboard != None:
                app.label.config(text=board.arduinoboard.analog[0].read())
            app.fen.update()
        except:
            break


if __name__=='__main__':
    main()
