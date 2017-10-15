import time
import os
import sys

try:
    iterations = int(sys.argv[1])
except:
    iterations = 10

try:
    file = sys.argv[2]
    testFile = open(file, "r")
    testFile.close()
except:
    file = "test.txt"

times = []
messages = []

messages.append("Selected test file: " + file)
messages.append("")

def display(iteration):
    os.system("clear")
    for line in messages:
        print(line)
    if not iteration == -1:
        counter = ""
        for i in range (iterations):
            if i+1 <= iteration:
                counter = counter + "|"
            else:
                counter = counter + "-"
        print("\nIteration " + str(iteration) + "/" + str(iterations) + " " + counter)

for i in range(iterations):
    display(i + 1)
    currentTime = time.time()
    os.system('cat ' + file + ' | python3 MACparser.py > /dev/null')  
    times.append(time.time() - currentTime)

messages.append("Average execution time: " + str(round(sum(times)/float(len(times)), 3)))

times = []

for i in range(iterations):
    display(i + 1)
    currentTime = time.time()
    os.system('cat ' + file + ' | python3 MACparser.py -p > /dev/null')  
    times.append(time.time() - currentTime)

messages.append("Average execution time with partial flag: " + str(round(sum(times)/float(len(times)), 3)))

display(-1)