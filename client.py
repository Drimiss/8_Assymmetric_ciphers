import socket
import pickle
from random import randint

def encrypt_decrypt(message, key):
    return ''.join(chr(ord(char) ^ key) for char in message)

def send_message(sock, message, key):
    encrypted_message = encrypt_decrypt(message, key)
    sock.send(pickle.dumps(encrypted_message))

def receive_message(sock, key):
    encrypted_message = pickle.loads(sock.recv(1024))
    return encrypt_decrypt(encrypted_message, key)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

sock = socket.socket()
sock.connect((SERVER_HOST, SERVER_PORT))
print('Соединение установлено!')
print('Введите "exit" для закрытия соединения')

prime, base, client_secret = [randint(0, 250) for _ in range(3)]
client_public = pow(base, client_secret, prime)
sock.send(pickle.dumps((prime, base, client_public)))
server_public = pickle.loads(sock.recv(1024))
shared_key = pow(server_public, client_secret, prime)

while True:
    message = input('Введите сообщение: ')
    if message == 'exit':
        break
    send_message(sock, message, shared_key)
    response = receive_message(sock, shared_key)
    print(response)

sock.close()
