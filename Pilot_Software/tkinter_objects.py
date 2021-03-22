import tkinter as tk
from pynput.mouse import Button, Controller
import time
import os

import tkinter_window


class Tkinter_button(tk.Button):
    '''Créer les boutons de commande'''
    def __init__(self, application, id):
        tk.Button.__init__(self, application)

        self.app = application
        self.id = id
        if self.app.name == 'main':
            self.clicked = False

            if self.id == 0:
                self.bg, self.fg, self.cursor, self.command = 'green3', 'black', 'hand2', self.motor_direction
                self.config(text='La rotation est\ndirecte', width=16, height=2, bg=self.bg, fg=self.fg, font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 460, 210

            if self.id == 1:
                self.bg, self.fg, self.cursor, self.command = 'red', 'black', 'hand2', self.def_pilote_mode
                self.config(text='Pilotage manuel', width=16, height=2, bg=self.bg, fg=self.fg,
                            cursor=self.cursor, font='Arial 11 bold', command=self.command)
                self.x, self.y = 630, 210

            if self.id == 2:
                self.bg, self.fg, self.cursor, self.command = 'green3', 'black', 'hand2', self.motor_start_stop
                self.config(text='Démarrer le moteur', width=16, height=2, bg=self.bg, fg=self.fg, font='Arial 11 bold',
                            relief=tk.RAISED, cursor=self.cursor, command=self.command)
                self.x, self.y = 460, 290

            if self.id == 3:
                self.bg, self.fg, self.cursor, self.command = 'green3', 'black', 'hand2', self.acquisition
                self.config(command=self.command, width=16, height=2,
                            text='Débuter Acquisition', bg=self.bg, fg=self.fg, cursor=self.cursor, font='Arial 11 bold')
                self.x, self.y = 550, 460

        self.bind('<Return>', self.command)
        self.init_y = self.y

    def acquisition(*args):
        self = args[0]
        if self.bg == 'green3':
            self.app.board.start_recording()
            self.bg = 'red'
            self.config(bg=self.bg, text='Stop Acquisition')

        elif self.bg == 'red':
            self.app.board.stop_recording()
            self.bg = 'green3'
            self.config(bg=self.bg, text='Débuter Acquisition')

    def motor_direction(*args):
        self = args[0]
        if self.bg == 'green3':
            self.bg = 'red'
            self.config(text='La rotation est\nindirecte', bg=self.bg)
            self.app.board.change_motor_rotation('indirect')
        else:
            self.bg = 'green3'
            self.config(text='La rotation est\ndirecte', bg=self.bg)
            self.app.board.change_motor_rotation('direct')

    def motor_start_stop(*args):
        self = args[0]

        if self.bg == 'green3':
            self.bg = 'red'
            self.config(text='Arrêter le moteur', bg=self.bg)
            self.app.board.start_motor(forced=True)
        else:
            self.bg = 'green3'
            self.config(text='Démarrer le moteur', bg=self.bg)
            self.app.board.stop_motor(forced=True)

    def def_pilote_mode(*args):
        self = args[0]

        if self.bg == 'red':
            self.bg = 'green3'
            self.config(text='Pilotage automatique', bg=self.bg)
            self.app.board.pilot_mode = 'auto'

        elif self.bg == 'green3':
            self.bg = 'red'
            self.config(text='Pilotage manuel', bg=self.bg)
            self.app.board.pilot_mode = 'manual'

    def unfocus(*args):
        self = args[0]
        self.app.labels[0].focus()


class Tkinter_label(tk.Label):

    def __init__(self, application, id):

        tk.Label.__init__(self, application)
        self.id = id
        self.app = application

        if self.app.name == 'main':
            if self.id == 0:
                self.config(text='Interface de pilotage du\nsystème de stockage d’énergie',
                            bg='light blue', fg='navy', width=30, font='Impact 30 bold')
                self.x, self.y = 85, 40

            if self.id == 1:
                self.config(text='________________________________________________', bg='light blue',
                            fg='blue', width=20, font='Arial 20')
                self.x, self.y = 240, 385
        self.init_y = self.y


class Tkinter_scale(tk.Scale):
    '''Graduation pour valeur d'entrée'''

    def __init__(self, application, id):
        tk.Scale.__init__(self, application)

        self.id = id
        self.app = application

        if self.app.name == 'main':
            if self.id == 0:
                self.value = 0
                self.x, self.y = 55, 235
                self.bg, self.fg, self.cursor = 'light blue', 'black', 'hand2'
                self.config(label='Vitesse Moteur', orient='horizontal', to=255, cursor=self.cursor, font='Arial 10',
                            resolution=1, tickinterval=25, length=350, bg=self.bg, fg=self.fg, command=self.get_value)
        self.init_y = self.y

    def get_value(self, value):
        self.value = value
        self.app.board.change_motor_speed(value)

    def change_state(self, state):
        if state == tk.DISABLED:
            self.config(state=state, fg='grey')
        else:
            self.config(state=state, fg='black')


class Tkinter_canvas(tk.Canvas):
    '''Console d'affichage'''

    def __init__(self, application, id):
        tk.Canvas.__init__(self, application)
        self.id = id
        self.app = application

        if self.id == 0:
            # Console
            self.config(bg='white', height=65, width=600, relief='raised')
            self.x, self.y = 100, 555

            self.create_text(20, 20, anchor='w', text='Console',
                             font='Arial 10 italic bold', fill='blue')
            self.create_text(20, 45, anchor='w', text='Pas de carte Arduino branchée',
                             font='Arial 10 italic bold', fill='red')
            self.create_text(580, 20, anchor='e', text=f'Port : {self.app.board.port}',
                             font='Arial 10 italic bold', fill='black')
            self.create_text(580, 45, anchor='e', text=f'FPS : {self.app.fps}',
                             font='Arial 10 italic bold', fill='grey70')

        elif self.id == 1:
            self.config(bg='white', height=100, width=400, relief='raised')
            self.x, self.y = 100, 435

            self.create_text(42, 20, text='Données',
                             font='Arial 10 italic bold', fill='blue')
            self.create_text(50, 45, text='Temps',
                             font='Arial 8 italic', fill='black')
            self.create_text(50, 70, text='',
                             font='Arial 8 italic', fill='black')
            self.create_text(150, 45, text='Courant mesuré',
                             font='Arial 8 italic', fill='black')
            self.create_text(150, 70, text='',
                             font='Arial 8 italic', fill='black')
            self.create_text(250, 45, text='Distance',
                             font='Arial 8 italic', fill='black')
            self.create_text(250, 70, text='',
                             font='Arial 8 italic', fill='black')
            self.create_text(350, 45, text='Vitesse angulaire',
                             font='Arial 8 italic', fill='black')
            self.create_text(350, 70, text='',
                             font='Arial 8 italic', fill='black')

            self.create_line(100, 40, 100, 130)
            self.create_line(200, 40, 200, 130)
            self.create_line(300, 40, 300, 130)
        self.init_y = self.y


class Tkinter_entry(tk.Entry):
    '''boîtes d'entrée de texte pour consigne'''

    def __init__(self, application, id):
        tk.Entry.__init__(self, application)
        self.id = id
        self.app = application

        if self.app.name == 'main':
            if self.id == 0:
                self.config(width=15, font='Arial 12', fg='grey')
                self.insert(0, 'Vitesse spécifique')
                self.bind('<Return>', self.enter)
                self.bind('<Button-1>', self.type)
                self.bind_all('<Key>', self.type)
                self.x, self.y = 55, 330

            if self.id == 1:
                self.config(width=15, font='Arial 12', fg='grey')
                self.insert(0, 'Commentaires')
                self.bind('<Return>', self.enter)
                self.bind('<Button-1>', self.type)
                self.bind_all('<Key>', self.type)
                self.x, self.y = 550, 522
        self.init_y = self.y

    def enter(self, state):
        if self.id == 0:
            try:  # l'exception sert à ignorer si l'utilisateur entre une valeur absurde.
                value = int(self.get())
                self.delete(0, tk.END)
                if value >= 0 and value <= 255 and self.id == 0:
                    self.app.scales[0].set(value)
                    self.app.scales[0].value = value
            except:
                self.delete(0, tk.END)

        elif self.id == 1:
            if self.get() != '':
                self.unfocus()
            else:
                self.insert(0, 'Commentaires')
                self.config(fg='grey')
                self.app.labels[0].focus()

    def type(*args):
        self, event = args[0], args[1]
        if event.char == event.keysym or event.char == '<Button-1>':
            if self['fg'] == 'grey':
                self.delete(0, tk.END)
                self.config(fg='black')
            if self['fg'] == 'green':
                self.config(fg='black')

    def change_state(self, state):
        self.config(state=state)
        self.unfocus('state')

    def unfocus(*args):
        self = args[0]
        if self.id == 0:
            self.delete(0, tk.END)
            self.insert(0, 'Vitesse spécifique')
            self.config(fg='grey')
            self.app.labels[0].focus()

        if self.id == 1:
            if self.get() == '':
                self.insert(0, 'Commentaires')
                self.config(fg='grey')
            else:
                self.config(fg='green')
            self.app.labels[0].focus()


class Tkinter_checkbox(tk.Tk):

    def __init__(self, parent_app):
        tk.Tk.__init__(self)
        self.parent_app = parent_app
        self.buttons = []
        self.length, self.height = 480, 500 #650
        self.x, self.y = -10, 0
        self.geometry(f'{self.length}x{self.height}+{self.x}+{self.y}')
        self.center_position = ((self.length/2)-9 + self.x, (self.height/2)+9 + self.y)
        self.configure(bg='light blue')
        self.title('All Excels')

        class small_button(tk.Button):
            def __init__(self, app, id, name):
                tk.Button.__init__(self, app)
                self.app, self.id, self.name = app, id, name
                self.config(text=self.name[-30:], command=self.button_command, font='Arial 10 underline', bg="light blue", fg='blue', cursor='hand2')
                self.place(x=15, y=100+self.id*50)
                self.app.bind('<Return>', self.button_command)
            def button_command(*args):
                self = args[0]
                try: os.startfile(self.name)
                except: print("can't")

        l=tk.Label(self, text='All excels', font='Impact 20 bold', fg='navy', bg='light blue', width=10)
        l.place(x=self.center_position[0]-65, y=10)

        for i in range(len(parent_app.excel_created)):
            self.buttons.append(small_button(self, i, parent_app.excel_created[i]))
        self.parent_app.sub_windows.append(self)
        self.id = len(self.parent_app.sub_windows)-1
        self.bind('<Escape>', self.kill)
        self.protocol('WM_DELETE_WINDOW', self.kill)

        def click():
            self.mouse_click(position = (self.center_position[0], 100))
        self.after(300, click)

    def kill(*args):
        self = args[0]
        self.parent_app.sub_windows.pop(self.id)
        self.mouse_click(position = self.parent_app.center_position)
        self.destroy()

    def mouse_click(*args, position = None):
        self = args[0]
        mouse = Controller()
        if position == None:
            position = Controller().position
        mouse.position = position
        mouse.press(Button.left)
        mouse.release(Button.left)
