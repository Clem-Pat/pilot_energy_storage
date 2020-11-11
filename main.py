import tkinter as tk  #module d'interface graphique
import pyfirmata    #module de communication avec la carte Arduino
import time

import arduino_objects
import tkinter_window

"""pot pin A0
sensor pin A1
IN3 pin d7
IN4 pin d8
ENB pin d9"""
"""740g 0,75cL"""


def main():

    board = arduino_objects.Arduino_board('COM7', [0,1], [7,8,9]) #Définir la carte arduino et les 3 pins avec lesquelles on communique.

    app = tkinter_window.tkinterWindow('main', board) #Créer la fenêtre
    app.place_all_objects()

    while True:

        board.analog_pot = board.get_potentiometer_value()
        board.analog_cap = board.get_sensor_value()

        if app.pilot_mode == 'auto':
            if board.analog_cap < 10:
                board.motor_is_on = False

        try:
            board.reupload_motor_command()

            app.update()
        except:
            break


if __name__ == "__main__":
    main()
