#! /usr/bin/env pythone3

import datetime

def log_anomaly(message):
    with open("anomalies.log", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {message}\n")

def report_anomaly(message):
    print(f"ANOMALY DETECTED: {message}")
    log_anomaly(message)

