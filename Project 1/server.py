import socket
host = ''
port = 5535
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((host, port))
ss.listen(1)
conn, address = ss.accept()


for i in range(20):
    # receive the string from the client and decode it
    x = conn.recv(512)
    x = x.decode('utf-8')
    # reverse the string, encode it and send it back to client
    x = x [::-1]
    conn.sendall(x.encode('utf-8'))

conn.close()
