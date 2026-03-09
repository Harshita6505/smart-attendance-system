
import csv
from datetime import datetime
import os

ATTENDANCE_FILE = "attendance.csv"

def mark_attendance(name):
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Date", "Time"])

    with open(ATTENDANCE_FILE, "r") as f:
        existing = f.read()

    if name in existing:
        return  # already marked

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, date, time])

    print(f"[ATTENDANCE] Marked for {name}")
