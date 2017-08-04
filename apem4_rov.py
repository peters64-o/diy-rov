#!/usr/bin/env python
"""
Code to translate joystick data via a Phidget to drive pulse motors in a ROV exhbition
Not that DRY code :-)
"""
# from ctypes import *
#import sys
from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
import serial
from time import sleep
def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case    
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )
 
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )


try:
	interfaceKit = InterfaceKit()
except RuntimeError as e:
	print("Runtime Error: %s" % e.message)
try:
	ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
except:
	try:
		ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
	except:
		print "not connected"
try:
#Your program Code here
	interfaceKit.openPhidget()
	interfaceKit.waitForAttach(10000)
	print ("%d attached!" % (interfaceKit.getSerialNum()))
	xold = 0
	yold = 0
	zold = 0
	pold = 0
	cmd="\x82"
	ser.write(cmd) 
	while True:
		x1 = interfaceKit.getSensorValue(0)
		y1 = interfaceKit.getSensorValue(1)
		z1 = interfaceKit.getSensorValue(2)
		p1 = interfaceKit.getSensorValue(3)
		sleep(0.2)
		x3 = interfaceKit.getSensorValue(0)
        	y3 = interfaceKit.getSensorValue(1)
        	z3 = interfaceKit.getSensorValue(2)
        	p3 = interfaceKit.getSensorValue(3)
		if ( -20 < (int(x3) - int(x1)) < 20 and 450 < z1 < 550 ):
	        	print (x1, y1, p1, z1)
			x2=int(round((int(x1)-500)/7,0))
			if ( -10 < x2 < 10 and x2 != xold ):
				cmd1 = "\xaa\x04\x06"
				cmd2 = "\xaa\x04\x07"
				ser.write(cmd1)			
				sleep(0.1)
				ser.write(cmd2)
				xold = x2
			else:
				if ( 10 < x2 < 99 ):
					cmd1 = HexToByte("aa0409" + str(x2))
					cmd2 = HexToByte("aa040d" + str(x2))
					ser.write(cmd1)
       		                 	sleep(0.1)
               		         	ser.write(cmd2)
                       		 	xold = x2
				else:
					if ( -99 < x2 < -10 ):
						x2=abs(x2)
						cmd1 = HexToByte("aa040a" + str(x2))
						cmd2 = HexToByte("aa040e" + str(x2))
						ser.write(cmd1)
                               		 	sleep(0.1)
	                               		ser.write(cmd2)
                                		xold = x2

		if ( -20 < (int(y3) - int(y1)) < 20 and 450 < z1 < 550 ):
			y2=int(round((int(y1)-500)/7,0))
			if ( -10 < y2 < 10 and y2 != yold ):
				cmd1 = "\xaa\x02\x06"
				cmd2 = "\xaa\x02\x07"
				ser.write(cmd1)			
				sleep(0.1)
				ser.write(cmd2)
				yold = y2
			else:
				if ( 10 < y2 < 99 ):
					cmd1 = HexToByte("aa0209" + str(y2))
					cmd2 = HexToByte("aa020e" + str(y2))
					ser.write(cmd1)
       		                 	sleep(0.1)
               		         	ser.write(cmd2)
                       		 	yold = y2
				else:
					if ( -99 < y2 < -10 ):
						y2=abs(y2)
						cmd1 = HexToByte("aa020a" + str(y2))
						cmd2 = HexToByte("aa020d" + str(y2))
						ser.write(cmd1)
                               		 	sleep(0.1)
                                		ser.write(cmd2)
                                		yold = y2

		if ( -20 < (int(z3) - int(z1)) < 20 ):
			z2=int(round((int(z1)-500)/7,0))
			if ( -10 < z2 < 10 and z2 != zold ):
				cmd1 = "\xaa\x02\x06"
				cmd2 = "\xaa\x02\x07"
				ser.write(cmd1)			
				sleep(0.1)
				ser.write(cmd2)
				zold = z2
			else:
				if ( 10 < z2 < 99 ):
					cmd1 = HexToByte("aa0209" + str(z2))
					cmd2 = HexToByte("aa020d" + str(z2))
					ser.write(cmd1)
       		                 	sleep(0.1)
               		         	ser.write(cmd2)
                       		 	zold = z2
				else:
					if ( -99 < z2 < -10 ):
						z2=abs(z2)
						cmd1 = HexToByte("aa020a" + str(z2))
						cmd2 = HexToByte("aa020e" + str(z2))
						ser.write(cmd1)
                               		 	sleep(0.1)
                                		ser.write(cmd2)
                                		zold = z2
                if ( -20 < (int(p3) - int(p1)) < 20 ):
                        p2=int(round((int(p1)-495)/6,0))
                        if ( -25 < p2 < 25 and p2 != pold ):
                                cmd1 = "\xaa\x08\x06"
                                cmd2 = "\xaa\x08\x07"
                                ser.write(cmd1)
                                sleep(0.1)
                                ser.write(cmd2)
                                pold = p2
                        else:
                                if ( 10 < p2 < 99 ):
#                                        cmd1 = HexToByte("aa080c" + str(p2))
                                        cmd2 = HexToByte("aa080d" + str(p2))
                                        ser.write(cmd1)
                                        sleep(0.1)
                                        ser.write(cmd2)
                                        pold = p2
                                else:
                                        if ( -99 < p2 < -10 ):
                                                pold = p2
                                                p2=abs(p2)
#                                                cmd1 = HexToByte("aa0809" + str(p2))
                                                cmd2 = HexToByte("aa080e" + str(p2))
                                                ser.write(cmd1)
                                                sleep(0.1)
                                                ser.write(cmd2)
except PhidgetException as e:
	print ("Phidget Exception %i: %s" % (e.code, e.details))
	exit(1)

def interfaceKitSensorChanged(e):
		print ("Sensor %i: %i" % (e.index, e.value))
		return 0
#interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
#sleep(3)
interfaceKit.closePhidget()
ser.close(t
)
