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



def test_connection(speed_tester: Speedtest, number_of_tests: int = 1) -> tuple[LegacyDataRecord, ...]:

    test_records: list[LegacyDataRecord] = []

    t = datetime.datetime.now()

    speed_tester.get_servers([])
    speed_tester.get_best_server()

    for _ in range(number_of_tests):
        speed_tester.download()
        speed_tester.upload()
        results = speed_tester.results.dict()

        test_records.append(LegacyDataRecord(
            time           = t,
            ping           = results["ping"    ],
            download_speed = results["download"],
            upload_speed   = results["upload"  ],
            server_url     = results["server"  ]["url"],
            server_ID      = results["server"  ]["id" ],
        ))

    return tuple(test_records)



def main() -> None:

    config = InternetSpeedLogConfig()

    machine_name:      str = socket.gethostname()
    log_file_template: str = f"internet-speed-log-{machine_name}-{{}}.txt"

    kill: threading.Event = threading.Event()
    def getKill(killEvent):
        Console.print_info("Return \"x\" at any time to terminate.")
        while True:
            value = input()
            if value.lower() != "x":
                Console.print_error(f"Invalid input \"{value}\". Return \"x\" to exit.")
            else:
                Console.print_raw()
                Console.print_info("Sent kill signal. Please wait for application to terminate!")
                killEvent.set()
                break

    killInputThread = Thread(target = getKill, args = (kill,), daemon = True)
    killInputThread.start()

    tester = Speedtest(shutdown_event = kill)

    while not kill.is_set():

        connected: bool
        ssid:      str
        attempts:  int = 0
        while True:
            try:
                ssid = get_current_ssid()
                connected = True
                break
            except SSIDRetrievalError:
                connected = False
                attempts += 1
                Console.print_error(f"Unable to find an active network connection (attempt {attempts}/{config.missing_connection_retries}).")

            if attempts <= config.missing_connection_retries:
                Console.print_warning(f"Retrying in {config.missing_connection_retry_interval} seconds...")
                time.sleep(config.missing_connection_retry_interval)
            else:
                break

        if connected:

            log_file:      LegacyDataFile
            log_file_path: Path           = Path.cwd().joinpath(log_file_template.format(ssid))
            if not log_file_path.exists():
                log_file = LegacyDataFile.new(log_file_path)
            else:
                log_file = LegacyDataFile(log_file_path)

            test_results = test_connection(tester, config.repeats)
            
            log_file.insert(*test_results)

            log_file.update()

            for _ in range(int(config.log_interval / config.kill_check_interval)):
                if kill.is_set(): break
                time.sleep(config.kill_check_interval)

        else:
            Console.print_info(f"No active network connection available. Retrying in {config.log_interval} seconds.")
            time.sleep(config.log_interval)

    killInputThread.join()
