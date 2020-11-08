import tkinter as tk  # module d'interface graphique
from pynput.mouse import Button, Controller
import time

import tkinter_window


class tkinterButton(tk.Button):
    """Créer les boutons de commande"""

    def __init__(self, application, id):
        tk.Button.__init__(self, application.fen)

        self.app = application
        self.id = id
        if self.app.name == 'main':
            self.clicked = False

            if self.id == 0:
                self.bg, self.fg, self.cursor = 'green3', 'black', 'hand2'
                self.config(text="La rotation est\ndirecte", width=16, height=2, bg=self.bg, fg=self.fg, font="Arial 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.motor_direction)
                self.x, self.y = 460, 210

            if self.id == 1:
                self.bg, self.fg, self.cursor = 'green3', 'black', 'hand2'
                self.config(text="Démarrer le moteur", width=16, height=2, bg=self.bg, fg=self.fg, font="Arial 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.motor_start_stop)
                self.x, self.y = 460, 290

            if self.id == 2:
                self.bg, self.fg, self.cursor = "red", 'black', "hand2"
                self.config(text='Pilotage manuel', width=16, height=2, bg=self.bg, fg=self.fg,
                            cursor=self.cursor, font='Arial 11 bold', command=self.def_pilote_mode)
                self.x, self.y = 630, 210

            if self.id == 3:
                self.bg, self.fg, self.cursor = "blue", 'black', "hand2"
                self.config(command=self.initialiser_potentiometres, width=16, height=2,
                            text='Init Potentiomètre', bg=self.bg, fg=self.fg, cursor=self.cursor, font='Arial 11 bold')
                self.x, self.y = 500, 460

        elif self.app.name == "init_pot":
            self.value = 444
            self.bg, self.fg, self.cursor = "grey70", 'black', "hand2"
            if self.id == 0:
                self.config(width=20, height=2, command=self.def_value, font='Arial 11 bold',
                            text='Init 0 potentiomètre', bg=self.bg, fg=self.fg, cursor=self.cursor)
                self.x, self.y = 100, 200

            elif self.id == 1:
                self.config(width=20, height=2, command=self.def_value, font='Arial 11 bold',
                            text='Init 90 potentiomètre', bg=self.bg, fg=self.fg, cursor=self.cursor)
                self.x, self.y = 350, 200

    def def_value(self):
        if self.app.board.arduinoboard != None:
            """potentiometre pin A0"""
            self.value = self.app.board.pin["A0"].read()

    def initialiser_potentiometres(self):
        init_pot_app = tkinter_window.tkinterWindow(
            "init_pot", self.app.board, parent_app=self.app)
        self.app.init_pot_app = init_pot_app
        init_pot_app.place_all_objects()

    def motor_direction(self):
        if self.bg == 'green3':
            self.bg = 'red'
            self.config(text="La rotation est\nindirecte", bg=self.bg)
        else:
            self.bg = 'green3'
            self.config(text="La rotation est\ndirecte", bg=self.bg)

    def motor_start_stop(self):
        if self.bg == 'green3':
            self.bg = 'red'
            self.config(text="Arrêter le moteur", bg=self.bg)
            self.app.board.motor_is_on = True
        else:
            self.bg = 'green3'
            self.config(text="Démarrer le moteur", bg=self.bg)
            self.app.board.motor_is_on = False

    def def_pilote_mode(self):

        if self.bg == 'red':
            self.bg = 'green3'
            self.config(text='Pilotage automatique', bg=self.bg)
            self.app.pilot_mode = 'auto'
            self.app.scales[0].change_state(tk.DISABLED)
            self.app.entrys[0].change_state(tk.DISABLED)

        elif self.bg == 'green3':
            self.bg = 'red'
            self.config(text='Pilotage manuel', bg=self.bg)
            self.app.pilot_mode = 'manual'
            self.app.scales[0].change_state(tk.NORMAL)
            self.app.entrys[0].change_state(tk.NORMAL)


class tkinterLabel(tk.Label):

    def __init__(self, application, id):

        tk.Label.__init__(self, application.fen)
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

        elif self.app.name == 'init_pot':
            if self.id == 0:
                self.config(text='Initialisation du potentiomètre', bg='grey70',
                            fg='black', font='Impact 30 bold')
                self.x, self.y = 55, 40


class tkinterScale(tk.Scale):
    """Graduation pour valeur d'entrée"""

    def __init__(self, application, id):
        tk.Scale.__init__(self, application.fen)

        self.id = id
        self.app = application

        if self.app.name == 'main':
            if self.id == 0:
                self.value = 0
                self.x, self.y = 55, 235
                self.bg, self.fg, self.cursor = 'light blue', 'black', 'hand2'
                self.config(label='Vitesse Moteur', orient='horizontal', to=255, cursor=self.cursor, font='Arial 10',
                            resolution=1, tickinterval=25, length=350, bg=self.bg, fg=self.fg, command=self.get_value)

    def get_value(self, value):
        self.value = value

    def change_state(self, state):
        if state == tk.DISABLED:
            self.config(state=state, fg='grey')
        else:
            self.config(state=state, fg='black')


class tkinterCanvas(tk.Canvas):
    """Console d'affichage"""

    def __init__(self, application, id):
        tk.Canvas.__init__(self, application.fen)
        self.id = id
        self.app = application

        if self.id == 0:
            # Console
            self.config(bg="white", height=65, width=600, relief='raised')
            self.x, self.y = 100, 555

            self.create_text(42, 20, text="Console",
                             font="Arial 10 italic bold", fill="blue")
            self.create_text(56, 57, text=' ',
                             font="Arial 10 italic bold", fill="black")
            self.create_text(110, 40, text='Pas de carte Arduino branchée',
                             font="Arial 10 italic bold", fill="red")
            self.create_text(570, 20, text=self.app.board.port,
                             font="Arial 10 italic bold", fill="black")

        elif self.id == 1:
            self.config(bg="white", height=100, width=300, relief='raised')
            self.x, self.y = 100, 435

            self.create_text(42, 20, text='Données',
                             font="Arial 10 italic bold", fill="blue")
            self.create_text(50, 45, text='Temps',  # 1
                             font="Arial 8 italic", fill="black")
            self.create_text(50, 70, text='',
                             font="Arial 8 italic", fill="black")
            self.create_text(150, 45, text='Potentiomètre',  # 2
                             font="Arial 8 italic", fill="black")
            self.create_text(150, 70, text='',
                             font="Arial 8 italic", fill="black")
            self.create_text(250, 45, text='Distance',  # 3
                             font="Arial 8 italic", fill="black")
            self.create_text(250, 70, text='',
                             font="Arial 8 italic", fill="black")

            self.create_line(100, 40, 100, 130)
            self.create_line(200, 40, 200, 130)


class tkinterEntry(tk.Entry):
    """boîtes d'entrée de texte pour consigne"""

    def __init__(self, application, id):
        tk.Entry.__init__(self, application.fen)
        self.id = id
        self.app = application

        if self.app.name == 'main':
            if self.id == 0:
                self.config(width=15, font='Arial 12', fg='grey')
                self.insert(0, 'Vitesse spécifique')
                self.bind('<Return>', self.enter)
                self.bind('<Button-1>', self.type)
                self.x, self.y = 55, 330

    def enter(self, state):
        try:  # l'exception sert à ignorer si l'utilisateur entre une valeur absurde.
            value = int(self.get())
            self.delete(0, tk.END)
            if value >= 0 and value <= 255 and self.id == 0:
                self.app.scales[0].set(value)
                self.app.scales[0].value = value
        except:
            self.delete(0, tk.END)

    def type(self, state):
        if self['fg'] == 'grey':
            self.delete(0, tk.END)
            self.config(fg='black')

    def change_state(self, state):
        self.delete(0, tk.END)
        self.insert(0, 'Vitesse spécifique')
        self.config(state=state, fg='grey')
        self.app.labels[1].focus()
