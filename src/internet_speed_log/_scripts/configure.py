# SPDX-FileCopyrightText: 2025-present Christopher Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

import argparse
from   pathlib                      import Path
from   QuasarCode                   import Console, Settings
from   QuasarCode.IO.Configurations import PropertiesConfig
import sys

from internet_speed_log._config import _internal_config_file, InternetSpeedLogConfig



def main():

    parser = argparse.ArgumentParser(description = "Configure this Internet Speed Logger installation.")

    parser.add_argument("--location",      type = str,             help = "File containing configurations."        )
    parser.add_argument("--new-file",      action  = "store_true", help = "Create a new settings file and exit."   )
    parser.add_argument("--verbose", "-v", action  = "store_true", help = "Display extra information."             )
    parser.add_argument("--debug",   "-d", action  = "store_true", help = "Display extreme amounts of information.")

    # This will exit the program if -h or --help are specified
    args = parser.parse_args()

    if args.verbose:
        Settings.enable_verbose()
    if args.debug:
        Settings.enable_verbose()
        Settings.enable_debug()

    Console.print_verbose_info("Arguments:")
    for key in args.__dict__:
        Console.print_verbose_info(f"    {key}: {getattr(args, key)}")

    # New file
    if args.new_file:
        InternetSpeedLogConfig.create(Path.cwd().joinpath("internet-speed-log-config.yaml"))

    # Set the specified location
    elif args.location is not None:

        target_file = Path(args.location).absolute()

        if not target_file.exists():
            Console.print_error(f"Target configuration file \"{target_file}\" does not exist.")
            sys.exit(1)

        # Overwrite the existing file
        with _internal_config_file.open("w") as file:
            file.write(f"# Location of the configuration file:\nfilepath={target_file}\n")

    # No action requested - show usage info
    else:
        parser.print_help()
