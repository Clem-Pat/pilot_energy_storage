import tkinter as tk  #module d'interface graphique
import pyfirmata    #module de communication avec la carte Arduino
import time

import arduino_objects
import tkinter_window

"""pot pin A0
sensor pin A1
IN4 pin d8
IN3 pin d7
ENB pin d9"""

def chronometre(t):

    # Conversion en tuple (1970, 1, 1, 0, 0, 4, 3, 1, 0)
    temps_tuple = time.gmtime(t)
    reste = t - temps_tuple[3] * 3600.0 - temps_tuple[4] * \
        60.0 - temps_tuple[5] * 1.0  # on récupère le reste
    # Affiche les dixièmes et centièmes de l'arrondi
    reste = ("%.2f" % reste)[-2::]
    tt = time.strftime("%H:%M:%S", temps_tuple) + "," + reste
    return tt


def main():

    board = arduino_objects.Arduino_board('COM7', [0,1], [7,8,9]) #Définir la carte arduino et les 3 pins avec lesquelles on communique.

    app = tkinter_window.tkinterWindow('main', board) #Créer la fenêtre
    app.place_all_objects()

    t0 = time.time()
    while True:
        t = time.time() - t0
        chrono = chronometre(t)

        board.analog_pot = board.get_potentiometer_value()
        board.analog_cap = board.get_sensor_value()

        if app.pilot_mode == 'auto':
            if board.analog_cap < 10:
                board.motor_is_on = False

        try:
            board.reupload_motor_command()

            app.canvas[1].itemconfig(3, text=chrono)
            app.canvas[1].itemconfig(5, text="%.3f" %board.analog_pot) # Valeur rendue par le potentiomètre avec que 3 décimales
            app.canvas[1].itemconfig(7, text="%.3f" %board.analog_cap) # Valeur rendue par le capteur de distance avec que 3 décimales
            app.update()
        except:
            break


if __name__ == "__main__":
    main()
