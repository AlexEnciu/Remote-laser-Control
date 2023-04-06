import socket

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
	print(command)
    # Perform some operation on the received command
	response = command.upper()

    # Send the response back to the client
	client_socket.sendall(response.encode())

    # Close the connection with the client
	client_socket.close()
