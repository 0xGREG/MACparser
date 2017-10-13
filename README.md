# MACparser
Gets MAC address and gives the device manufacturer

## Installation
In order to install the script you need to pull/download this repository and run install script (as root).
It'll copy files to correct directories and in case wireshark is not installed will copy the vendors list 
to /usr/share/wireshark (version from 13.10.2017) (otherwise will use the one generated by wireshark)

## Prerequisities
- Linux device
- Python3
- Wireshark (optional) (if not present script will use the list provided with this repo)

## Usage
- Interactive mode:
  `MACparser`
- Single command mode:
  `MACparser 00:11:22:33:44:55 [00:00:00:00:00:00]`
- Pipe mode (example):
  `cat test.txt | MACparser`
  
 ## Interactive mode
You won't be greeted with any prompt, you just enter mac addresses and accept by return key

## Single command mode
You can enter multiple MAC addresses to check at the same time
