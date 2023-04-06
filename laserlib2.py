import os, sys

#if not os.getegid() == 0:
	#sys.exit('start script as root')
from pyGPIO2.gpio import gpio, port
from time import sleep

#Init GPIO lib
gpio.init()

#Define pins Motor 0
step_pin=port.GPIO4 
dir_pin=port.GPIO18
enable_pin=port.GPIO17
sw_pin=port.GPIO27

#Define pins Motor 1
step_pin_1=port.GPIO22
dir_pin_1=port.GPIO23
enable_pin_1=port.GPIO24
sw_pin_1=port.GPIO25

#Define Variable

class Stepper(object):
	# initialisation
	#speed=0.0001
	#step_nr=2000
	def __init__(self,step_pin,dir_pin,enable_pin,sw_pin):
		self.step_pin=step_pin
		self.dir_pin=dir_pin
		self.enable_pin=enable_pin
		self.sw_pin=sw_pin
		self.setSpeed(0.001)
		gpio.setcfg(self.step_pin, 1)
		gpio.setcfg(self.enable_pin,1)
		gpio.setcfg(self.dir_pin,1)
		gpio.setcfg(self.sw_pin,0)
		gpio.pullup(self.sw_pin,1)

	def setSpeed(self,speed):
		self.speed=speed
		return print("Speed value ", self.speed," has been selected")

	def homing(self):
		self.setState("ENABLE")
		self.setDirection("CLOCKWISE")
		while gpio.input(self.sw_pin)==1:
			gpio.output(self.step_pin,1)
			sleep(0.0001)
			gpio.output(self.step_pin,0)
			sleep(0.0001)
		self.setDirection("COUNTER CLOCKWISE")
		self.move_relativ(500)
		self.setDirection("CLOCKWISE")
		while gpio.input(self.sw_pin)==1:
			gpio.output(self.step_pin,1)
			sleep(0.001)
			gpio.output(self.step_pin,0)
			sleep(0.001)
		self.setState("DISABLE")


	def setDirection(self,state):
		if state=="CLOCKWISE":
			gpio.output(self.dir_pin,0)
		elif state=="COUNTER CLOCKWISE":
			gpio.output(self.dir_pin,1)
		print("Motor ", state, gpio.input(self.dir_pin))


	def setState(self,state):
		if state=="ENABLE":
			gpio.output(self.enable_pin,0)
		elif state=="DISABLE":
			gpio.output(self.enable_pin,1)
		print("Motor ", state, gpio.input(self.enable_pin))

	def move_relativ(self,step_nr):
		for i in range(step_nr):
			gpio.output(self.step_pin,1)
			sleep(self.speed)
			gpio.output(self.step_pin,0)
			sleep(self.speed)

motor1=Stepper(step_pin_1,dir_pin_1,enable_pin_1,sw_pin_1)
motor0=Stepper(step_pin,dir_pin,enable_pin,sw_pin)


#sys.exit('Laser Close!')
