import socket

#use localhost Port 4000 for testing
HOST = 'localhost' 
PORT = 4000  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
s.listen(5)
print("Socket bound to %s : %d" % (HOST, PORT))
#accept new connections until the user says to stop
keepGoing = True
while keepGoing:
    #accept connection
    conn, addr = s.accept()
    print("\nConnected by ",addr)
    #emulate until client closes connection
    while True:
        data = conn.recv(1024)
        if data == b'':
            break
        data_str = data.decode('ascii')
        #if query received, echo query for testing
        if data_str.endswith('?'):
            conn.send(bytes('Received: "' + data_str + '"','ascii'))
    #close connected socket once client closes
    conn.close()
    #prompt to keep going
    t = input("Continue? [Y/N]: ")
    if t[0] == 'N':
        keepGoing = False
#close server socket once finished
print("\nShutting down")
s.close()