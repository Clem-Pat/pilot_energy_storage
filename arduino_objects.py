import pyfirmata  # module de communication avec la carte Arduino
import time
import numpy as np

"""pot pin A0
sensor pin A1
IN3 pin d7
IN4 pin d8
ENB pin d9"""

class Arduino_board():

    def __init__(self, usb_port, analogs, digitals):

        self.name = 'board_' + usb_port
        self.port = usb_port
        self.analog_pins_used = analogs
        self.digital_pins_used = digitals
        self.app = None
        self.arduinoboard = None
        self.pin = None
        self.analog_cap, self.analog_pot = self.get_sensor_value(), self.get_potentiometer_value()

    def reload(self):
        try:
            # On définit la carte Arduino qui est branchée sur le port COM8
            self.arduinoboard = pyfirmata.Arduino(self.port)
            self.app.canvas[0].itemconfig(3,  text='Arduino branchée {}'.format(self.port), fill='green')
        except:
            self.arduinoboard = None

        if self.arduinoboard != None:
            self.iterate = pyfirmata.util.Iterator(self.arduinoboard)
            self.iterate.start()
            time.sleep(1)

            self.pin = {}
            for i in self.analog_pins_used:
                self.arduinoboard.analog[i].enable_reporting()
                self.pin["A" + str(i)] = self.arduinoboard.analog[i]
                self.pin["A" + str(i)].value = self.pin["A" + str(i)].read()
                time.sleep(0.5)
            for j in self.digital_pins_used:
                self.pin["d" + str(j)] = self.arduinoboard.get_pin('d:' + str(j) + ':s')
                self.pin["d" + str(j)].value = None

            self.init_board()

        else:
            self.pin = {}
            for i in self.analog_pins_used:
                self.pin["A" + str(i)] = None
            for i in self.digital_pins_used:
                self.pin["d" + str(i)] = None


    def init_board(self):
        self.pin["d9"].write(self.app.scales[0].value)
        self.pin['d7'].write(0)
        self.pin['d8'].write(1)


    def get_sensor_value(self):
        if self.arduinoboard != None:
            if 1 in self.analog_pins_used:
                x = self.pin['A1'].read()
                try :
                    value = float(48.366*np.exp(-(float(x)-0.102)/0.109)+7.931)
                    if value>=0 and value<=100:
                        return value
                    else:
                        return 1
                except:
                    return 0
        else:
            return 0


    def get_potentiometer_value(self):
        if self.arduinoboard != None:
            return self.pin['A0'].read()
        else:
            return 0


    def change_motor_rotation(self, rotation_direction):
        if self.arduinoboard != None:
            #sens de rotation :
            if rotation_direction == 'direct':
                self.pin['d7'].write(0)
                self.pin['d8'].write(1)
            elif rotation_direction == 'indirect':
                self.pin['d7'].write(1)
                self.pin['d8'].write(0)


    def change_motor_speed(self, value):
        self.pin['d9'].write(value)

    def stop_motor(self):
        self.pin['d9'].write(0)
    def start_motor(self):
        self.pin['d9'].write(self.app.scales[0].value)
