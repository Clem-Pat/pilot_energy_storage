import tkinter as tk
import time
from pynput.mouse import Button, Controller
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys
from tkinter_objects import Tkinter_button, Tkinter_label, Tkinter_scale, Tkinter_canvas, Tkinter_entry
import main
import os

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
        self.offset = 0
        self.last_excel_created = None

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
            self.x, self.y = -10, 0
            self.length, self.height = 480, 650
            self.title('plot mesures')
            self.data_to_plot_name = ['u_mes', 'i_mes', 'speed', 'dist', 'motor_on']
            self.data_to_plot = [self.board.u_mes_list_plot, self.board.i_mes_list_plot, self.board.angular_speed_list_plot, self.board.distance_list_plot, self.board.motor_is_on_list_plot]
            self.frames = [Plot_frame(self, i, name=self.data_to_plot_name[i]) for i in range(len(self.data_to_plot))]
            self.objects = [self.frames]
            self.figures, self.axes = [0]*10, [0]*10
            self.color = ['b', 'r', 'g', 'c', 'm', 'y', 'k']

        self.center_position = ((self.length/2)-9 + self.x, (self.height/2)+9 + self.y)
        self.geometry(f'{self.length}x{self.height}+{self.x}+{self.y}')
        self.resizable(width=False, height=False)
        self.bind('<Escape>', self.kill)
        self.bind('<Control_L>r', self.reload)
        self.bind('<Control_L>m', self.get_mouse_position)
        self.bind('<Control_L>p', self.demand_plot)
        self.bind('<Control_L>o', self.open_excel)
        self.bind('<question>', self.print_shortcut)
        self.protocol('WM_DELETE_WINDOW', self.kill)
        self.bind_all("<MouseWheel>", self.scroll)

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
            self.canvas[1].itemconfig(5, text='{:.3f}'.format(self.board.i_mes)) #avec que 3 décimales
            self.canvas[1].itemconfig(7, text='{:.3f}'.format(self.board.distance))
            self.canvas[1].itemconfig(9, text='{:.3f}'.format(self.board.angular_speed))


            if self.init_pot_app != None:
                try:self.init_pot_app.refresh()
                except:self.init_pot_app = None

            if self.plot_app != None:
                try:self.plot_app.refresh()
                except:self.plot_app = None

        elif self.name == 'init_pot_app':
            if self.parent_app.particular_pot_value[0] == None :
                self.labels[1].config(text='Valeur 0 potentiomètre : {:.3f}'.format(self.board.angular_position))
            if self.parent_app.particular_pot_value[1] == None :
                self.labels[2].config(text='Valeur 90 potentiomètre : {:.3f}'.format(self.board.angular_position))

        elif self.name == 'plot_app':
            for list_objects in self.objects:
                for object in list_objects:
                    if type(object).__name__ == 'Plot_frame':
                        object.refresh()
            pass

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

    def open_excel(*args):
        self = args[0]
        if self.last_excel_created != None: os.startfile(self.last_excel_created)
        else: print('no last excel created to open')

    def print_shortcut(*args):
        print("échap : Détruire l'app\nctrl+r : Recharger l'app\nctrl+m : Afficher la position de la souris dans l'app\nctrl+entrée : cliquer\nespace : Démarrer/Arrêter le moteur\nctrl+p : plot la dernière acquisition \nmaj+? : Aide raccourcis\n")

    def scroll(*args):
        self, event = args[0], args[1]
        for list_objects in self.objects:
            for object in list_objects:
                if self.offset + event.delta/50 <= 0:
                    self.offset += event.delta/50
                    object.y += event.delta/50
                else:
                    self.offset = 0
                    object.y = object.init_y
                object.place(x=object.x, y=object.y)


class Point():
    def __init__(self, master, x, y, color='black'):
        self.master = master
        self.x, self.y = x, y
        self.color = color
        self = [self.master.create_line(self.x-10, self.y, self.x+10, self.y, fill=self.color),
                                   self.master.create_line(selfself.x, self.y-10, self.x, self.y+10, fill=self.color)]


