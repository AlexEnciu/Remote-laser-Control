import os, sys
from laserlib import Stepper
from pyGPIO2.gpio import gpio, port
from time import sleep
import socket

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

#Define motors
motor0=Stepper(step_pin,dir_pin,enable_pin,sw_pin)
motor1=Stepper(step_pin_1,dir_pin_1,enable_pin_1,sw_pin_1)



def control_stepper(command):
	parts = command.split() #split command in 3 [command->target->value]
	print("PARTS: ",parts)
	function=parts[0] # function which you want to call
	target=parts[1] # the motor where you want to apply the function
	if function =='Move': # move the motor with a relative number of steps
		steps=int(parts[2])
		if target == '0':
			motor0.enable()
			msg=motor0.move_relative(steps)
			motor0.disable()
			return msg
		elif target == '1':
			motor1.enable()
			msg=motor1.move_relative(steps)
			motor1.disable()
			return msg
	elif function =='Homing':
		if target =='0':
			motor0.homing()
			return "ok"
		elif target =='1':
			motor1.homing()
			return "ok"
	elif function =='Enable':
		if target =='0':
			motor0.enable()
			return "ok"
		elif target =='1':
			motor1.enable()
			return "ok"
	elif function =='Disable':
		if target =='0':
			motor0.disable()
			return "ok"
		elif target =='1':
			motor1.disable()
			return "ok"
	elif function =='Direction':
		dir_value=parts[2]
		if target =='0':
			if dir_value =='CW':
				motor0.setDirection("CLOCKWISE")
				return "ok"
			elif dir_value == 'CCW':
				motor0.setDirection("COUNTER CLOCKWISE")
				return "ok"
		elif target =='1':
			if dir_value == 'CW':
				motor1.setDirection("CLOCKWISE")
				return "ok"
			elif dir_value == 'CCW':
				motor1.setDirection("COUNTER CLOCKWISE")
				return "ok"
	elif function =='ReadState':
		if target =='0':
			return motor0.readState()
		elif target =='1':
			return motor1.readState()
	elif function =='ReadAbs':
		if target =='0':
			return motor0.readCounter()
		elif target =='1':
			return motor1.readCounter()
	elif function =='SetSpeed':
		speed=float(parts[2])
		if target == '0':
			motor0.setSpeed(speed)
			return "ok"
		elif target == '1':
			motor1.move_relative(speed)
			return "ok"
	if function =='MoveToAbs': # move the motor with a relative number of steps
		steps=int(parts[2])
		if target == '0':
			motor0.enable()
			msg=motor0.move_toAbs(steps)
			motor0.disable()
			return msg
		elif target == '1':
			motor1.enable()
			msg=motor1.move_toAbs(steps)
			motor1.disable()
			return msg


# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #release the port after intrerrupt
# Bind the socket to a specific IP address and port number
server_address = ('192.168.15.43', 10000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print('Server is listening for incoming connections...')
while True:
    # Wait for a client to connect
	client_socket, client_address = server_socket.accept()
	print('Received connection from', client_address)
    # Receive the command from the client
	command = client_socket.recv(1024).decode()
	#client_socket.sendall("command recived".encode())
	print(command)
	answear=control_stepper(command)
    # Perform some operation on the received command
	#response = command.upper()
    # Send the response back to the client
	if answear is None:
		client_socket.sendall("Wrong Command!".encode())
	elif answear is not None:
		client_socket.sendall(answear.encode())
    # Close the connection with the client
	client_socket.close()

