import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

while True:
    client, addr = server.accept()
    client.send("Hello, world!".encode("utf-8"))
    print(client.recv(1024).decode('utf-8'))
    client.close()