class Plot_frame(tk.Canvas):
    def __init__(self, parent_app, id, name=None):
        tk.Canvas.__init__(self, parent_app)
        self.id = id
        self.app = parent_app
        self.name = name
        self.x_axis, self.y_axis = [], []
        self.height, self.width = 130, 480
        self.config(bg='white', height=self.height, width=self.width, relief='raised')
        self.x, self.y = 0, 5 + 130*self.id
        self.create_text(15, 10, anchor='w', text=self.name, font='Arial 10 italic bold')
        self.points, self.points_coords, self.continuous_lines = [], [], []
        self.cross_size, self.padding = 5, 5
        self.precision = 3
        self.legends, self.plot_legends = [[], []], True
        self.create_axis()
        self.init_y = self.y

    def refresh(self):
        self.x_axis = self.app.board.time_list_plot
        self.y_axis = self.app.data_to_plot[self.id]
        if self.points != []:
            for point in self.points:
                self.delete(point[0])
                self.delete(point[1]) #destroy les deux lignes du point
        if self.continuous_lines != []:
            for line in self.continuous_lines:
                self.delete(line)
        self.points, self.points_coords, self.continuous_lines = [], [], []
        for i in range(len(self.x_axis)):
            self.create_point(self.x_axis[i], self.y_axis[i])

        if self.x_axis != [] and self.plot_legends:
            self.update_legends()

        self.app.update()

    def create_point(self, x, y, create_lines=True):
        maxi = max(np.abs(max(self.y_axis)), np.abs(min(self.y_axis)))
        if min(self.y_axis) == max(self.y_axis):
            y = y + self.padding*2 + int((self.height-self.padding*4)/2)
        else:
            y = int(y*(self.padding*6-self.height)/(2*maxi)+(self.height/2))

        x = self.x_axis.index(x)*int((self.width-self.padding*4)/self.app.board.plot_limit) + self.padding*2
        self.points.append([self.create_line(x-self.cross_size, y, x+self.cross_size, y, fill='blue', width=2), self.create_line(x, y-self.cross_size, x, y+self.cross_size, fill='blue', width=2)])
        self.points_coords.append([x,y])
        if create_lines and len(self.points_coords) >= 2:
            self.continuous_lines.append(self.create_line(self.points_coords[-2][0], self.points_coords[-2][1], self.points_coords[-1][0], self.points_coords[-1][1], fill='grey'))

    def create_axis(self):
        self.create_line(self.padding*2, self.height-(self.padding*2), self.padding*2, self.padding*2)    # y_axis
        self.create_line(self.padding*2, self.height-(self.padding*2), self.width-self.padding*2, self.height-self.padding*2) # x_axis

        if self.plot_legends:
            self.create_line((self.padding*2)-self.cross_size, self.padding*3, self.padding*2+self.cross_size, self.padding*3)
            self.create_line((self.padding*2)-self.cross_size, int(self.height/2), self.padding*2+self.cross_size, int(self.height/2))
            self.create_line((self.padding*2)-self.cross_size, self.height-self.padding*3, self.padding*2+self.cross_size, self.height-self.padding*3)
            for i in range(self.precision+1):
                self.legends[0].append(self.create_text(int(i*(self.width-20)/self.precision)+self.padding*2, self.height-(self.padding*2)+self.cross_size, text=' '))
                # self.legends[1].append(self.create_text((self.padding*2)-self.cross_size, int(((self.height+2*self.padding*3)/2)-self.padding*3), text=' ')) #Les textes de légende des ordonnées pas bien placés

    def update_legends(self):
        for i in range(self.precision+1):
            self.itemconfigure(self.legends[0][i], text='{:.1f}'.format(float(((max(self.x_axis)-min(self.x_axis))*(i))/self.precision)+min(self.x_axis)))
