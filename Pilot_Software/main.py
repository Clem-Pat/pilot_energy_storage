from sys import platform
import glob
import serial.tools.list_ports

import arduino_objects
import tkinter_window

'''
637.8 g
Voltmeter pin A0
Ammeter pin A1
Voltmeter 2 pin A2
Encoder SW pin d2
        DT pin d3
        CLK pin d4
Hbridge IN3 pin d7
        IN4 pin d8
        ENB pin d9'''
'''740g 0,75cL'''

def main():
    port = 'COM7'
    board = arduino_objects.Arduino_uno_board(port, analogs=[0,1,2], output_pins=[7,8], input_pins=[2,3,4], pwm_pins=[9])
    app = tkinter_window.Tkinter_window('main', board)

    while True:
        board.u_mes = board.get_voltmeter_value(1)
        board.u_mes2 = board.get_voltmeter_value(2)
        board.i_mes = board.get_ammeter_value()
        board.angular_position = board.get_angular_position_value()
        board.angular_speed = board.get_angular_speed_value()
        board.distance = board.get_distance_value()
        board.record_mesures()

        if board.pilot_mode == 'auto' :
            if board.motor_is_on and board.distance < 10 :
                board.stop_motor()
            if not board.motor_is_on and board.distance >= 10 and not board.motor_is_forced:
                board.start_motor()

        try: app.refresh()
        except:
            board.exit()
            break
if __name__ == '__main__':
    main()
