from tkinter import *
from tkinter import ttk
import socket

class MSO_Interface : 
    def __init__(self):
        """MSO_Interface Constructor
        Creates root window for TK GUI
        """
        self.m_root = Tk()
        self.m_root.title("Tektronix MSO 5x/6x Interface")
        self.m_ip = StringVar()
        self.m_port = StringVar()
        self.m_connected = False
        self.m_cmd = StringVar()        
        self.m_setupFile = StringVar()
        self.placeWidgets()

    def startApplication(self):
        """Begins application main loop
        """
        self.m_root.mainloop()

    def placeWidgets(self):
        """Place TK widgets to construct the GUI
        """
        #Socket connection section
        socketFrame = ttk.Frame(self.m_root)
        ttk.Label(socketFrame, text='IP Address:', width=8, anchor=E).grid(row=0, column=0, sticky=E)
        ttk.Label(socketFrame, text='Port:', width=8, anchor=E).grid(row=1, column=0, sticky=E)
        self.m_ip.set('localhost')
        self.m_port.set('4000')
        ttk.Entry(socketFrame, textvariable=self.m_ip, width=12).grid(row=0, column=1, sticky=(E,W))
        ttk.Entry(socketFrame, textvariable=self.m_port, width=12).grid(row=1, column=1, sticky=(E,W))
        self.m_socketBtn = ttk.Button(socketFrame, text='Connect', command=self.socketConnectionHandler, width=8)
        self.m_socketBtn.grid(row=0, column=2, sticky=(W))
        self.m_socketLabel = ttk.Label(socketFrame, text='No Connection', anchor=W)
        self.m_socketLabel.grid(row=1, column=2, sticky=(E,W))
        socketFrame['padding'] = (10,10)
        socketFrame.grid(row=0, column=0, sticky=(E,W))
        socketFrame.columnconfigure(0,weight=1)
        socketFrame.columnconfigure(2,weight=1)
        #Command line section
        cmdFrame = ttk.Frame(self.m_root)
        ttk.Label(cmdFrame, text='Command').grid(row=0, column=0, sticky=E)
        ttk.Label(cmdFrame, text='Response').grid(row=1, column=0, sticky=(N,E))
        self.m_cmd.set("COMMAND")
        cmdEntry = ttk.Entry(cmdFrame, textvariable=self.m_cmd, width=40)
        cmdEntry.bind('<Return>',self.sendCmdHandler)
        cmdEntry.grid(row=0, column=1, sticky=(E,W))
        self.cmdResponse = Text(cmdFrame, width=40, height=2)
        self.cmdResponse.grid(row=1,column=1, sticky=(N,S,E,W))
        self.cmdResponse.tag_configure('defaultFont', font='calibri 14')
        self.cmdResponse.tag_configure('errorFont', foreground='red', font='helvetica 20 bold', relief='raised')
        cmdFrame['padding'] = (10,10)
        cmdFrame.grid(row=2, column=0, sticky=(N,S,E,W))
        #Load oscilloscope setup section
        setupFrame = ttk.Frame(self.m_root)
        ttk.Label(setupFrame, text='Load Setup (.set)').grid(row=0, column=0, sticky=(E))
        self.m_setupFile.set("E:/AnechoicTests/TxCal.set")
        ttk.Entry(setupFrame, textvariable=self.m_setupFile).grid(row=0, column=1, sticky=(E,W))
        ttk.Button(setupFrame, text='Load', command=self.loadSetupFile).grid(row=0, column=2, sticky=(W))
        setupFrame.grid(row=4, column=0, sticky=(N,S,E,W))
        setupFrame.columnconfigure(1,weight=1)
        #Communication log section
        logFrame = ttk.Frame(self.m_root)
        self.log = Text(logFrame, state='disabled', width=61, height=12)
        self.log.grid(row=0,column=0, sticky=(N,S,E,W))
        self.log.tag_configure('tx', font='calibri 12', foreground='gray')
        self.log.tag_configure('rx', font='calibri 12', foreground='#03244d')
        self.log.tag_configure('error', font='calibri 12', foreground='red')
        logFrame['padding'] = (10,10)
        logFrame.grid(row=6, column=0, sticky=(N,S,E,W))
        #place separators
        ttk.Separator(self.m_root, orient=HORIZONTAL).grid(row=1, column=0, sticky=(N,S,E,W))
        ttk.Separator(self.m_root, orient=HORIZONTAL).grid(row=3, column=0, sticky=(N,S,E,W))
        ttk.Separator(self.m_root, orient=HORIZONTAL).grid(row=5, column=0, sticky=(N,S,E,W))



    def socketConnectionHandler(self):
        """Handles socket connection at user specified IP address and Port.
        - Manages button and label state to display current connection status.
        - Displays "REFUSED" message if IP address and Port combo rejects connection.
        """
        #if no active connection, establish one
        if not self.m_connected:
            HOST = self.m_ip.get()
            PORT = int(self.m_port.get())
            try:
                self.m_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.m_s.connect((HOST, PORT))
                self.m_socketBtn['text'] = 'Disconnect'
                self.m_socketLabel['text'] = 'Connected'
                self.m_connected = True
            #print error for user if IP address and PORT rejected the connection
            except socket.error:
                self.m_socketLabel['text'] = 'REFUSED'
        #if an active connection exists, close it
        else:
            self.m_s.close()
            self.m_socketBtn['text'] = 'Connect'
            self.m_socketLabel['text'] = 'No Connection'
            self.m_connected = False

    def sendCmdHandler(self, event):
        """Handles <Return> key when typing in Command Entry box.
        - User input command is sent through active socket connection.
        - The result of the command is displayed in the Response Text box;
          if the command was not a query, a message stating so is displayed
        """
        CMD = self.m_cmd.get()
        response = self.sendCmd(CMD)
        if response:
            #clear previous message
            self.cmdResponse.delete('1.0','end')        
            #write all responses
            for resp in response:
                self.cmdResponse.insert('end',(resp+'    '),'defaultFont')

    def sendCmd(self, cmd):
        """Sends command through the active socket connection; if no socket
        connection is active, an appropriate warning is displayed to the user
        and 0 is returned. The return value should be checked by the user
        input:
            - cmd (string): command to send
        return:
            - response (list) : list object containing all responses to queries
                                as separate entries; query responses are separated
                                by a ';' by the oscilloscope. If no query was sent,
                                the list will contain 'No Queries Sent'.
            - 0 :   returned if no active socket connection is available to
                    write to
        """
        self.updateLog(cmd, 'tx')
        try:
            self.m_s.send(bytes(cmd,'ascii'))
            response = ['No Query Sent']
            #if command contained a query, receive response
            if '?' in cmd:
                data = self.m_s.recv(1024)
                data = data.decode('ascii')
                response = data.split(';')
                self.updateLog(data,'rx')
            return response
        except:
            self.cmdResponse.delete('1.0','end')
            self.cmdResponse.insert('1.0','*** NO PORT CONNECTED ***', 'errorFont')
            self.updateLog('*** NO PORT CONNECTED ***','error')
            return 0

    def updateLog(self, msg, msgType='tx'):
        """Updates the console log at the bottom of the GUI
        intpu:
            - msg (string) : line of text to write to the console log
            - msgType (string) : tag to describe message for contextual 
                                 coloring ('tx','rx','error')
        """
        #determine number of lines in log window
        numlines = int(self.log.index('end - 1 line').split('.')[0])
        self.log['state'] = 'normal'
        #delete first line if log window is full
        if numlines==11:
            print('here!')
            self.log.delete('1.0', '2.0')
        #ensure all entries start on a new line
        if self.log.index('end-1c')!='1.0':
            self.log.insert('end', '\n')
        #insert new message
        self.log.insert('end', msg, msgType)
        self.log['state'] = 'disabled'


    def loadSetupFile(self):
        """Sends MSO64 command to load the user specified .set file
        """
        CMD = 'RECALL:SETUP "' + self.m_setupFile.get() + '"'
        self.sendCmd(CMD)




        

def main():
    App = MSO_Interface()
    App.startApplication()

if __name__ == "__main__":
    main()





