
# creates small socket server in order to test network
# connections

import socket

HOST = 'cc02wbstappprd02'
PORT = 5001


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print "connected by", addr

# while loop allows connection to stay enabled and not close
# immediately after client connection. comment out while loop
# for connect and immediate disconnect.

while 1:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data)

conn.close()
