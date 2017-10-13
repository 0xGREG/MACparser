import re
import sys

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
                if not re.match(r"^([\dA-F]{2}[:-]){2}[\dA-F]{2}", line): # We don't need to process the line if it doesn't contain MAC patterns
                    continue
                args = line.split("\t")
                windows = False
                if re.match(r"^([\dA-F]{2}-){5}[\dA-F]{2}/\d{1,2}", args[0]):
                    args[0] = re.sub("-",":",args[0])
                    windows = True
                if re.match(r"^([\dA-F]{2}-){5}[\dA-F]{2}", args[0]):
                    args[0] = re.sub("-",":",args[0])
                    args[0] = args[0] + "/48"
                    windows = True
                if re.match(r"^([\dA-F]{2}:){5}[\dA-F]{2}/\d{1,2}", args[0]): #checking if that mac is a subgroup
                    if (globals.match == False and windows == False):
                        continue # We don't want to check the extended options if we know that first bits already have no match
                    if verifyFullMac(args[0], mac) == True:
                        args[1] = args[1].split(" ")
                        globals.matchedVendor = args[1][0]
                        break
                    else:
                        continue
            
                if globals.match == True:
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

def parse(mac):
    check(mac)

if len(sys.argv) == 2:
    try:
        address = sys.argv[1]
        
        if not re.match(r"^([\dA-Fa-f]{2}:){5}[\dA-Fa-f]{2}$", address):
            print("Correct usage: MACparser macNumber")
            print("Example: MACparser 00:11:22:33:44:55")
            exit()

        parse(address)

    except:
        print("Correct usage: MACparser macNumber")
        print("Example: MACparser 00:11:22:33:44:55")
        exit()
    exit()

for line in sys.stdin:
    try:
        line = re.sub("-", ":", line)
        addresses = re.findall(r"(([\dA-Fa-f]{2}:){5}[\dA-Fa-f]{2})", line)
        for address in addresses:
            parse(address[0])

    except:
        continue
    