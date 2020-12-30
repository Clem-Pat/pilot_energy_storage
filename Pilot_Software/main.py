from sys import platform
import glob
import serial.tools.list_ports

import arduino_objects
import tkinter_window

'''
Voltmeter pin A0
Sensor pin A1
Tachymeter pin A2
Encoder SW pin d2
        DT pin d3
        CLK pin d4
Hbridge IN3 pin d7
        IN4 pin d8
        ENB pin d9'''
'''740g 0,75cL'''
'''Encoder law not perfect + get_angular_speed_value doesn't work'''

def find_port():
    if platform == 'win32':
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 1: return str(ports[0][0])
        else: return str(None)
    if platform == 'darwin':
        ports = list(glob.glob('/dev/tty.usbmodem*'))
        if len(ports) == 1: return str(ports[0])
        else: return str(None)

def main():
    port = find_port()
    board = arduino_objects.Arduino_uno_board(port, analogs=[0,1,2], output_pins=[7,8], input_pins=[2,3,4], pwm_pins=[9])
    app = tkinter_window.Tkinter_window('main', board)

    while True:
        board.u_mes = board.get_voltmeter_value()
        board.angular_position = board.get_angular_position_value()
        board.angular_speed = board.get_angular_speed_value()
        board.distance = board.get_distance_value()
        board.record_mesures()

        if board.pilot_mode == 'auto' :
            if board.motor_is_on and board.distance < 10 :
                board.stop_motor()
            if not board.motor_is_on and board.distance >= 10 and not board.motor_is_forced:
                board.start_motor()

        try:
            app.update()
        except:
            board.exit()
            break
if __name__ == '__main__':
    main()
