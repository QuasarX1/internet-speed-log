# SPDX-FileCopyrightText: 2025-present Christopher Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from typing import Any

import numpy as np



class IDataRecord(ABC):
    """
    Interface for data record handling.
    """



class IDataFile(ABC):
    """
    Interface for data file handling.
    Filepaths are handled using the pathlib.Path class.
    """

    @staticmethod
    @abstractmethod
    def new(filepath: Path) -> "IDataFile":
        raise NotImplementedError

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert(self, *data) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_record(self, index: int) -> IDataRecord:
        raise NotImplementedError

    @abstractmethod
    def get_records(self, slice: slice) -> tuple[IDataRecord, ...]:
        raise NotImplementedError


    @property
    @abstractmethod
    def path(self) -> Path:
        raise NotImplementedError
    


@dataclass
class LegacyDataRecord(IDataRecord):
    """
    Implementation of IDataRecord for legacy data file format.
    """
    time:           datetime
    ping:           float
    download_speed: float
    upload_speed:   float
    server_url:     str
    server_ID:      str



class LegacyDataFile(IDataFile):
    """
    Implementation of IDataFile for legacy data file format.
    """

    def __init__(self, filepath: Path) -> None:

        # Check the path is valid
        if not filepath.is_file():
            raise ValueError(f"Provided path \"{filepath}\" is not a file.")
        if not filepath.exists():
            raise FileNotFoundError(f"Unable to locate data file at \"{filepath}\".")

        self.__path:         Path                   = filepath
        self.__loaded:       bool                   = False
        self.__data:         list[LegacyDataRecord] = []
        self.__update_index: int                    = 0

    @staticmethod
    def new(filepath: Path) -> "LegacyDataFile":

        # Check the path is valid
        if not filepath.is_file():
            raise ValueError(f"Provided path \"{filepath}\" is not a file.")
        if filepath.exists():
            raise FileExistsError(f"File already exists at \"{filepath}\".")

        # Insert the header line
        with filepath.open("w") as file:
            file.write("Timestamp Ping Download Upload Server Server-ID\n")

        return LegacyDataFile(filepath)

    def load(self) -> None:

        # Check the file still exists
        if not self.__path.exists():
            raise FileNotFoundError(f"Unable to locate data file at \"{self.__path}\".")
        
        with self.__path.open("r") as file:
            lines = file.readlines()
    
        loaded_data: list[LegacyDataRecord] = []
        for line in lines[1:]:# Skip header line
            line_elements = line.rstrip("\n").split(" ")
            record = LegacyDataRecord(
                time           = datetime.strptime(line_elements[0], "%Y/%m/%dT%H:%M:%S"),
                ping           = float(line_elements[1]),
                download_speed = float(line_elements[2]),
                upload_speed   = float(line_elements[3]),
                server_url     = line_elements[4],
                server_ID      = line_elements[5]
            )
            loaded_data.append(record)

        if len(self.__data) > 0:
            self.__data = loaded_data + self.__data
            self.__update_index = len(loaded_data)
        else:
            self.__data = loaded_data
            self.__update_index = len(self.__data)

    def insert(self, *data: LegacyDataRecord) -> None:

        self.__data.extend(data)

    def update(self) -> None:

        # Check the file still exists
        if not self.__path.exists():
            raise FileNotFoundError(f"Unable to locate data file at \"{self.__path}\".")
        if self.__update_index == len(self.__data):
            return# No updates to make
        backup_path = self.__path.with_suffix(self.__path.suffix + ".old")
        if backup_path.exists():
            backup_path.unlink()
        os.system(f'cp "{self.__path}" "{backup_path}"')
        #_ = self.__path.copy(backup_path)#TODO: update to Python3.14 for support of .copy
        with self.__path.open("a") as file:
            for record in self.__data[self.__update_index:]:
                file.write(f"{record.time.strftime('%Y/%m/%dT%H:%M:%S')} {record.ping} {record.download_speed} {record.upload_speed} {record.server_url} {record.server_ID}\n")
        self.__update_index = len(self.__data)

    @property
    def path(self) -> Path:
        return self.__path

    @staticmethod
    def _decorator_require_data_loaded(func):
        def wrapper(self, *args, **kwargs):
            if not self.__loaded:
                self.load()
            return func(self, *args, **kwargs)
        return wrapper

    @property
    @_decorator_require_data_loaded
    def timestamps(self) -> np.ndarray[tuple[int], np.dtype[np.str_]]:
        return np.array([r.time.strftime("%Y/%m/%dT%H:%M:%S") for r in self.__data], dtype = np.str_)

    @property
    @_decorator_require_data_loaded
    def datetimes(self) -> np.ndarray[tuple[int], Any]:
        return np.array([r.time for r in self.__data], dtype = datetime)

    @property
    @_decorator_require_data_loaded
    def pings(self) -> np.ndarray[tuple[int], np.dtype[np.float32]]:
        return np.array([r.ping for r in self.__data], dtype = np.float32)

    @property
    @_decorator_require_data_loaded
    def download_speeds(self) -> np.ndarray[tuple[int], np.dtype[np.float32]]:
        return np.array([r.download_speed for r in self.__data], dtype = np.float32)

    @property
    @_decorator_require_data_loaded
    def upload_speeds(self) -> np.ndarray[tuple[int], np.dtype[np.float32]]:
        return np.array([r.upload_speed for r in self.__data], dtype = np.float32)

    @property
    @_decorator_require_data_loaded
    def server_urls(self) -> np.ndarray[tuple[int], np.dtype[np.str_]]:
        return np.array([r.server_url for r in self.__data], dtype = np.str_)

    @property
    @_decorator_require_data_loaded
    def server_IDs(self) -> np.ndarray[tuple[int], np.dtype[np.str_]]:
        return np.array([r.server_ID for r in self.__data], dtype = np.str_)
    
    def __len__(self) -> int:
        return len(self.__data)
    
    def get_record(self, index: int) -> IDataRecord:
        return self.__data[index]
    
    def get_records(self, slice: slice) -> tuple[IDataRecord, ...]:
        return tuple(self.__data[slice])
