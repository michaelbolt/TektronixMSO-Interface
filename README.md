# TektronixMSO-Interface
A simple GUI Interface for sending commands to Tektronix 5 and 6 series MSO Oscilloscopes. This was created for use in my research efforts, but can be used by anybody.

## Using the GUI
1. To launch the GUI, run `MSO_Interface.py` from the command line. 
2. Type the instrument's IP Address and Port number before clicking `Connect`. If the connection is successful, you will see `Connected` appear; if you entered an incorrect or invalid IP Address and Port, you will see `Refused` appear.
3. Commands can be sent to the instrument by typing in the `Command` field and pressing `return` or `enter`. If your command is a query (ends in a _?_), the instrument's response will be displayed in the `Response` field; otherwise, the phrase _Not Query Form_ will be displayed.
4. Scope Setup files (_.set_) can be loaded by typing the _.set_ file's location and name into the text entry box and pressing `Load`. An example of loading a setup file from a removable USB storage device drive `E:/` is present by default.

## MSO5x/6x Emulator
A simple server script to emulate a 5/6 series MSO oscilloscope is included as `MSO_emulator.py`. If you run this script a socket will be established on `localhost` Port 4000 for testing purposes. The MSO emulator will receive commands from the GUI and echo received queries to assist in debugging. 

## Valid Commands
Programming commands for the 5/6 Series MSO Oscilloscopes can be found [here](https://download.tek.com/manual/5_6-Series-MSO54-MSO56-MSO58-MSO58L-MSO64-Programmer-Manual_EN-US_077130505.pdf)
