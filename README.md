# TektronixMSO-Interface
A simple GUI Interface for sending commands to Tektronix 5 and 6 series MSO Oscilloscopes. This was created for use in my research efforts, but can be used by anybody.

## Using the GUI
- To launch the GUI, run `MSO_Interface.py` from the command line. Type the instrument's IP Address and Port number before clicking `Connect`. If the connection is successful, you will see `Connected` appear; if you entered an incorrect or invalid IP Address and Port, you will see `Refused` appear.
- Commands can be sent to the instrument by typing in the `Command:` field and pressing `return` or `enter`. If your command is a query (ends in a _?_), the instrument's response will be displayed in the `Response:` field; otherwise, the phrase _Not Query Form_ will be displayed.
- User-defined command scripts can be run by typing the file name in the `SCript (.txt):`field or by using the file select dialog box and clicking the `Run` button. All commands and responses will be displayed in the log at the bottom of the GUI along with any comments contained in the user-defined script.

## User-Defined Scripts
A sample user-defined script is included in `SampleScript.txt`. USer-defined scripts support three types of lines: _commands_, _comments_, _pauses_, and _blank lines_.

### Commands
Commands are valid 5/6 Series MSO Oscilloscope commands found in the programmer's guide (linked at the bottom of this ReadMe). The user-defined script is case insensitive towards commands, as they are internally changed to upper case before being sent to the instrument.

### Comments
Comments are any any line in which the first non-whitespace chracter is the `#` symbol. These will be displayed in the GUI log window with syntactic coloring and serve to provide clarity for the user. _Do not place comments and commands on the same line._

### Pauses
A line that contains the string 'PAUSE' and is _not_ a comment will cause the script to pause at this point during runtime. The MSO Interface GUI will wait for you to press either `Continue` or `Stop` before performing either action.

### Blank Lines
Blank lines can contain any amount of whitespace and write an empty line to the GUI log window. These are intended to improve readability of script results in the log window.

## MSO5x/6x Emulator
A simple server script to emulate a 5/6 series MSO oscilloscope is included as `MSO_emulator.py`. If you run this script a socket will be established on `localhost` Port 4000 for testing purposes. The MSO emulator will receive commands from the GUI and respond with a dummy message of '4000' to each query received. The emulator supports concatenated commands 

## Valid Commands
Programming commands for the 5/6 Series MSO Oscilloscopes can be found [here](https://download.tek.com/manual/5_6-Series-MSO54-MSO56-MSO58-MSO58L-MSO64-Programmer-Manual_EN-US_077130505.pdf)
