import threading
import socket
import os
import binascii, datetime
from time import sleep

host = '0.0.0.0'
port = 55555

sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sever.bind((host, port))
except:
	sever.close()
	os.system('clear; python3 server.py')
	print(f'retrying bind to {host}:{port}')
	sleep(1)
	exit()
sever.listen()

clients = []
nicknames = []

def fulltime():
	#to get current time
	tim = datetime.datetime.now().date()
	tim = str(tim)
	tim = tim.replace('-', '/')
	tim = tim + ' '
	time = datetime.datetime.now().time()
	time = str(time)
	time = time[:8]
	fulltime = tim + time
	return fulltime

def broadcast(message):
	if message != '':
		print(fulltime() + '  ' + message.decode('ascii'))
		for clint in clients:
			clint.send(message)

def handle(clint):
	while True:
		try:
			message = clint.recv(1024)
			broadcast(message)
		except:
			index = clients.index(clint)
			clients.remove(clint)
			clint.close()
			nickname = nicknames[index]
			broadcast(f'{nickname} left the chat'.encode('ascii'))
			nicknames.remove(nickname)
			break
def receive():
	while True:
		clint, address = sever.accept()
		print(f'Connected with {str(address)}')
		
		clint.send('NICK'.encode('ascii'))
		
		nickname = clint.recv(1024).decode('ascii')
		
		nicknames.append(nickname)
		clients.append(clint)
		
		print(f'Nickname of the clint is {nickname}')
		broadcast(f'{nickname} joined the chat'.encode('ascii'))
		clint.send('Connected to the sever'.encode('ascii'))
		
		thread = threading.Thread(target=handle, args=(clint,))
		thread.start()

print('sever is listening')
receive()
