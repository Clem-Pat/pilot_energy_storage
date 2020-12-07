import tkinter as tk
import pyfirmata
import time
import os
import matplotlib.pyplot as plt

import arduino_objects
import tkinter_window

"""PB : deuxième avquisition de mesures"""
"""TO DO : un plot en direct (fenêtre en plus à part)"""

"""pot pin A0
sensor pin A1
IN3 pin d7
IN4 pin d8
ENB pin d9"""
"""740g 0,75cL"""


def main():
    board = arduino_objects.Arduino_uno_board('COM7', analogs=[0,1], output_pins=[7,8], pwm_pins=[9])
    app = tkinter_window.tkinterWindow('main', board)

    while True:
        board.analog_pot = board.get_rotation_speed_value()
        board.analog_cap = board.get_sensor_value()
        board.record_mesures()

        if board.pilot_mode == 'auto' :
            if board.motor_is_on and board.analog_cap < 10 :
                board.stop_motor()
            if not board.motor_is_on and board.analog_cap >= 10 and not board.motor_is_forced:
                board.start_motor()

        try:
            app.update()
        except:
            board.exit()
            break

if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', 'output.dat')
    #
    # import pstats
    # from pstats import SortKey
    #
    # with open('output_time.txt', "w") as f:
    #     p = pstats.Stats("output.dat", stream=f)
    #     p.sort_stats('time').print_stats()
    #
    # with open('output_calls.txt', "w") as f:
    #     p = pstats.Stats("output.dat", stream=f)
    #     p.sort_stats('calls').print_stats()
    import pprofile
    profiler = pprofile.Profile()
    with profiler:
        main()
    profiler.dump_stats(os.path.dirname(os.path.abspath(__file__))+"\\profiler_stats.txt")
