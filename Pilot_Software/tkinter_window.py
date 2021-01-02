import tkinter as tk
import time
from pynput.mouse import Button, Controller
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
import numpy as np

from tkinter_objects import Tkinter_button, Tkinter_label, Tkinter_scale, Tkinter_canvas, Tkinter_entry
import main

class Tkinter_window(tk.Tk):

    def __init__(self, name_of_application, board, init_pot_app=None, parent_app=None):
        tk.Tk.__init__(self)
        self.name = name_of_application
        self.board = board
        self.init_pot_app = init_pot_app
        self.plot_app = None
        self.parent_app = parent_app
        self.t0 = time.time()
        self.last_tick_t = time.time()
        self.fps = 1
        self.tick = 0

        if self.name == 'main':
            self.x, self.y = 470, 0
            self.length, self.height = 800, 800
            self.title("Interface de pilotage du système de stockage d'énergie")
            self.configure(bg='light blue')
            self.buttons = [Tkinter_button(self, i) for i in range(5)]
            self.labels = [Tkinter_label(self, i) for i in range(2)]
            self.scales = [Tkinter_scale(self, i) for i in range(1)]
            self.canvas = [Tkinter_canvas(self, i) for i in range(2)]
            self.entrys = [Tkinter_entry(self, i) for i in range(2)]
            self.objects = [self.buttons, self.labels, self.scales, self.canvas, self.entrys]

            self.board.app = self
            self.board.reload()
            self.bind('<space>', self.buttons[2].motor_start_stop)
            self.particular_pot_value = [None, None]
            self.plot_demanded = False

        elif self.name == 'init_pot_app':
            self.x, self.y = 10, 50
            self.length, self.height = 650, 500
            self.title('Initialisation potentiomètres')
            self.configure(bg='grey70')
            self.buttons = [Tkinter_button(self, i) for i in range(2)]
            self.labels = [Tkinter_label(self, i) for i in range(3)]
            self.objects = [self.buttons, self.labels]

        elif self.name == 'plot_app':
            self.x, self.y = -10,0
            self.length, self.height = 480, 650
            self.title('plot mesures')
            self.objects = []
            self.figures, self.axes = [0]*10, [0]*10
            self.color = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
            self.data_to_plot_name = ['u_mes', 'speed', 'dist', 'bits', 'motor_on']
            self.data_to_plot = [self.board.u_mes_list_plot, self.board.angular_speed_list_plot, self.board.distance_list_plot, self.board.bits_list_plot, self.board.motor_is_on_list_plot]

        self.center_position = ((self.length/2)-9 + self.x, (self.height/2)+9 + self.y)
        self.geometry(f'{self.length}x{self.height}+{self.x}+{self.y}')
        self.resizable(width=False, height=False)
        self.bind('<Escape>', self.kill)
        self.bind('<Control_L>r', self.reload)
        self.bind('<Control_L>m', self.get_mouse_position)
        self.bind('<Control_L>p', self.demand_plot)
        self.bind('<question>', self.print_shortcut)
        self.protocol('WM_DELETE_WINDOW', self.kill)

        self.place_all_objects()
        self.refresh()
        self.mouse_click(position = self.center_position)

    def reload(*args):
        self = args[0]
        if self.parent_app != None:
            self.parent_app.reload()
        try: self.kill()
        except: pass
        main.main()

    def demand_plot(*args):
        self = args[0]
        if self.name == 'main':
            self.plot_demanded = not self.plot_demanded
            if self.plot_demanded:
                self.plot_app = Tkinter_window('plot_app', self.board, parent_app=self)
            else:
                self.plot_app.kill()

    def plot_mesures(*args):
        def plot(plot_app, x_axis, y_axis_list):
            for i in range(len(y_axis_list)):
                if len(y_axis_list) <= 4:
                    plot_app.figures[i] = Figure(figsize=(5, 1.7), dpi=100)
                    n = 160
                if len(y_axis_list) == 5:
                    plot_app.figures[i] = Figure(figsize=(5, 1.7), dpi=90)
                    n = 123
                plot_app.axes[i] = plot_app.figures[i].add_subplot(111)
                plot_app.axes[i].plot(x_axis, y_axis_list[i], plot_app.color[i], label=plot_app.data_to_plot_name[i], marker='+', ls='-')
                plot_app.axes[i].legend(loc='best', shadow=True, fontsize='small', markerscale=0.4)   #Ajouter une légende qui s'affiche au mieux sur le graphe
                try:
                    canvas = FigureCanvasTkAgg(plot_app.figures[i], master=plot_app).get_tk_widget()
                    canvas.place(x=0,y=n*i)
                except:
                    pass
            plot_app.axes[0].set(xlabel='temps (s)')
            plot_app.refresh()

        self = args[0]
        plot(self, self.board.time_list_plot, self.data_to_plot)

    def readable_time(self):
        t = time.time() - self.t0
        temps_tuple = time.gmtime(t)
        reste = t - temps_tuple[3] * 3600.0 - temps_tuple[4] * \
            60.0 - temps_tuple[5] * 1.0  # on récupère le reste
        reste = ('%.2f' % reste)[-2::]
        tt = time.strftime('%H:%M:%S', temps_tuple) + ',' + reste
        return tt

    def get_and_update_fps(self):
        t = time.time()
        if t-self.last_tick_t >= 0.5:
            self.fps = int(self.tick/(t-self.last_tick_t))
            if self.fps < 1/self.board.record_period:
                self.canvas[0].itemconfig(4, text=f'FPS : {self.fps} < f_acq !', fill='red')
            else:
                self.canvas[0].itemconfig(4, text=f'FPS : {self.fps}', fill='grey70')
            self.last_tick_t = time.time()
            self.tick = 0

    def refresh(self):
        if self.name == 'main':
            self.canvas[1].itemconfig(3, text=self.readable_time())
            self.canvas[1].itemconfig(5, text='{:.3f}'.format(self.board.u_mes)) #avec que 3 décimales
            self.canvas[1].itemconfig(7, text='{:.3f}'.format(self.board.distance))
            self.canvas[1].itemconfig(9, text='{:.3f}'.format(self.board.angular_speed))


            if self.init_pot_app != None:
                try:self.init_pot_app.refresh()
                except:self.init_pot_app = None

        elif self.name == 'init_pot_app':
            if self.parent_app.particular_pot_value[0] == None :
                self.labels[1].config(text='Valeur 0 potentiomètre : {:.3f}'.format(self.board.angular_position))
            if self.parent_app.particular_pot_value[1] == None :
                self.labels[2].config(text='Valeur 90 potentiomètre : {:.3f}'.format(self.board.angular_position))

        self.tick += 1
        if self.name == 'main':
            self.get_and_update_fps()
        self.update()

    def place_all_objects(self):
        for list_objects in self.objects:
            for object in list_objects:
                object.place(x=object.x, y=object.y)

    def kill(*args):
        self = args[0]
        if str(self.focus_get())[:15] == '.!tkinter_entry' or str(self.focus_get())[:16] == '.!tkinter_button':
            self.focus_get().unfocus()
        else:
            if self.name == 'main':
                if self.plot_app == None and self.init_pot_app == None:
                    self.destroy()
                if self.init_pot_app != None:
                    self.init_pot_app.kill()
                if self.plot_app != None:
                    self.plot_app.kill()

            if self.name == 'init_pot_app':
                try: self.destroy()
                except: pass
                self.parent_app.init_pot_app = None

            if self.name == 'plot_app':
                try: self.destroy()
                except: pass
                self.parent_app.plot_demanded = False
                self.parent_app.plot_app = None

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

        if self.name == 'plot_app':
            mouse.position = self.parent_app.center_position
            mouse.press(Button.left)
            mouse.release(Button.left)

    def print_shortcut(*args):
        print("échap : Détruire l'app\nctrl+r : Recharger l'app\nctrl+m : Afficher la position de la souris dans l'app\nctrl+entrée : cliquer\nespace : Démarrer/Arrêter le moteur\nctrl+p : plot la dernière acquisition \nmaj+? : Aide raccourcis\n")
