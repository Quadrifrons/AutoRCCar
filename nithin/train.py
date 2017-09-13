__author__ = 'zhengwang'

import sys
import numpy as np
import cv2
import curses
import socket

pi_ip=sys.argv[1]
#pi_ip = "127.0.0.1"

class CollectTrainingData(object):

    def __init__(self):

        # Server to recieve data
        self.server_socket = socket.socket()
        self.server_socket.bind(("", 8001))
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server_socket.listen(1)
	print "Data server initialised and listening... "
        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')
        #----Client made------------"
        self.send_inst = True

        # Making server for bot control
        self.host=''
        self.port=5560
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        print("Control server initialised...")
        try:
            self.s.bind((self.host, self.port))
        except socket.error as msg:
            print(msg)
        print("Control Socket bind complete.")
        print "Listening..."
	self.s.listen(1)
        self.conn, self.address = self.s.accept()
        print("Connected to: " + self.address[0] + ":" + str(self.address[1]))
        #dir="up"
        #conn.sendall(str.encode(dir))
        #print("Data has been sent!")
        #conn.close()
        #----- Server made------"

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        #pygame.init()
        screen=curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
	print "Keyboard control initialised."
        self.collect_image()

    def collect_image(self):

     	print "Starting image collection..."
        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
		print "Receiving stream bytes..."
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
		    print "Decodong received image..."
                    # select lower half of the image
                    roi = image[120:240, :]

                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)

                    #cv2.imshow('roi_image', roi)
		    print "Showing image..."
                    cv2.imshow('image', image)

                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    #for event in pygame.event.get():
                     #   if event.type == KEYDOWN:
                      #      key_input = pygame.key.get_pressed()
                    while True:
                     	    char = screen.getch()
                            ''' # complex orders currently skipping
                            if char == curses.KEY_UP and char == curses.KEY_RIGHT:
                                print("Forward Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                #self.ser.write(chr(6))

                            elif char == curses.KEY_UP and char == curses.KEY_LEFT:
                                print("Forward Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                #self.ser.write(chr(7))

                            elif char == curses.KEY_DOWN and char == curses.KEY_RIGHT:
                                print("Reverse Right")
                                #self.ser.write(chr(8))

                            elif char == curses.KEY_DOWN and char == curses.KEY_LEFT:
                                print("Reverse Left")
                                #self.ser.write(chr(9))
                             '''
                            # simple orders
                            if char == curses.KEY_UP:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                #self.ser.write(chr(1))
                                self.conn.sendall(str.encode("up"))
				print "Data sent"

                            elif char == curses.KEY_DOWN:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                #self.ser.write(chr(2))
                                self.conn.sendall(str.encode("down"))

                            elif char == curses.KEY_RIGHT:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                #self.ser.write(chr(3))
                                self.conn.sendall(str.encode("right"))

                            elif char == curses.KEY_LEFT:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                #self.ser.write(chr(4))
                                self.conn.sendall(str.encode("left"))

                            elif char == ord('q'):
                                print 'exit'
                                self.send_inst = False
                                #self.ser.write(chr(0))
                                break

                        #elif event.type == pygame.KEYUP:
                            #self.ser.write(chr(0))
                         #   self.conn.sendall(str.encode("up"))

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            np.savez('training_data_temp/test08.npz', train=train, train_labels=train_labels)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print(train_labels.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame

        finally:
            self.connection.close()
            self.server_socket.close()
            self.conn.close()
            self.s.close()

if __name__ == '__main__':
   CollectTrainingData()
