import socket

HOST = '192.168.1.14'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")
    while True:
        msg = input("> ")
        if msg == "quit":
            break
        s.sendall(msg.encode())
        print("Received:", s.recv(1024).decode())
