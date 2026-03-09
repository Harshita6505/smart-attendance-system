import cv2
import face_recognition
import pickle
import os
import csv
import numpy as np
from datetime import datetime
from scipy.spatial import distance as dist

ENCODINGS_FILE = "encodings/face_encodings.pkl"
ATTENDANCE_FILE = "attendance/attendance.csv"
SUBJECT = input("Enter Subject Name: ").strip()

EYE_AR_THRESH = 0.27
EYE_AR_CONSEC_FRAMES = 1
MATCH_THRESHOLD = 0.55

print("[INFO] Loading encodings...")

with open(ENCODINGS_FILE, "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

print(f"[INFO] Registered Students: {len(set(known_names))}")
print("[INFO] System Started - Press 'q' to Quit\n")

os.makedirs("attendance", exist_ok=True)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time", "Subject"])

marked_today = set()
blink_counter = {}
blink_confirmed = set()

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if name in marked_today:
        return

    marked_today.add(name)

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, date, time, SUBJECT])

    print(f"[ATTENDANCE MARKED] {name} | {date} | {time} | {SUBJECT}")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)
    landmarks = face_recognition.face_landmarks(rgb)

    for encoding, box, lm in zip(encodings, boxes, landmarks):

        name = "Unknown"
        status = "UNKNOWN"

        if len(known_encodings) > 0:
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < MATCH_THRESHOLD:
                name = known_names[best_match_index]

        if name != "Unknown":

            if "left_eye" in lm and "right_eye" in lm:

                leftEye = np.array(lm["left_eye"])
                rightEye = np.array(lm["right_eye"])

                ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

                if name not in blink_counter:
                    blink_counter[name] = 0

                if ear < EYE_AR_THRESH:
                    blink_counter[name] += 1
                else:
                    if blink_counter[name] >= EYE_AR_CONSEC_FRAMES:
                        blink_confirmed.add(name)
                    blink_counter[name] = 0

            if name in blink_confirmed:
                mark_attendance(name)
                status = "LIVE"
            else:
                status = "NO LIVENESS"

        top, right, bottom, left = box
        color = (0,255,0) if status == "LIVE" else (0,0,255)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{name} | {status}",
                    (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, color, 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n[INFO] System Closed")
        break

cap.release()
cv2.destroyAllWindows()