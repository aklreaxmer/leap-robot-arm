import Leap
import time
import sys
import serial

controller = Leap.Controller()
ser = serial.Serial("COM6", 9600)


while True:
    frame = controller.frame()
    if not frame.fingers.is_empty:
        fingers = frame.fingers

        # if more than three fingers are extended, the claw should open
        extend_count = 0 
        for f in range(0, 5):
            if fingers[f].is_extended:
                extend_count = extend_count + 1
                
        ''' communicate with arduino (write to serial) '''
        if extend_count >= 3:
            ser.write(chr(-1))# start byte
            ser.write(chr(3)) # servo
            ser.write(chr(0)) # angle to write
            print "open"

        # if less than 3 fingers extended (hand is closed), close the claw
        else:
            ser.write(chr(-1))
            ser.write(chr(3))
            ser.write(chr(60))
            print "closed"

        # Y position of palm determines vertical servo position
        hand_y = frame.hands.rightmost.stabilized_palm_position.y
        ser.write(chr(-1))
        ser.write(chr(2))
        ser.write(chr(180-int(hand_y)))
        time.sleep(.01)

        # X position determines horizontal servo position
        hand_x = frame.hands.rightmost.stabilized_palm_position.x
        ser.write(chr(-1))
        ser.write(chr(1))
        ser.write(chr(int(hand_x)))
        time.sleep(.01)

