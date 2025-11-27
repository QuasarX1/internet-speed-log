# SPDX-FileCopyrightText: 2025-present Christopher Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

from platform import platform
import subprocess

class SSIDRetrievalError(Exception):
    """
    Error raised when unable to locate the current SSID.
    Can be raised if no network is found or if the OS is unsupported.
    """

def get_ssid_windows():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell = True, text = True)
        for line in result.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except Exception as e:
        raise SSIDRetrievalError(f"Unable to get SSID on Windows: {e}")

def get_ssid_mac():
    try:
        result = subprocess.check_output(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
            text=True
        )
        for line in result.split("\n"):
            if "SSID" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        raise SSIDRetrievalError(f"Unable to get SSID on Mac: {e}")

def get_ssid_linux():
    try:
        result = subprocess.check_output(["iwgetid", "-r"], text = True)
        return result.strip()
    except Exception as e:
        raise SSIDRetrievalError(f"Unable to get SSID on Linux: {e}")

def get_current_ssid() -> str:
    match platform().lower():
        case p if "windows" in p:
            return get_ssid_windows()
        case p if "darwin" in p:
            return get_ssid_mac()
        case p if "linux" in p:
            return get_ssid_linux()
        case _:
            raise SSIDRetrievalError("Unsupported platform.")
