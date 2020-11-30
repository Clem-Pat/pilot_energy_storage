import tkinter as tk
from pynput.mouse import Button, Controller
import time
import matplotlib.pyplot as plt

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

        if self.name == 'main':
            self.x, self.y = 450, 0
            self.center_position = (424 + self.x, 310 + self.y)
            self.length, self.height = 800, 800
            self.fen.title("Interface de pilotage du système de stockage d'énergie")
            self.fen.configure(bg="light blue")
            self.t0 = time.time()
            self.buttons = [tkinterButton(self, i) for i in range(5)]
            self.labels = [tkinterLabel(self, i) for i in range(2)]
            self.scales = [tkinterScale(self, i) for i in range(1)]
            self.canvas = [tkinterCanvas(self, i) for i in range(2)]
            self.entrys = [tkinterEntry(self, i) for i in range(1)]
            self.objects = [self.buttons, self.labels, self.scales, self.canvas, self.entrys]

            self.board.app = self
            self.board.reload()
            self.fen.bind('<space>', self.buttons[2].motor_start_stop)
            self.particular_pot_value = [None, None]


        elif self.name == "init_pot":
            self.x, self.y = 10, 50
            self.center_position = (316 + self.x, 236 + self.y)
            self.length, self.height = 650, 500
            self.fen.title("Initialisation potentiomètres")
            self.fen.configure(bg="grey70")
            self.buttons = [tkinterButton(self, i) for i in range(2)]
            self.labels = [tkinterLabel(self, i) for i in range(3)]
            self.objects = [self.buttons, self.labels]

        self.fen.geometry("{}x{}+{}+{}".format(str(self.length),
                                               str(self.height), str(self.x), str(self.y)))
        self.fen.resizable(width=False, height=False)
        self.fen.bind('<Escape>', self.destroy)
        self.fen.bind('<Control_L>r', self.reload)
        self.fen.bind('<Control_L>m', self.get_mouse_position)
        self.fen.bind('<Control_L><Return>', self.mouse_click)
        self.fen.bind('<Control_L>p', self.plot_recorded_mesures)
        self.fen.bind('<question>', self.print_shortcut)
        self.fen.protocol("WM_DELETE_WINDOW", self.destroy)

        self.place_all_objects()
        self.update()
        self.mouse_click(position = self.center_position)


    def reload(*args):
        self = args[0]
        if self.parent_app != None:
            self.parent_app.reload()
        try: self.destroy()
        except: pass
        main.main()

    def destroy(*args):
        self = args[0]

        if str(self.fen.focus_get())[:14] == '.!tkinterentry' or str(self.fen.focus_get())[:15] == '.!tkinterbutton':
            self.fen.focus_get().unfocus()

        else:
            if self.init_pot_app != None:
                try: self.init_pot_app.fen.destroy()
                except: pass
                self.init_pot_app = None
            if self.parent_app != None:
                self.parent_app.init_pot_app = None
            self.fen.destroy()

    def get_mouse_position(*args):
        self = args[0]
        mouse = Controller()
        position = (mouse.position[0] - self.x - 10, mouse.position[1] - self.y - 30)
        print('Position : {}'.format(position))

    def mouse_click(*args, position = None):
        self = args[0]
        mouse = Controller()
        if position == None:
            position = Controller().position
        mouse.position = position
        mouse.press(Button.left)
        mouse.release(Button.left)

    def print_shortcut(*args):
        print("échap : Détruire l'app\nctrl+r : Recharger l'app\nctrl+m : Afficher la position de la souris dans l'app\nctrl+entrée : cliquer\nespace : Démarrer/Arrêter le moteur\nctrl+p : plot la dernière acquisition \nmaj+? : Aide raccourcis\n")

    def plot_recorded_mesures(*args):

        def close_plot(event):
            if event.key == 'escape':
                plt.close()

        self = args[0]
        plt.connect("key_press_event", close_plot)
        plt.plot(self.board.time_list, self.board.distance_list)
        plt.plot(self.board.time_list, self.board.rotation_list)
        plt.plot(self.board.time_list, self.board.bits_list)
        print(self.board.bits_list)
        plt.show()

    def readable_time(self):
        t = time.time() - self.t0
        temps_tuple = time.gmtime(t)
        reste = t - temps_tuple[3] * 3600.0 - temps_tuple[4] * \
            60.0 - temps_tuple[5] * 1.0  # on récupère le reste
        # Affiche les dixièmes et centièmes de l'arrondi
        reste = ("%.2f" % reste)[-2::]
        tt = time.strftime("%H:%M:%S", temps_tuple) + "," + reste
        return tt

    def update(self):
        if self.name == "main":
            self.canvas[1].itemconfig(3, text=self.readable_time())
            self.canvas[1].itemconfig(5, text="{:.3f}".format(self.board.analog_pot)) #avec que 3 décimales
            self.canvas[1].itemconfig(7, text="{:.3f}".format(self.board.analog_cap))

            if self.init_pot_app != None:
                try:
                    self.init_pot_app.update()
                except:
                    self.init_pot_app = None

        elif self.name == "init_pot":
            if self.parent_app.particular_pot_value[0] == None :
                self.labels[1].config(text='Valeur 0 potentiomètre : {:.3f}'.format(self.board.analog_pot))
            if self.parent_app.particular_pot_value[1] == None :
                self.labels[2].config(text='Valeur 90 potentiomètre : {:.3f}'.format(self.board.analog_pot))

        self.fen.update()

    def place_all_objects(self):
        for list_objects in self.objects:
            for object in list_objects:
                object.place(x=object.x, y=object.y)
