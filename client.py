import socket
import threading

nickname = input('choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('public ip here', 55555))

def receive():
	while True:
		try:
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
				next_message = client.recv(1024).decode('ascii')
			else:
				print(message)
		except:
			print('an error occured!')
			client.close()
			break

def write():
	while True:
		message = f'{nickname}: {input("")}'
		msg = message[len(nickname) +2:]
		client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
