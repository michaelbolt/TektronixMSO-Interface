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
    print("Connected by ",addr)
    #emulation loop
    while True:
        #wait for command or closed connection
        cmd = conn.recv(1024)
        if cmd == b'':
            break
        #split commands into list
        cmd_str = cmd.decode('ascii')
        cmd_list = cmd_str.split(';')
        #create list of responses to commands
        response_list = []
        for c in cmd_list:
            print(c)
            if '?' in c:
                response_list.append('4000')
        #create response string if any to send
        if response_list:
            response_str = ''
            for r in response_list:
                response_str += r + ';'
            #remove the final ';'
            response_str = response_str[:-1]
            #send response
            conn.send(bytes(response_str,'ascii'))
    #close connected socket once client closes
    conn.close()
    #prompt to keep going
    t = input("Continue? [Y/N]: ")
    if t[0] == 'N':
        keepGoing = False
#close server socket once finished
print("\nShutting down")
s.close()