#import os, sys
from pyGPIO2.gpio import gpio, port
from time import sleep

#Init GPIO lib
gpio.init()

class Stepper(object):

	def __init__(self,step_pin,dir_pin,enable_pin,sw_pin):
		self.step_pin=step_pin
		self.dir_pin=dir_pin
		self.enable_pin=enable_pin
		self.sw_pin=sw_pin
		self.setSpeed(0.0001)
		self.counter=0
		gpio.setcfg(self.step_pin, 1)
		gpio.setcfg(self.enable_pin,1)
		gpio.setcfg(self.dir_pin,1)
		gpio.setcfg(self.sw_pin,0)
		gpio.pullup(self.sw_pin,1)

	def setSpeed(self,speed):
		self.speed=speed
		return print("Speed value ", self.speed," has been selected")

	def positionCounter(self):
		if gpio.input(self.dir_pin)==0:
			self.counter += 1
		elif gpio.input(self.dir_pin)==1:
			self.counter -= 1
		return print(f"\rAbsPosition= {self.counter}",end="")

	def homing(self):
		self.enable()
		self.setDirection("CLOCKWISE")
		while gpio.input(self.sw_pin)==1:
			gpio.output(self.step_pin,1)
			sleep(0.0005)
			gpio.output(self.step_pin,0)
			sleep(0.0005)
		self.setDirection("COUNTER CLOCKWISE")
		self.move_relative(200)
		self.setDirection("CLOCKWISE")
		while gpio.input(self.sw_pin)==1:
			gpio.output(self.step_pin,1)
			sleep(0.001)
			gpio.output(self.step_pin,0)
			sleep(0.001)
		self.disable()
		self.counter=0

	def setDirection(self,state):
		if state=="CLOCKWISE":
			gpio.output(self.dir_pin,0)
		elif state=="COUNTER CLOCKWISE":
			gpio.output(self.dir_pin,1)

	def disable(self):
		gpio.output(self.enable_pin,1)

	def enable(self):
		gpio.output(self.enable_pin,0)

	def readPosition(self):
		return self.counter

	def readState(self):
		if gpio.input(self.enable_pin)==0:
			enableState="ENABLE"
		elif gpio.input(self.enable_pin)==1:
			enableState="DISABLE"
		if gpio.input(self.dir_pin)==0:
			dirState="CLOCKWISE"
		elif gpio.input(self.dir_pin)==1:
			dirState="COUNTER CLOCKWISE"
		return enableState,dirState

	def move_relative(self,step_nr):
		#calculate ramp
		if gpio.input(self.enable_pin)==1:
			return "Motor DISABLE"
		ramp_step_nr=int(step_nr*0.10)
		speed_step=(0.001-self.speed)/ramp_step_nr
		#ramp steps
		for i in range(ramp_step_nr):
			self.positionCounter()
			gpio.output(self.step_pin,1)
			sleep(abs(speed_step*i-0.001))
			gpio.output(self.step_pin,0)
			sleep(abs(speed_step*i-0.001))
		for i in range(step_nr-2*ramp_step_nr):
			self.positionCounter()
			gpio.output(self.step_pin,1)
			sleep(self.speed)
			gpio.output(self.step_pin,0)
			sleep(self.speed)
		for i in range(ramp_step_nr):
			self.positionCounter()
			gpio.output(self.step_pin,1)
			sleep(speed_step*i)
			gpio.output(self.step_pin,0)
			sleep(speed_step*i)
		print("\r")



