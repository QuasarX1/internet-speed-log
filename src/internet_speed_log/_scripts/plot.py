# SPDX-FileCopyrightText: 2025-present Christopher Christopher J. R. Rowe <chris.rowe19@outlook.com>
#
# SPDX-License-Identifier: LicenseRef-Internet-Speed-Log-1.0

import os
import sys
import datetime
import numpy as np
from matplotlib import pyplot as plt

def main():

    if len(sys.argv) > 1:
        logFile = sys.argv[1]
        print(f"--|| INFO ||-- Using data from file: {logFile}")
    else:
        logFile = "./log.txt"

    if not os.path.exists(logFile):
        print("No data available.")
        input("Press enter to exit...")
        sys.exit()

    with open(logFile, "r") as file:
        lines = file.readlines()

    timestamps = []
    datetimes = []
    pings = []
    download_speeds = []
    upload_speeds = []
    server_urls = []
    server_IDs = []
    first = True
    for line in lines:
        if first:
            first = False
            continue
        line_elements = line.rstrip("\n").split(" ")
        timestamps.append(line_elements[0])
        datetimes.append(datetime.datetime.strptime(line_elements[0], "%Y/%m/%dT%H:%M:%S"))
        pings.append(float(line_elements[1]))
        download_speeds.append(float(line_elements[2]))
        upload_speeds.append(float(line_elements[3]))
        server_urls.append(line_elements[4])
        server_IDs.append(line_elements[5])
    timestamps = np.array(timestamps)
    datetimes = np.array(datetimes)
    pings = np.array(pings)
    download_speeds = np.array(download_speeds) / (1024**2)
    upload_speeds = np.array(upload_speeds) / (1024**2)
    server_urls = np.array(server_urls)
    server_IDs = np.array(server_IDs)



    mean_download = download_speeds.mean()

    mean_upload = upload_speeds.mean()

    mean_ping = pings.mean()

    download_speeds_copy = download_speeds.copy()
    download_speeds_copy.sort()
    download_half_way_point = int((len(download_speeds) - 1) / 2)
    median_download = (download_speeds_copy[download_half_way_point] + download_speeds_copy[download_half_way_point]) / 2

    upload_speeds_copy = upload_speeds.copy()
    upload_speeds_copy.sort()
    upload_half_way_point = int((len(upload_speeds) - 1) / 2)
    median_upload = (upload_speeds_copy[upload_half_way_point] + upload_speeds_copy[upload_half_way_point]) / 2

    pings_copy = pings.copy()
    pings_copy.sort()
    ping_half_way_point = int((len(pings) - 1) / 2)
    median_ping = (pings_copy[ping_half_way_point] + pings_copy[ping_half_way_point]) / 2



    plt.plot(datetimes, download_speeds, label = "Download")
    plt.plot(datetimes, upload_speeds, label = "Upload")
    x_lims = plt.xlim()
    plt.plot(x_lims, (median_download, median_download), c = "r", label = "Median Download")
    plt.plot(x_lims, (median_upload, median_upload), c = "r", label = "Median Upload")
    plt.plot(x_lims, (mean_download, mean_download), c = "k", linestyle = "--", label = "Mean Download")
    plt.plot(x_lims, (mean_upload, mean_upload), c = "k", linestyle = "--", label = "Mean Upload")
    plt.xlim(x_lims)
    plt.ylim((0, plt.ylim()[1]))
    plt.legend()
    plt.title("Download and Upload Speeds Over Time")
    plt.xlabel("Date and Time")
    plt.ylabel("Speed (Mb/s)")
    plt.show()

    plt.plot(datetimes, pings, label = "Ping")
    x_lims = plt.xlim()
    plt.plot(x_lims, (median_ping, median_ping), c = "r", label = "Median")
    plt.plot(x_lims, (mean_ping, mean_ping), c = "k", linestyle = "--", label = "Mean")
    plt.xlim(x_lims)
    plt.ylim((0, plt.ylim()[1]))
    plt.legend()
    plt.title("Ping Time Over Time")
    plt.xlabel("Date and Time")
    plt.ylabel("Time (s)")
    plt.show()



    weekdays = np.array([value.isoweekday() - 1 for value in datetimes], dtype = np.int8)# 0 = monday
    #weekly_timedeltas = [value - datetime.datetime(year = value.year, month = value.month, day = value.day) + datetime.timedelta(hours = (value.isoweekday() - 1) * 24) for value in datetimes]
    get_hours_from_time = lambda t: t.hour + (t.minute + (t.second + (t.microsecond / 1E6) / 60)) / 60
    weekly_time_in_hours = np.array([get_hours_from_time(value.time()) + ((value.isoweekday() - 1) * 24) for value in datetimes], dtype = np.float64)
    #datapoint_days_of_the_week = np.array([value.days for value in weekly_timedeltas], dtype = np.int8)
    #datapoint_hours_of_day = np.array([value.seconds / 60**2 for value in weekly_timedeltas], dtype = np.float64)
    weekly_day_centres = np.array([weekly_time_in_hours[weekdays == i].mean() for i in range(7)], dtype = np.float16)
    daily_errors = np.array([weekly_time_in_hours[weekdays == i].std() for i in range(7)], dtype = np.float16)

    daily_fastest_10th_percentile_download = [np.percentile(download_speeds[weekdays == i], 10) for i in range(7)]
    daily_fastest_90_percent_download_filter = [download_speeds[weekdays == i] > daily_fastest_10th_percentile_download[i] for i in range(7)]
    daily_mean_download_speeds = np.array([download_speeds[weekdays == i][daily_fastest_90_percent_download_filter[i]].mean() for i in range(7)], dtype = np.float64)
    daily_download_speed_std = np.array([download_speeds[weekdays == i][daily_fastest_90_percent_download_filter[i]].std() for i in range(7)], dtype = np.float64)
    daily_median_download_speeds = np.array([np.median(download_speeds[weekdays == i]) for i in range(7)], dtype = np.float64)
    plt.scatter(weekly_time_in_hours, download_speeds, s = 0.7)
    plt.errorbar(weekly_day_centres, daily_median_download_speeds, xerr = daily_errors, label = "Daily Median", linestyle = "", c = "green")
    plt.errorbar(weekly_day_centres, daily_mean_download_speeds, xerr = daily_errors, yerr = daily_download_speed_std, label = "Daily Mean", linestyle = "", c = "red")
    x_lims = plt.xlim()
    plt.plot([0.0, 24.0, 24.0, 48.0, 48.0, 72.0, 72.0, 96.0, 96.0, 120.0, 120.0, 144.0, 144.0, 168.0],
            [daily_fastest_10th_percentile_download[0], daily_fastest_10th_percentile_download[0],
            daily_fastest_10th_percentile_download[1], daily_fastest_10th_percentile_download[1],
            daily_fastest_10th_percentile_download[2], daily_fastest_10th_percentile_download[2],
            daily_fastest_10th_percentile_download[3], daily_fastest_10th_percentile_download[3],
            daily_fastest_10th_percentile_download[4], daily_fastest_10th_percentile_download[4],
            daily_fastest_10th_percentile_download[5], daily_fastest_10th_percentile_download[5],
            daily_fastest_10th_percentile_download[6], daily_fastest_10th_percentile_download[6]],
            c = "r", linestyle = "--", label = "Mean Cutoff")
    plt.xlim(x_lims)
    plt.ylim((0, plt.ylim()[1]))
    plt.legend()
    plt.title("Download speeds on each day of the week.")
    plt.xlabel("Hours since 00:00 on Monday")
    plt.ylabel("Speed (Mb/s)")
    plt.show()

    daily_fastest_10th_percentile_upload = [np.percentile(upload_speeds[weekdays == i], 10) for i in range(7)]
    daily_fastest_90_percent_upload_filter = [upload_speeds[weekdays == i] > daily_fastest_10th_percentile_download[i] for i in range(7)]
    daily_mean_upload_speeds = np.array([upload_speeds[weekdays == i][daily_fastest_90_percent_upload_filter[i]].mean() for i in range(7)], dtype = np.float64)
    daily_upload_speed_std = np.array([upload_speeds[weekdays == i][daily_fastest_90_percent_upload_filter[i]].std() for i in range(7)], dtype = np.float64)
    daily_median_upload_speeds = np.array([np.median(upload_speeds[weekdays == i]) for i in range(7)], dtype = np.float64)
    plt.scatter(weekly_time_in_hours, upload_speeds, s = 0.7)
    plt.errorbar(weekly_day_centres, daily_median_upload_speeds, xerr = daily_errors, label = "Daily Median", linestyle = "", c = "green")
    plt.errorbar(weekly_day_centres, daily_mean_upload_speeds, xerr = daily_errors, yerr = daily_upload_speed_std, label = "Daily Mean", linestyle = "", c = "red")
    x_lims = plt.xlim()
    plt.plot([0.0, 24.0, 24.0, 48.0, 48.0, 72.0, 72.0, 96.0, 96.0, 120.0, 120.0, 144.0, 144.0, 168.0],
            [daily_fastest_10th_percentile_upload[0], daily_fastest_10th_percentile_upload[0],
            daily_fastest_10th_percentile_upload[1], daily_fastest_10th_percentile_upload[1],
            daily_fastest_10th_percentile_upload[2], daily_fastest_10th_percentile_upload[2],
            daily_fastest_10th_percentile_upload[3], daily_fastest_10th_percentile_upload[3],
            daily_fastest_10th_percentile_upload[4], daily_fastest_10th_percentile_upload[4],
            daily_fastest_10th_percentile_upload[5], daily_fastest_10th_percentile_upload[5],
            daily_fastest_10th_percentile_upload[6], daily_fastest_10th_percentile_upload[6]],
            c = "r", linestyle = "--", label = "Mean Cutoff")
    plt.xlim(x_lims)
    plt.ylim((0, plt.ylim()[1]))
    plt.legend()
    plt.title("Upload speeds on each day of the week.")
    plt.xlabel("Hours since 00:00 on Monday")
    plt.ylabel("Speed (Mb/s)")
    plt.show()



    plt.scatter(download_speeds, upload_speeds, s = 0.7)
    x_lims = plt.xlim()
    y_lims = plt.ylim()
    plt.plot((median_download, median_download), y_lims, c = "r", label = "Median")
    plt.plot(x_lims, (median_upload, median_upload), c = "r")
    plt.plot((mean_download, mean_download), y_lims, c = "k", linestyle = "--", label = "Mean")
    plt.plot(x_lims, (mean_upload, mean_upload), c = "k", linestyle = "--")
    plt.xlim((0, x_lims[1]))
    plt.ylim((0, y_lims[1]))
    plt.legend()
    plt.title("Upload Speed as a Function of Download Speed")
    plt.xlabel("Download Speed (Mb/s)")
    plt.ylabel("Upload Speed (Mb/s)")
    plt.show()



    plt.hist(download_speeds, bins = 100)
    y_lims = plt.ylim()
    plt.plot((median_download, median_download), y_lims, c = "r", label = "Median")
    plt.plot((mean_download, mean_download), y_lims, c = "k", linestyle = "--", label = "Mean")
    plt.ylim(y_lims)
    plt.title("Download Speed")
    plt.xlabel("Speed (Mb/s)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

    plt.hist(upload_speeds, bins = 100)
    y_lims = plt.ylim()
    plt.plot((median_upload, median_upload), y_lims, c = "r", label = "Median")
    plt.plot((mean_upload, mean_upload), y_lims, c = "k", linestyle = "--", label = "Mean")
    plt.ylim(y_lims)
    plt.title("Upload Speed")
    plt.xlabel("Speed (Mb/s)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

    plt.hist(pings, bins = 200)
    y_lims = plt.ylim()
    plt.plot((median_ping, median_ping), y_lims, c = "r", label = "Median")
    plt.plot((mean_ping, mean_ping), y_lims, c = "k", linestyle = "--", label = "Mean")
    plt.ylim(y_lims)
    plt.title("Ping Speed")
    plt.xlabel("Ping Time (s)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
