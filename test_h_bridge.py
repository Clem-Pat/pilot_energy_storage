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

IN3pin = board.digital[7]
IN4pin = board.digital[8]
ENBpin = board.digital[9]

IN3pin.write(1)
IN4pin.write(0)   #
ENBpin.write(100) #vitesse [0,255]
