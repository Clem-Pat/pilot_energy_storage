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
        self.motor_is_on = False
        self.analog_cap, self.analog_pot = self.get_sensor_value(), self.get_potentiometer_value()

    def reload(self):
        try:
            # On définit la carte Arduino qui est branchée sur le port COM8
            self.arduinoboard = pyfirmata.Arduino(self.port)
            self.app.canvas[0].itemconfig(3,  text='Arduino branchée {}        '.format(self.port), fill='green')
        except:
            self.arduinoboard = None

        if self.arduinoboard != None:
            # On accepte de soutirer des infos à la carte
            self.iterate = pyfirmata.util.Iterator(self.arduinoboard)
            # On démarre la lecture des données (itérative cad qu'on actualise la lecture des données)
            self.iterate.start()

            for i in self.analog_pins_used:
                # On accepte la lecture des données de la pin analogue 0
                self.arduinoboard.analog[i].enable_reporting()

            # On attend un peu pour laisser le temps à la carte de charger
            time.sleep(1)

            self.pin = {}
            for i in self.analog_pins_used:
                self.pin["A" + str(i)] = self.arduinoboard.analog[i]
                self.pin["A" + str(i)].value = self.pin["A" + str(i)].read()
                time.sleep(0.5)
            for i in self.digital_pins_used:
                self.pin["d" + str(i)] = self.arduinoboard.get_pin('d:' + str(i) + ':s')
                self.pin["d" + str(i)].value = 90
                self.pin["d" + str(i)].write(self.pin["d" + str(i)].value)

        else:
            self.pin = {}
            for i in self.analog_pins_used:
                self.pin["A" + str(i)] = None
            for i in self.digital_pins_used:
                self.pin["d" + str(i)] = None

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

    def reupload_motor_command(self):
        if self.arduinoboard != None:
            if self.motor_is_on:
                #sens de rotation :
                if self.app.buttons[0]['text'] == 'La rotation est\ndirecte':
                    self.pin['d7'].write(0)
                    self.pin['d8'].write(1)
                elif self.app.buttons[0]['text'] == 'La rotation est\nindirecte':
                    self.pin['d7'].write(1)
                    self.pin['d8'].write(0)

                #vitesse de rotation :
                self.pin['d9'].write(self.app.scales[0].value)
            else:
                self.pin['d9'].write(0)

        else:
            pass
