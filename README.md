# bounce-cli-iosxe
This is a naive and simple implementation of a port bounce CLI in IOS-XE. It gives operators a method to bounce a port in a single command. This could be useful when bouncing a port could cut off access to the network device or a command authorization server.
## Two Options
1. Tcl script
2. Guestshell with a Python script

## TCL Script Usage
```
csr1000v-1#bounce Loopback4 10
Interface Loopback4 will be bounced with a 10 delay. Are you sure? (y/n)
y
csr1000v-1#sh log last 10
Syslog logging: enabled (0 messages dropped, 3 messages rate-limited, 0 flushes, 0 overruns, xml disabled, filtering disabled)

Showing last 10 lines

Log Buffer (131072 bytes):

*Mar 16 20:14:53.829: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback4, changed state to down
*Mar 16 20:14:53.830: %LINK-5-CHANGED: Interface Loopback4, changed state to administratively down
*Mar 16 20:15:03.836: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback4, changed state to up
*Mar 16 20:15:03.836: %LINK-3-UPDOWN: Interface Loopback4, changed state to up
csr1000v-1#
```

## Guestshell/Python Script Usage
```
csr1000v-1#bounce Loopback4 10
Interface Loopback4 will be bounced with a 10 second delay. Are you sure? (y/n)y
Line 1 SUCCESS:  interface Loopback4
Line 2 SUCCESS:  shutdown
Line 3 SUCCESS:  end

Line 1 SUCCESS:  interface Loopback4
Line 2 SUCCESS:  no shutdown
Line 3 SUCCESS:  end

csr1000v-1#sh log last 10
Syslog logging: enabled (0 messages dropped, 3 messages rate-limited, 0 flushes, 0 overruns, xml disabled, filtering disabled)

Showing last 10 lines

Log Buffer (131072 bytes):

*Mar 16 20:29:48.331: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback4, changed state to down
*Mar 16 20:29:48.331: %LINK-5-CHANGED: Interface Loopback4, changed state to administratively down
*Mar 16 20:29:58.400: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback4, changed state to up
*Mar 16 20:29:58.400: %LINK-3-UPDOWN: Interface Loopback4, changed state to up
```

## Example Deployment
There are scripts using Nornir to deploy either the guestshell or Tcl solution. They require Nornir and two Nornir plugins: Scrapli and Netmiko. These are examples of how to deploy these scripts and not meant to be used in production networks.

```
➜  bounce-cli-iosxe git:(main) ✗ poetry run python deploy_guestshell_script.py
Configure IOx and app hosting.**************************************************
* ios-xe-mgmt-latest.cisco.com ** changed : True *******************************
vvvv Configure IOx and app hosting. ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvv INFO
iox
app-hosting appid guestshell
app-vnic management guest-interface 0

^^^^ END Configure IOx and app hosting. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Enable guestshell.**************************************************************
* ios-xe-mgmt-latest.cisco.com ** changed : False ******************************
vvvv Enable guestshell. ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface will be selected if configured in app-hosting
Please wait for completion
% Error: Guestshell already in RUNNING state

Python 3.6.8
^^^^ END Enable guestshell. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Copy script file to device.*****************************************************
* ios-xe-mgmt-latest.cisco.com ** changed : True *******************************
vvvv Copy script file to device. ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Successfully copied script file to device.
---- Delete previous script. ** changed : False -------------------------------- INFO
%Error deleting bootflash:guest-share/bounce.py (No such file or directory)

%Error deleting bootflash:bounce.py (No such file or directory)
---- Copy script to network device. ** changed : True -------------------------- INFO
True
---- Copy script to guest-share directory. ** changed : True ------------------- INFO
---- Delete script from root directory on flash. ** changed : False ------------ INFO
^^^^ END Copy script file to device. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create CLI alias.***************************************************************
* ios-xe-mgmt-latest.cisco.com ** changed : True *******************************
vvvv Create CLI alias. ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
```

```
➜  bounce-cli-iosxe git:(main) ✗ poetry run python deploy_tcl_script.py 
Copy bounce.tcl script to network device.***************************************
* ios-xe-mgmt-latest.cisco.com ** changed : True *******************************
vvvv Copy bounce.tcl script to network device. ** changed : True vvvvvvvvvvvvvvv INFO
True
^^^^ END Copy bounce.tcl script to network device. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create CLI alias.***************************************************************
* ios-xe-mgmt-latest.cisco.com ** changed : True *******************************
vvvv Create CLI alias. ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
alias exec bounce tclsh bounce.tcl

^^^^ END Create CLI alias. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```