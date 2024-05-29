import socket
import pickle
from random import randint

def encrypt_decrypt(message, key):
    return ''.join(chr(ord(char) ^ key) for char in message)

def send_message(conn, message, key):
    encrypted_message = encrypt_decrypt(message, key)
    conn.send(pickle.dumps(encrypted_message))

def receive_message(conn, key):
    encrypted_message = pickle.loads(conn.recv(1024))
    return encrypt_decrypt(encrypted_message, key)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

sock = socket.socket()
sock.bind((SERVER_HOST, SERVER_PORT))
sock.listen(1)
conn, addr = sock.accept()

prime, base, client_public = pickle.loads(conn.recv(1024))
server_secret = randint(10, 250)
server_public = pow(base, server_secret, prime)
conn.send(pickle.dumps(server_public))
shared_key = pow(client_public, server_secret, prime)

while True:
    try:
        message = receive_message(conn, shared_key)
        print(message)
        send_message(conn, 'сообщение получено', shared_key)
    except (EOFError, ConnectionResetError):
        break

conn.close()
