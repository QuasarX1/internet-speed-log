# SPDX-FileCopyrightText: 2025-present Christopher Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

from   QuasarCode import Console
from   pathlib    import Path
import socket
from   speedtest  import Speedtest
import time
from   threading  import Thread
import threading
import os
import datetime

from internet_speed_log import InternetSpeedLogConfig, get_current_ssid, SSIDRetrievalError, LegacyDataFile, LegacyDataRecord



def test_connection() -> LegacyDataRecord:
    pass#TODO:



def main():

    config = InternetSpeedLogConfig()

    machine_name:      str = socket.gethostname()
    log_file_template: str = f"internet-speed-log-{machine_name}-{{}}.txt"

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

        connected: bool
        try:
            ssid = get_current_ssid()
            connected = True
        except SSIDRetrievalError as e:
            connected = False
            Console.print_error(f"Unable to find an active network connection. Retrying in {config.log_interval} seconds...")

        if connected:

            log_file_path = Path.cwd().joinpath(log_file_template.format(ssid))
            log_file = LegacyDataFile(log_file_path)

            logs = []
            for _ in range(config.repeats):
                logs.append(test_connection())
            
            log_file.insert(*logs)

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
