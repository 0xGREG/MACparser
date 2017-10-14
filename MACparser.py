import re
import sys
import time

class globals:
    """class providing global accessible variables"""
    match = False
    matchedString = ""
    matchedVendor = ""

def calculateLengthFromMask(mask):
    characters = mask / 4 # there is 4 bits in each character
    characters = int(characters + characters//2) # every 2 characters are followed by colla so we have to add those characters to pattern 
    if characters == 18:
        characters = characters - 1 # if it shows length 18 it means whole MAC is a pattern and we have remove last collon
    return characters

def verifyFullMac(pattern, mac):
    """ This function creates valid pattern to check mac against 
    pattern consisting of full MAC address and mask and checks it using verif """
    pattern = pattern.split("/")
    patternLength = calculateLengthFromMask(int(pattern[1]))
    pattern = pattern[0][:patternLength]
    return verifyMac(pattern, mac)

def verifyMac(pattern, mac):
    """ checks if mac address matches the pattern """
    valid = True
    iteration = 0
    for char in pattern:
        if (char != mac[iteration]):
            valid = False
            break
        iteration = iteration + 1
    if valid == True: # set global variables if pattern is matched
        globals.match = True
        globals.matchedString = pattern
    return valid

def check(mac):
    mac = mac.upper()
    try:
        with open("/usr/share/wireshark/manuf", "r", encoding="utf8") as maclist:
            for line in maclist:
                try:
                    if line[0] not in "0123456789ABCDEFabcdef": # if line starts with one of valid characters it contains MAC pattern
                        continue
                except: # empty sting
                    continue 
                args = line.split("\t")
                windows = False
                try: # if MAC is written in form 00-00... change it to 00:00..
                    if args[0][2] == '-':
                        args[0] = re.sub("-",":",args[0])
                        windows = True 
                except:
                    pass
                isPatternToBeChecked = False
                if re.match(r"^([\dA-F]{2}:){5}[\dA-F]{2}/\d{1,2}", args[0]): #checking if that mac is a subgroup
                    if globals.match == False and windows == False:
                        continue # We don't want to check the extended options if we know that first bits already have no match
                    isPatternToBeChecked = True
                    args[0] = args[0].split("/")
                    patternLength = calculateLengthFromMask(int(args[0][1]))
                    args[0] = args[0][0][:patternLength]
                    if args[0][-1]==":":
                        args[0] = args[0][:-1]
            
                if globals.match == True and isPatternToBeChecked == False: # If previous option was matched and MAC didn't match any extended options/extended options for this MAC did't exist, mark previous match as answer
                    break
                if verifyMac(args[0], mac) == True:
                    args[1] = args[1].split(" ")
                    globals.matchedVendor = args[1][0]
                    continue
    except IOError:
        print("You need wireshark installed!")
    if globals.match == False:
        print(mac + " noMatch")
    else:
        if globals.matchedVendor[-1] == "\n":
            globals.matchedVendor = globals.matchedVendor[0:len(globals.matchedVendor)-1]
        print(mac + " matches " + globals.matchedVendor)
    
    globals.match = False
    globals.matchedVendor = ""
    globals.matchedString = ""

if len(sys.argv) >= 2:
    for address in sys.argv[1:]:
        if not re.match(r"^([\dA-Fa-f]{2}:){5}[\dA-Fa-f]{2}$", address):
            print("Correct usage: MACparser macNumber")
            print("Example: MACparser 00:11:22:33:44:55")
            exit()
        parse(address)

for line in sys.stdin:
    try:
        line = re.sub("-", ":", line)
        addresses = re.findall(r"(([\dA-Fa-f]{2}:){5}[\dA-Fa-f]{2})", line)
        for address in addresses:
            check(address[0])

    except:
        continue