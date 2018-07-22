from Adafruit_MotorHAT import *

from illustrator import CartesianIllustrator
from illustrator.Illustrator import *
import threading

hat = Adafruit_MotorHAT()
illustrator = CartesianIllustrator(hat, 30, 30, (0, 0), (50,50))
illustrator.start()

orig = exit
def exit():
	print '\n[+] Motors off...'
	illustrator._turnOff()
	orig()

try:
	while True:
		x = -1
		y = -1
		try:
			x = raw_input('x ----> ')
			if x == 'exit':
				exit()	
			x = int(x)
			y = int(raw_input('y ----> '))
		except ValueError:
			print "\n\n\n"
			continue
		
		if x == -1 or y == -1:
			continue

		illustrator.go(x, y)
except KeyboardInterrupt:
	exit()	
