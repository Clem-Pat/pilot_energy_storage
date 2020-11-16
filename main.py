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
    board = arduino_objects.Arduino_board('COM7', [0,1], [7,8,9,11]) #Définir la carte arduino et les 3 pins avec lesquelles on communique.
    app = tkinter_window.tkinterWindow('main', board) #Créer la fenêtre

    while True:
        board.analog_pot = board.get_potentiometer_value()
        board.analog_cap = board.get_sensor_value()

        if app.pilot_mode == 'auto' and board.analog_cap < 10:
                board.stop_motor()

        if board.arduinoboard != None :
            board.pin["d11"].write((int(app.scales[0].value))*180/255)

        # try:
        app.update()
        # except:
        #     break
        if app.buttons[0].bg == 'red':
            break


if __name__ == "__main__":
    main()
