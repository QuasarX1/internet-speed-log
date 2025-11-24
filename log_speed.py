#from speedtest import Speedtest
#tester = Speedtest()
#tester.get_servers([])
#print(tester.get_best_server())
#print(tester.download())
#print(tester.upload())
#print(tester.results.dict())
#exit()

from speedtest import Speedtest
import time
from threading import Thread
import threading
import os
import datetime

logFile = "./log.txt"
logInterval: int = 10# minutes
exitTestDelay: int = 30# seconds
killPrompt = "Press X to terminate application..."

kill = threading.Event()
def getKill(killEvent):
    while True:
        value = input(killPrompt)
        if value.lower() != "x":
            print("Invalid input. Application continuing.\n" + killPrompt)
        else:
            print("Exiting...")
            killEvent.set()
            break

killInputThread = Thread(target = getKill, args = (kill, ), daemon = True)
killInputThread.start()

tester = Speedtest()
while not kill.is_set():
    tester.get_servers([])
    tester.get_best_server()
    tester.download()
    tester.upload()
    results = tester.results.dict()
    newFile = not os.path.exists(logFile)
    with open(logFile, "a") as file:
        if newFile:
            file.write("Timestamp Ping Download Upload Server Server-ID\n")
        file.write(datetime.datetime.now().strftime("%Y/%m/%dT%H:%M:%S") + " " + str(results["ping"]) + " " + str(results["download"]) + " " + str(results["upload"]) + " " + str(results["server"]["url"]) + " " + str(results["server"]["id"]) + "\n")
    for _ in range(int(logInterval * 60 / exitTestDelay)):
        if kill.is_set(): break
        time.sleep(exitTestDelay)

killInputThread.join()
