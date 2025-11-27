# SPDX-FileCopyrightText: 2025-present Christopher Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

from pathlib                      import Path
from QuasarCode.IO.Configurations import YamlConfig, PropertiesConfig



_internal_config_file = Path(__file__).parent.joinpath("config.properties")

default_config_text = """\
# Internet Speed Log Configuration

# Logging Options

log_interval:        10 # minutes (must be a multiple of `kill_check_interval`)
repeats:             1

# Application Options

kill_check_interval:               5  # seconds
missing_connection_retries:        3
missing_connection_retry_interval: 30 # seconds
"""

class InternetSpeedLogConfig(YamlConfig):
    """
    Configuration for Internet Speed Log application.
    """

    def __new__(cls, *args, **kwargs):
        if not _internal_config_file.exists():
            raise FileNotFoundError("Unable to locate internal config file.")
        target_file = Path(PropertiesConfig().from_file(str(_internal_config_file)).filepath)
        if not target_file.exists():
            raise FileNotFoundError(f"Unable to locate config file: \"{target_file}\".")
        return cls.from_file(str(target_file), *args, **kwargs)
    
    @staticmethod
    def create(filepath: Path) -> None:
        with filepath.open("w") as file:
            file.write(default_config_text)
