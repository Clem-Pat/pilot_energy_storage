import tkinter as tk  #module d'interface graphique
from pynput.mouse import Button, Controller
import time

from tkinter_objects import tkinterButton, tkinterLabel, tkinterScale, tkinterCanvas, tkinterEntry
import main
import arduino_objects

class tkinterWindow():

    def __init__(self, name_of_application, board, init_pot_app=None, parent_app=None):

        self.fen = tk.Tk()
        self.name = name_of_application
        self.board = board
        self.init_pot_app = init_pot_app
        self.parent_app = parent_app
        self.pilot_mode = "manual"

        if self.name == 'main':
            self.center_position = (860, 260)
            self.x, self.y = 450, 0
            self.longueur, self.hauteur = 800, 800
            self.fen.title("Interface de pilotage du système de stockage d'énergie")
            self.fen.configure(bg="light blue")
            self.buttons = [tkinterButton(self, i) for i in range(4)]
            self.labels = [tkinterLabel(self, i) for i in range(2)]
            self.scales = [tkinterScale(self, i) for i in range(1)]
            self.canvas = [tkinterCanvas(self, i) for i in range(2)]
            self.entrys = [tkinterEntry(self, i) for i in range(1)]
            self.objects = [self.buttons, self.labels, self.scales, self.canvas, self.entrys]

            self.board.app = self
            self.board.reload()

        elif self.name == "init_pot":
            self.center_position = (325, 270)
            self.x, self.y = 10, 50  # positions de la fenetre
            self.longueur, self.hauteur = 650, 500
            self.fen.title("Initialisation potentiomètres")
            self.fen.configure(bg="grey70")
            self.buttons = [tkinterButton(self, i) for i in range(2)]
            self.labels = [tkinterLabel(self, i) for i in range(1)]
            self.objects = [self.buttons, self.labels]

        self.fen.geometry("{}x{}+{}+{}".format(str(self.longueur),
                                               str(self.hauteur), str(self.x), str(self.y)))
        self.fen.resizable(width=False, height=False)
        self.fen.bind('<Escape>', self.destroy)
        self.fen.bind('<Control_L>p', self.get_mouse_position)
        self.fen.bind('<Control_L><Return>', self.mouse_click)
        self.fen.bind('<Control_L>r', self.reload)

        self.update()
        self.mouse_click('event', position = self.center_position)


    def reload(self, event):
        self.destroy('event')
        main.main()

    def destroy(self, event):
        if self.init_pot_app != None:
            self.init_pot_app.fen.destroy()
            self.init_pot_app = None
        if self.parent_app != None:
            self.parent_app.init_pot_app = None
        self.fen.destroy()

    def get_mouse_position(self, event):
        mouse = Controller()
        position = (mouse.position[0] - self.x - 10, mouse.position[1] - self.y - 30)
        print('Position : {}'.format(position))

    def mouse_click(self, event, mouse = Controller(), position = Controller().position):
        mouse.position = position
        mouse.press(Button.left)
        mouse.release(Button.left)

    def update(self):
        self.fen.update()

    def place_all_objects(self):
        for list_objects in self.objects:
            for object in list_objects:
                object.place(x=object.x, y=object.y)