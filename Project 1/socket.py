import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('ilab1.cs.rutgers.edu', 5535))
sock.send(b'test')
