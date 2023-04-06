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

motor0=Stepper(step_pin,dir_pin,enable_pin,sw_pin)
motor1=Stepper(step_pin_1,dir_pin_1,enable_pin_1,sw_pin_1)

def control_stepper(command):
	if command == 'Homing M1':
        # Code to move the stepper motors to the left
		motor1.homing()
	elif command == 'Homing M0':
        # Code to move the stepper motors to the right
		motor0.homing()
	elif command == 'stop':
        # Code to stop the stepper motors
		pass

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	client_socket.sendall("command recived".encode())
	print(command)
	control_stepper(command)
    # Perform some operation on the received command
	response = command.upper()
    # Send the response back to the client
	client_socket.sendall(response.encode())
    # Close the connection with the client
	client_socket.close()

