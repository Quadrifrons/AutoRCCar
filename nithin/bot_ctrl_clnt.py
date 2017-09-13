# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import time
import socket
import sys

sys_ip=sys.argv[1]
sys_ip="192.168.1.38"

# Client to initiate bot control
class MstrCtrl(object):
    def __init__():

        host=sys_ip
        port=5560
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,port))

        GPIO.setmode(GPIO.BOARD) # This is a mandatory step
        GPIO.setup(7,GPIO.OUT) # To setup channels to communicate with Pi
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(16,GPIO.OUT)

        GPIO.output(7,False)#ensuring that there is no output before keys are pressed
        GPIO.output(12,False)
        GPIO.output(13,False)
        GPIO.output(16,False)
        
        self.ctrl()

    def ctrl(direction):
        try:
            while True:

                reply = s.recv(1024)
                reply = reply.decode('utf-8')
                time.sleep(.030)
                GPIO.output(7,False)
                GPIO.output(12,False)
                GPIO.output(13,False)
                GPIO.output(16,False)
                char = reply
                if char == ord('q'):
                    break
                elif char == "up":
                    GPIO.output(7,True)#instruct to power motor one forward
                    GPIO.output(12,False)
                    GPIO.output(13,False)
                    GPIO.output(16,True) #instructs to power motor2 forward
                    print" up"     

                elif char == "down":
                    GPIO.output(12,True)
                    GPIO.output(13,True)
                    GPIO.output(7,False)
                    GPIO.output(16,False)
                    print "down"

                elif char == "right":
                    GPIO.output(12,False)
                    GPIO.output(13,False)
                    GPIO.output(7,True)
                    GPIO.output(16,False)
                    print "right"

                elif char == "left":
                    GPIO.output(12,False)
                    GPIO.output(13,False)
                    GPIO.output(16,True)
                    GPIO.output(7,False)
                    print "left"

                elif char == 10:
                    GPIO.output(7,False)
                    GPIO.output(12,False)
                    GPIO.output(13,False)
                    GPIO.output(16,False)

        finally:
            GPIO.cleanup()
            s.close()
if __name__ == '__main__':
   MstrCtrl()