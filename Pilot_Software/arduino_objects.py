import pyfirmata  # module de communication avec la carte Arduino
import time
import numpy as np

"""pot pin A0
sensor pin A1
IN3 pin d7
IN4 pin d8
ENB pin d9"""

class Arduino_uno_board():

    def __init__(self, usb_port, analogs=[], output_pins=[], pwm_pins=[], servo_pins=[]):
        """analogs = [0, 1, 2, 3, 4, 5], output_pins = [2, 4, 7, 8, 12, 13], pwm_pins=[3, 5, 6, 9, 10, 11]"""

        self.name = 'board_' + usb_port
        self.port = usb_port
        self.arduinoboard = None
        self.analog_pins = analogs
        self.digital_pins = output_pins + pwm_pins + servo_pins
        self.pwm_pins = pwm_pins
        self.servo_pins = servo_pins
        self.app = None
        self.pin = None
        self.analog_cap, self.analog_pot = self.get_sensor_value(), self.get_potentiometer_value()
        self.motor_is_on = False
        self.pilot_mode = 'manual'

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
            for i in self.analog_pins:
                self.arduinoboard.analog[i].enable_reporting()
                self.pin["A" + str(i)] = self.arduinoboard.analog[i]
                self.pin["A" + str(i)].value = self.pin["A" + str(i)].read()
                time.sleep(0.5)

            for j in self.digital_pins:
                if j in self.pwm_pins:
                    self.pin["d" + str(j)] = self.arduinoboard.get_pin('d:' + str(j) + ':p')
                elif j in self.servo_pins:
                    self.pin["d" + str(j)] = self.arduinoboard.get_pin('d:' + str(j) + ':s')
                else:
                    self.pin["d" + str(j)] = self.arduinoboard.get_pin('d:' + str(j) + ':o')
                self.pin["d" + str(j)].value = None

            self.init_board()

        else:
            self.pin = {}
            for i in self.analog_pins:
                self.pin["A" + str(i)] = None
            for i in self.digital_pins:
                self.pin["d" + str(i)] = None


    def init_board(self):
        if self.arduinoboard != None :
            self.pin['d9'].write(0)
            self.pin['d7'].write(0)
            self.pin['d8'].write(1)


    def get_sensor_value(self):
        if self.arduinoboard != None:
            if 1 in self.analog_pins:
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
        if self.arduinoboard != None and self.motor_is_on:
            self.pin['d9'].write(int(value)/255)

    def stop_motor(self):
        self.motor_is_on = False
        if self.arduinoboard != None:
            self.pin['d9'].write(0)

    def start_motor(self):
        self.motor_is_on = True
        if self.arduinoboard != None:
            self.pin['d9'].write(int(self.app.scales[0].value)/255)
