import tkinter as tk
import pyfirmata
import time
import matplotlib.pyplot as plt

import arduino_objects
import tkinter_window

"""
Voltmeter pin A0
sensor pin A1
tachymeter pin A2
IN3 pin d7
IN4 pin d8
ENB pin d9"""
"""740g 0,75cL"""


def main():
    board = arduino_objects.Arduino_uno_board('COM7', analogs=[0,1,2], output_pins=[7,8], pwm_pins=[9])
    app = tkinter_window.tkinterWindow('main', board)

    while True:
        board.analog_tach = board.get_rotation_speed_value()
        board.analog_sens = board.get_sensor_value()
        board.analog_Umes = board.get_voltmeter_value()         #fps devient 1600 au lieu de 2000
        board.record_mesures()

        if board.pilot_mode == 'auto' :
            if board.motor_is_on and board.analog_sens < 10 :
                board.stop_motor()
            if not board.motor_is_on and board.analog_sens >= 10 and not board.motor_is_forced:
                board.start_motor()

        try:
            app.update()
        except:
            board.exit()
            break
if __name__ == "__main__":
    main()
