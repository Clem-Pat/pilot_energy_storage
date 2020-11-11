import pyfirmata  # module de communication avec la carte Arduino
import time
"""pot pin A0
IN3 pin d7
IN4 pin d8
ENB pin d9"""

board = pyfirmata.Arduino('COM7')

iterate = pyfirmata.util.Iterator(board)
iterate.start()
time.sleep(0.05)

A0pin = board.analog[0].enable_reporting()
IN3pin = board.get_pin('d:7:s')
IN4pin = board.get_pin('d:8:s')
ENBpin = board.get_pin('d:9:s')

IN3pin.write(1)
IN4pin.write(0)   #
ENBpin.write(100) #vitesse [0,255]

print(A0pin.read())
