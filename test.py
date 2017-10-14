import time
import os

times = []

for i in range(10):
    currentTime = time.time()
    os.system('cat test.txt | python3 MACparser.py > /dev/null')  
    times.append(time.time() - currentTime)

print("Average execution time: " + str(sum(times)/float(len(times))))