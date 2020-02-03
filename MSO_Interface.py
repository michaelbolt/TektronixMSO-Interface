from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import socket
import threading

class MSO_Interface : 
    def __init__(self):
        """MSO_Interface Constructor
        Creates root window for TK GUI
        """
        self.m_root = Tk()
        self.m_root.title("Tektronix MSO 5x/6x Interface")
        self.m_connected = False  
        self.m_scriptRunning = False  
        self.m_logLength = 20  
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
        ttk.Label(socketFrame, text='IP Address:', width=12, anchor=E).grid(row=0, column=0, sticky=E)
        ttk.Label(socketFrame, text='Port:', width=12, anchor=E).grid(row=1, column=0, sticky=E)
        self.m_ipEntry = Text(socketFrame, width=16, height=1)
        self.m_ipEntry.configure(font='helvetica')
        self.m_ipEntry.insert('1.0','localhost')
        self.m_ipEntry.grid(row=0, column=1, sticky=(E,W))
        self.m_portEntry = Text(socketFrame, width=16, height=1)
        self.m_portEntry.configure(font='helvetica')
        self.m_portEntry.insert('1.0', '4000') 
        self.m_portEntry.grid(row=1, column=1, sticky=(E,W))
        self.m_socketBtn = ttk.Button(socketFrame, text='Connect', command=self.socketConnectionHandler, width=14)
        self.m_socketBtn.grid(row=0, column=2, sticky=(W), padx=5)
        self.m_socketLabel = ttk.Label(socketFrame, text='No Connection', anchor=W, width=14)
        self.m_socketLabel.grid(row=1, column=2, sticky=(E,W), padx=5)
        socketFrame['padding'] = (10,10)
        socketFrame.grid(row=0, column=0, columnspan=3, sticky=(E,W))
        socketFrame.columnconfigure(0,weight=1)
        socketFrame.columnconfigure(2,weight=1)
        ttk.Separator(self.m_root, orient=HORIZONTAL).grid(row=1, column=0, sticky=(N,S,E,W))
        #Command line section
        midFrame = ttk.Frame(self.m_root)
        ttk.Label(midFrame, text='Command:', anchor=E).grid(row=0, column=0, sticky=(N,S,E,W))
        ttk.Label(midFrame, text='Response:', anchor=E).grid(row=1, column=0, sticky=(N,S,E,W))
        self.m_cmdEntry = Text(midFrame, width=40, height=1)
        self.m_cmdEntry.bind('<Return>',self.sendCmdHandler)
        self.m_cmdEntry.configure(font = 'helvetica')
        self.m_cmdEntry.grid(row=0, column=1, columnspan=3, sticky=(W,E), pady=2.5)
        self.m_cmdResponse = Text(midFrame, width=40, height=1)
        self.m_cmdResponse.configure(font = 'helvetica')
        self.m_cmdResponse.grid(row=1,column=1, columnspan=3, sticky=(W,E), pady=2.5)
        self.m_cmdResponse.tag_configure('defaultFont', font='helvetica')
        self.m_cmdResponse.tag_configure('errorFont', foreground='red', relief='raised')
        ttk.Separator(midFrame, orient=HORIZONTAL).grid(row=2, column=0, columnspan=5, sticky=(N,S,E,W), pady=7.5)
        #Load script section
        ttk.Label(midFrame, text='Script (.txt)', anchor=E).grid(row=3, column=0, sticky=(N,S,E,W))
        self.m_scriptFileEntry = Text(midFrame, width=40, height=1)
        self.m_scriptFileEntry.configure(font = 'helvetica')
        self.m_scriptFileEntry.grid(row=3, column=1, columnspan=3, sticky=(W,E), pady=2.5)
        self.m_scriptFileEntry.insert('1.0','SampleScript.txt')
        ttk.Button(midFrame, text='\u2026', width=1, command=self.loadScriptFile).grid(row=3,column=4,sticky=W)
        #Run script section
        ttk.Button(midFrame, text='Clear Log', width=8, command=self.clearLog).grid(row=4, column=1, sticky=(E,W), pady=2.5)
        self.m_continueBtn = ttk.Button(midFrame, text='Continue', width=8, command=self.continueBtn, state='disabled')
        self.m_continueBtn.grid(row=4, column=2, sticky=(E,W), pady=2.5)
        self.m_runStopBtn = ttk.Button(midFrame, text='Run', width=8, command=self.runStopBtn)
        self.m_runStopBtn.grid(row=4, column=3, sticky=(E,W), pady=2.5)
        midFrame.grid(row=2, column=0, sticky=(N,S,E,W))
        midFrame.columnconfigure(0, weight=1)
        midFrame.columnconfigure(4, weight=1)
        midFrame['padding'] = (10,7.5)
        ttk.Separator(self.m_root, orient=HORIZONTAL).grid(row=4, column=0, sticky=(N,S,E,W))
        #Communication log section
        logFrame = ttk.Frame(self.m_root)
        self.m_log = Text(logFrame, width=61, height=self.m_logLength)
        self.m_log.configure(font='helvetica')
        self.m_log.grid(row=0,column=0, sticky=(N,S,E,W))
        self.m_log.tag_configure('tx', foreground='gray')
        self.m_log.tag_configure('rx', foreground='#03244d')
        self.m_log.tag_configure('comment', foreground='#6aa16a')
        self.m_log.tag_configure('error', foreground='red')
        self.m_log.tag_configure('sysMsg', foreground = 'orange')
        logFrame['padding'] = (10, 10)
        logFrame.grid(row=5, column=0, sticky=(N,S,E,W))



    def socketConnectionHandler(self):
        """Handles socket connection at user specified IP address and Port.
        - Manages button and label state to display current connection status.
        - Displays "REFUSED" message if IP address and Port combo rejects connection.
        """
        #if no active connection, establish one
        if not self.m_connected:
            self.m_IP = self.m_ipEntry.get('1.0','end').strip()
            self.m_PORT = int(self.m_portEntry.get('1.0','end').strip())
            try:
                self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.m_socket.connect((self.m_IP, self.m_PORT))
                self.m_socketBtn['text'] = 'Disconnect'
                self.m_socketLabel['text'] = 'Connected'
                self.m_connected = True
                self.updateLog('*** Connected to ' + str(self.m_IP) + ' Port ' + str(self.m_PORT) + ' ***', 'sysMsg')
            #print error for user if IP address and PORT rejected the connection
            except socket.error:
                self.m_socketLabel['text'] = 'REFUSED'
                self.updateLog('*** Connection refused by ' + str(self.m_IP) + ' Port ' + str(self.m_PORT) + ' ***', 'error')
        #if an active connection exists, close it
        else:
            self.m_socket.close()
            self.m_socketBtn['text'] = 'Connect'
            self.m_socketLabel['text'] = 'No Connection'
            self.m_connected = False
            self.updateLog('*** Connection to ' + str(self.m_IP) + ' Port ' + str(self.m_PORT) + ' closed ***', 'sysMsg')

    def sendCmdHandler(self, event):
        """Handles <Return> key when typing in Command Entry box.
        - User input command is sent through active socket connection.
        - The result of the command is displayed in the Response Text box;
          if the command was not a query, a message stating so is displayed
        """
        CMD = self.m_cmdEntry.get('1.0','end').strip()
        response = self.sendCmd(CMD)
        if response:
            #clear previous message
            self.m_cmdResponse.delete('1.0','end')        
            #write all responses
            for resp in response:
                self.m_cmdResponse.insert('end',(resp+'    '),'defaultFont')
        #return 'break' so the '\n' is not added to the text
        return 'break'

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
            self.m_socket.send(bytes(cmd,'ascii'))
            response = ['No Query Sent']
            #if command contained a query, receive response
            if '?' in cmd:
                data = self.m_socket.recv(1024)
                data = data.decode('ascii')
                response = data.split(';')
                self.updateLog(data,'rx')
            return response
        except:
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
        # numlines = int(self.m_log.index('end - 1 line').split('.')[0])
        #delete first line if log window is full
        # print(numlines)
        # if numlines==self.m_logLength:
            # self.m_log.delete('1.0', '2.0')
        #ensure all entries start on a new line
        if self.m_log.index('end-1c')!='1.0':
            self.m_log.insert('end', '\n')
        #insert new message
        self.m_log.insert('end', msg, msgType)
        #make sure bottom of log is shown
        self.m_log.see('end')

    def clearLog(self):
        """Clears all text from console log at the bottom of the GUI
        """
        self.m_log.delete('1.0','end')

    def loadScriptFile(self):
        """Opens system file select dialog to select a script file
        """
        self.m_scriptFileEntry.delete('1.0','end')
        self.m_scriptFileEntry.insert('1.0', filedialog.askopenfilename())

    def runStopBtn(self):
        """Toggles state between running/not running a user-defined script.
        - If no script is currently running, a thread is started to run the script
        and output any commands/responses/comments to the console.
        - If a script is currently running, flags are set so that the thread
        executing the script will finish up and be destroyed.
        """
        #if we are not running a script, start
        if not self.m_scriptRunning:
            #acquire a thread lock to implement pause
            self.m_pauseLock = threading.Lock()
            self.m_pauseLock.acquire()
            self.m_scriptThread = threading.Thread(target=self.scriptThread, daemon=True)
            self.m_scriptThread.start()
        #if we are running a script, unpause and stop
        else:
            self.m_pauseLock.release()
            self.m_scriptRunning = False

    def continueBtn(self):
        """Sets the current paused state to False.
        Can only be called when the script is paused.
        """
        self.m_pauseLock.release()

    def scriptThread(self):
        """Thread to read in user-defined script and execute it accordingly.
        """
        try:
            #open the file
            self.m_scriptFile = open(self.m_scriptFileEntry.get('1.0','end').strip(), 'r')
            self.m_scriptRunning = True
            self.m_runStopBtn['text'] = 'Stop'
            #iterate through file
            for line in self.m_scriptFile:
                #if we quit during the last iteration, leave now
                if not self.m_scriptRunning:
                    break
                #clean up command
                cmd = line.strip()
                #if line was not blank...
                if cmd:
                    #comment operation
                    if cmd[0] == '#':
                        self.updateLog(cmd, 'comment')
                    #pause operation:
                    elif 'PAUSE' in cmd.upper():
                        #enable pause button
                        self.m_continueBtn['state'] = 'normal'
                        self.updateLog('*** PAUSED ***', 'sysMsg')
                        #wait for Continue/Stop button to release the pauseLock
                        self.m_pauseLock.acquire()
                        #disable the pause button
                        self.m_continueBtn['state'] = 'disabled'
                    #command to be sent
                    else:
                        self.sendCmd(cmd.upper())
                #if line was blank:
                else:
                    self.updateLog('  ', 'comment') 
            #once we have quit or finished the file
            self.updateLog('*** END ***', 'sysMsg')
            self.m_scriptFile.close()
            self.m_scriptRunning = False
            self.m_runStopBtn['text'] = 'Run'
        #catch file IO error
        except:
            self.updateLog('*** FILE NOT FOUND ***', 'error')



        

def main():
    App = MSO_Interface()
    App.startApplication()

if __name__ == "__main__":
    main()





