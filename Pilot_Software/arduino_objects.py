import pyfirmata
import time
import numpy as np
import os
import datetime

from excel_manager import Excel_manager

'''
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
# Sensor pin A1
# Tachymeter pin A2

class Arduino_uno_board():

    def __init__(self, usb_port, analogs=[], input_pins=[], output_pins=[], pwm_pins=[], servo_pins=[]):
        '''analogs = [0, 1, 2, 3, 4, 5], output_pins = [2, 4, 7, 8, 12, 13], pwm_pins=[3, 5, 6, 9, 10, 11]'''

        self.name = 'board_' + usb_port
        self.port = usb_port
        self.arduinoboard = None
        self.analog_pins = analogs
        self.pwm_pins = pwm_pins
        self.servo_pins = servo_pins
        self.input_pins = input_pins
        self.digital_pins = input_pins + output_pins + pwm_pins + servo_pins
        self.app = None
        self.pin = None
        self.pulley_radius = 5 #cm
        self.pilot_mode = 'manual'
        self.u_mes, self.u_mes2, self.i_mes, self.angular_speed, self.distance, self.motor_is_on = 0, 0, 0, 0, 0, False
        self.i_mes_moy, self.u_mes_moy, self.nbre_mesures = 0, 0, 0
        self.last_angular_position_time, self.last_angular_position = time.time(), 0
        self.angular_position_time, self.angular_position = time.time(), 0
        self.record_demanded = False
        self.record_period = 0.1  # période d'acquisition en secondes
        self.t0_record, self.time_list, self.u_mes_list, self.u_mes2_list, self.i_mes_list, self.angular_position_list, self.angular_speed_list, self.distance_list, self.bits_list, self.motor_is_on_list = time.time(), [0], [0.0], [0], [0], [self.angular_position], [self.angular_speed], [self.distance], [0], [int(self.motor_is_on)]
        self.time_list_plot, self.u_mes_list_plot, self.i_mes_list_plot, self.angular_speed_list_plot, self.distance_list_plot, self.bits_list_plot, self.motor_is_on_list_plot = [0], [0], [0], [self.angular_speed], [self.distance], [0], [int(self.motor_is_on)]
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.excel_manager = Excel_manager(self.app)
        self.angular_counter, self.old_clk, self.old_dt = 0, True, True
        self.plot_limit = 30

    def reload(self):
        self.excel_manager = Excel_manager(self.app)

        try:
            self.arduinoboard = pyfirmata.Arduino(self.port)
            self.app.canvas[0].itemconfig(
                2,  text='Arduino branchée {}'.format(self.port), fill='green')
        except:
            self.arduinoboard = None

        if self.arduinoboard != None:
            self.iterate = pyfirmata.util.Iterator(self.arduinoboard)
            self.iterate.start()
            time.sleep(1)

            self.pin = {}
            for i in self.analog_pins:
                self.arduinoboard.analog[i].enable_reporting()
                self.pin[f'A{i}'] = self.arduinoboard.analog[i]
                self.pin[f'A{i}'].value = self.pin[f'A{i}'].read()
                time.sleep(0.5)

            for j in self.digital_pins:
                if j in self.pwm_pins:
                    self.pin[f'd{j}'] = self.arduinoboard.get_pin(f'd:{j}:p')
                elif j in self.servo_pins:
                    self.pin[f'd{j}'] = self.arduinoboard.get_pin(f'd:{j}:s')
                elif j in self.input_pins:
                    self.pin[f'd{j}'] = self.arduinoboard.get_pin(f'd:{j}:i')
                else:
                    self.pin[f'd{j}'] = self.arduinoboard.get_pin(f'd:{j}:o')
                self.pin[f'd{j}'].value = None

            self.init_board()


        else:
            self.pin = {}
            for i in self.analog_pins:
                self.pin[f'A{i}'] = None
            for i in self.digital_pins:
                self.pin[f'd{i}'] = None

    def init_board(self):
        if self.arduinoboard != None:
            self.pin['d9'].write(0)
            self.pin['d7'].write(0)
            self.pin['d8'].write(1)

    def exit(self):
        if self.arduinoboard != None:
            self.arduinoboard.exit()

    def get_voltmeter_value(self, id):
        """returns tension mesured in volts"""
        if self.arduinoboard != None:
            if id == 1:
                return 25.34330509*self.pin['A0'].read()
            elif id == 2:
                return 3*5*self.pin['A2'].read()
        else:
            return 0

    def get_ammeter_value(self):
        if self.arduinoboard != None :
            # return 10*(self.pin['A1'].read()-0.5)
            return 0.03060430044*self.pin['A1'].read()
        else:
            return 0

    def get_angular_position_value(self):
        """returns angular position mesured in rounds"""
        if self.arduinoboard != None :
            self.last_angular_position = self.angular_position
            self.angular_position_time = time.time()

            now_dt = self.pin['d3'].read()
            now_clk = self.pin['d4'].read()

            if not now_clk and now_clk!=self.old_clk:
                if not now_dt : self.angular_counter += 1
                else: self.angular_counter -= 1

            now_sw = self.pin['d2'].read()
            if not now_sw:
                self.angular_counter = 0
            self.old_clk, self.old_dt = now_clk, now_dt
            return -(self.angular_counter)/20
        else: return 0

    def get_angular_speed_value(self):
        """returns the angular speed in rad/s"""
        """NOT TESTED YET"""
        # if len(self.angular_position_list) >= 2:
        #     if len(self.angular_position_list) >= 1/self.record_period:
        #         return (self.angular_position_list[-1]-self.angular_position_list[-int(1/self.record_period)])/(self.time_list[-1]-self.time_list[-int(1/self.record_period)])
        #     else:
        #         return self.record_period*(self.angular_position_list[-1]-self.angular_position_list[-2])/(self.time_list[-1]-self.time_list[-2])
        # else:
        #     return 0
        if self.angular_position_time-self.last_angular_position_time != 0:
            return (self.angular_position-self.last_angular_position)/(self.angular_position_time-self.last_angular_position_time)
        else: return 0

    def get_distance_value(self):
        """returns distance to mass in cm. (d=theta*pulley_radius)"""
        return self.angular_position* 2*np.pi * self.pulley_radius

    def change_motor_rotation(self, rotation_direction):
        if self.arduinoboard != None:
            if rotation_direction == 'direct':
                self.pin['d7'].write(0)
                self.pin['d8'].write(1)
            elif rotation_direction == 'indirect':
                self.pin['d7'].write(1)
                self.pin['d8'].write(0)

    def change_motor_speed(self, value):
        if self.arduinoboard != None and self.motor_is_on:
            self.pin['d9'].write(int(value) / 255)

    def stop_motor(self, forced=False):
        self.motor_is_on = False
        self.motor_is_forced = forced
        if self.arduinoboard != None:
            self.pin['d9'].write(0)

    def start_motor(self, forced=False):
        self.motor_is_on = True
        self.motor_is_forced = forced
        if self.arduinoboard != None:
            self.pin['d9'].write(int(self.app.scales[0].value) / 255)

    def start_recording(self):
        self.t0_record, self.time_list, self.u_mes_list, self.u_mes2_list, self.i_mes_list, self.angular_position_list, self.angular_speed_list, self.distance_list, self.bits_list, self.motor_is_on_list = time.time(), [0], [0.0], [0], [0], [self.angular_position], [self.angular_speed], [self.distance], [0], [int(self.motor_is_on)]
        self.record_demanded = True

    def record_mesures(self):
        self.u_mes_moy += self.u_mes
        self.i_mes_moy += self.i_mes
        self.nbre_mesures += 1

        if self.record_demanded == True:
            if (time.time() - self.t0_record) - self.time_list[-1] >= self.record_period:
                self.u_mes, self.i_mes = self.u_mes_moy/self.nbre_mesures, self.i_mes_moy/self.nbre_mesures
                self.time_list.append(time.time() - self.t0_record)
                self.u_mes_list.append(self.u_mes)
                self.u_mes2_list.append(self.u_mes2)
                self.i_mes_list.append(self.i_mes_moy)
                self.angular_position_list.append(self.angular_position)
                self.angular_speed_list.append(self.angular_speed)
                self.distance_list.append(self.distance)
                self.bits_list.append(self.app.scales[0].value)
                self.motor_is_on_list.append(int(self.motor_is_on))
                self.u_mes_moy, self.i_mes_moy, self.nbre_mesures = 0, 0, 0

        if (time.time() - self.app.t0) - self.time_list_plot[-1] >= self.record_period:
            self.time_list_plot.append(time.time() - self.app.t0)
            self.u_mes_list_plot.append(self.u_mes)
            self.i_mes_list_plot.append(self.i_mes)
            self.angular_speed_list_plot.append(self.angular_speed)
            self.distance_list_plot.append(self.distance)
            self.bits_list_plot.append(self.app.scales[0].value)
            self.motor_is_on_list_plot.append(int(self.motor_is_on))

            if len(self.time_list_plot) > self.plot_limit:
                self.time_list_plot.pop(0)
                self.u_mes_list_plot.pop(0)
                self.i_mes_list_plot.pop(0)
                self.angular_speed_list_plot.pop(0)
                self.distance_list_plot.pop(0)
                self.bits_list_plot.pop(0)
                self.motor_is_on_list_plot.pop(0)

            if self.app.plot_app != None:
                # self.app.plot_app.plot_mesures()
                pass

    def stop_recording(self):
        self.record_demanded = False
        L_data = [self.time_list, self.u_mes_list, self.u_mes2_list, self.i_mes_list, self.angular_position_list, self.angular_speed_list, self.distance_list, self.bits_list, self.motor_is_on_list]
        self.excel_manager.create_excel(L_data)
