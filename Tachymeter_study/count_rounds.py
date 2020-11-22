import tkinter as tk
import pyfirmata
import matplotlib.pyplot as plt
import os
from Create_excel_file import create_excel as create_excel
import numpy as np
from pynput.mouse import Button, Controller
import time

"""tachymeter pin A0
sensor pin A1
IN3 pin d7
IN4 pin d8
ENB pin d9"""
"""740g 0,75cL"""



class tkinterApp():
    def __init__(self, board):
        self.board = board
        self.fen = tk.Tk()
        self.x, self.y = 20, 20
        self.length, self.height = 800, 800
        self.button = tkinterButton(self)
        self.label = tkinterLabel(self)
        self.scale = tkinterScale(self)
        self.place_all_objects()

        self.L_reel = []
        self.L_capt = []
        self.path = os.path.dirname(os.path.abspath(__file__))

        self.fen.bind('<Control_L>p', self.get_mouse_position)
        self.fen.geometry("{}x{}+{}+{}".format(str(self.length),
                                               str(self.height), str(self.x), str(self.y)))
        self.path = os.path.dirname(os.path.abspath(__file__))

        self.t0 = time.time()
        self.scale.set(70)

    def place_all_objects(self):
        self.button.place(x=20,y=100)
        self.label.place(x=20, y=40)
        self.scale.place(x=self.scale.x, y=self.scale.y)

    def create_excel_file(self):
        mean_speeds = [self.board.mesures_duration[i]*self.board.max_number_mesures for i in range(len(self.board.mesures_duration))]
        create_excel(mean_speeds,self.board.mean_tachymeter_tension_values,self.path)
        pass

    def get_mouse_position(*args):
        self = args[0]
        mouse = Controller()
        position = (mouse.position[0] - self.x - 10, mouse.position[1] - self.y - 30)
        print('Position : {}'.format(position))

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
        if self.board.arduinoboard != None :

            value = self.board.get_sensor_value()
            self.label.config(text = str(self.board.count_rounds) + ' : ' + str(self.readable_time()))

            if value < 10 and self.board.rising_edge == 0:
                self.board.rising_edge = 1
                self.board.count_rounds += 1
                self.board.mean_tachymeter_tension_values[self.board.number_mesure] += self.board.tachymeter.read()

            if value >= 10 and self.board.rising_edge == 1:
                self.board.rising_edge = 0

            if self.board.count_rounds >= self.board.max_number_mesures:
                self.board.mesures_duration[self.board.number_mesure] = time.time()-self.t0
                self.board.mean_tachymeter_tension_values[self.board.number_mesure] *= 1/self.board.max_number_mesures
                self.board.number_mesure += 1
                self.board.count_rounds = 0

                future_scale_value = int(self.scale.value) + int(255//25)
                if  future_scale_value <= 255:
                    self.scale.value = future_scale_value
                    self.scale.set(self.scale.value)
                    self.t0 = time.time()
                else:
                    self.button.stop()


        self.fen.update()


class tkinterButton(tk.Button):
    def __init__(self, app):
        tk.Button.__init__(self, app.fen)
        self.app = app
        self.config(text='STOP', cursor='hand2', bg='red',font='Arial 10 bold', command=self.stop)

    def stop(self):
        self.app.fen.destroy()

        if self.app.board.arduinoboard != None:
            print('plot !!')
            self.app.create_excel_file()
            self.app.scale.get_value(0)
            mean_speeds = [self.app.board.mesures_duration[i]*self.app.board.max_number_mesures for i in range(len(self.app.board.mesures_duration))]
            plt.plot(mean_speeds, self.app.board.mean_tachymeter_tension_values,'g+')
            plt.show()


class tkinterLabel(tk.Label):
    def __init__(self, app):
        tk.Label.__init__(self, app.fen)
        self.app = app
        self.config(text='None', font='Arial 10 bold')


class tkinterScale(tk.Scale):
    """Graduation pour valeur d'entrée"""

    def __init__(self, application):
        tk.Scale.__init__(self, application.fen)

        self.app = application
        self.value = 0
        self.x, self.y = 192, 25
        self.bg, self.fg, self.cursor = 'light blue', 'black', 'hand2'
        self.config(label='Vitesse Moteur', orient='horizontal', to=255, cursor=self.cursor, font='Arial 10',
                    resolution=1, tickinterval=25, length=350, command=self.get_value)


    def get_value(self, value):
        self.value = value
        self.app.board.change_motor_speed(value)


class Board():
    def __init__(self, port):
        try :
            self.arduinoboard = pyfirmata.Arduino(port)
            iter8 = pyfirmata.util.Iterator(self.arduinoboard)
            iter8.start()

            self.tachymeter = self.arduinoboard.analog[0]
            self.sensor = self.arduinoboard.analog[1]
            self.tachymeter.enable_reporting()
            self.sensor.enable_reporting()

            self.enB = self.arduinoboard.get_pin('d:9:p')
            self.in3 = self.arduinoboard.get_pin('d:7:o')
            self.in4 = self.arduinoboard.get_pin('d:8:o')

            self.sensor_value = 9
            self.count_rounds = 0
            self.number_mesure = 0
            self.rising_edge = 0
            self.mesures_duration = [0]*25
            self.mean_tachymeter_tension_values = [0]*25
            self.max_number_mesures = 1

            self.in3.write(1)
            self.in4.write(0)
        except:
            self.arduinoboard = None
            print('Pas de carte Arduino branchée !!')

    def change_motor_speed(self, value):
        if self.arduinoboard != None:
            self.enB.write(int(value)/255)

    def get_sensor_value(self):
        if self.arduinoboard != None:
            x = float(self.sensor.read())

            # value = float(48.366*np.exp(-(float(x)-0.102)/0.109)+7.931) #3/2
            # value = float(71.36*np.exp(-(float(x)-78.2*10**(-3))/0.104)+9.445) #5/2 old
            if x>0.43 and x<=0.7: #entre 5 et 13 cm
                value = float(-24.891 * float(x) + 23.646)
            if x>=0.15 and x<=0.43: #entre 13cm et 40cm
                value = float(28.553 * np.exp(-(float(x) - 0.154) / 0.13) + 9.706)
            if x>0.12 and x<0.15: #entre 40 et 50cm
                value = float(-520 * float(x) + 117)
            if x>0.08 and x<=0.12: #entre 50 et 80cm
                value = float(79.49 * np.exp(- (float(x) - 0.089) / 0.084762) - 0.512)
            else:
                value = 90
            return value
        else:
            return 0


def main():
    board = Board('COM7')
    app = tkinterApp(board)

    while True:
        try:
            app.update()
        except:
            if board.arduinoboard != None:
                board.enB.write(0)
            break


if __name__=='__main__':
    main()
