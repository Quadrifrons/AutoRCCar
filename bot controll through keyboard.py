# import curses and GPIO
import curses
import RPi.GPIO as GPIO
#GPIO is used for raspberry pi pin control

#set GPIO numbering mode and define output pins
# Two pin numbering modes are possible
# BOARD numbering mode
# -->   This refers to the pin numbers on the P1 header of the Raspberry 
#	Pi board. The advantage of using this numbering system is that your
#	hardware will always work, regardless of the board revision of the RPi. 
#	You will not need to rewire your connector or change your code.
# BCM numbering mode
# -->    This is a lower level way of working - it refers to the channel numbers 
#	 on the Broadcom SOC. You have to always work with a diagram of which channel
#	 number goes to which pin on the RPi board. Your script could break between 
#	 revisions of Raspberry Pi boards. 
GPIO.setmode(GPIO.BOARD) # This is a mandatory step
GPIO.setup(7,GPIO.OUT) # To setup channels to communicate with Pi
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)
GPIO.output(7,False)
GPIO.output(12,False)
GPIO.output(13,False)
GPIO.output(16,False)
try:
        while True:   
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                GPIO.output(7,True)
                GPIO.output(12,False)
                GPIO.output(13,False)
                GPIO.output(16,True)           
                
                print" up"
            elif char == curses.KEY_DOWN:
                GPIO.output(12,True)
                GPIO.output(13,True)
                GPIO.output(7,False)
                GPIO.output(16,False)
                print "down"
            elif char == curses.KEY_RIGHT:
                GPIO.output(12,False)
                GPIO.output(13,False)
                GPIO.output(7,True)     
                GPIO.output(16,False)
                print "right"
            elif char == curses.KEY_LEFT:
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
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
