# SPDX-FileCopyrightText: 2025-present Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

import sys

from   QuasarCode import Console



# Get commandlet functions
from .configure import main as run_configure#TODO:
from .log       import main as run_log
from .plot      import main as run_plot



commandlets = {
    "configure" : run_configure,
    "log"       : run_log,
    "plot"      : run_plot,
}



def main():
    arguments = list(sys.argv[1:])

    if len(arguments) == 0 or arguments[0].replace("-", "").lower() in ("help", "h"):
        # Print command information and exit
        print(
"""
--|| Internet Speed Log ||--

Log internet speed and plot logged data.

usage: internet-speed-log [commandlet] [options | --help]
       internet-speed-log [--help | -h]

Commandlets:

    help      ->  Displays this message.

    configure -> Configure internet speed log.

    log       ->  Log internet speed.

    plot      ->  Generate plots from logged data.
""",
            flush = True
        )
        sys.exit(0)
        
    else:
        # Look for a script to run

        if arguments[0] in commandlets:
            sys.argv = [sys.argv[0]] + sys.argv[2:]
            Console.show_times()
            Console.reset_stopwatch()
            commandlets[arguments[0]]()
            sys.exit(0) # If the commandlet returns, assume success

        else:
            Console.print_error(f"Internet Speed Log: unrecognised commandlet: {arguments[0]}", flush=True)
            sys.exit(1)



if __name__ == "__main__":
    main()
