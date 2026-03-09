import face_recognition
import cv2
import os
import pickle

dataset_path = "dataset"
encoding_path = "encodings/face_encodings.pkl"

known_encodings = []
known_names = []

print("[INFO] Encoding faces...")

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_folder):
        continue

    for img_name in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_name)

        image = cv2.imread(img_path)
        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(person_name)

data = {"encodings": known_encodings, "names": known_names}

os.makedirs("encodings", exist_ok=True)

with open(encoding_path, "wb") as f:
    pickle.dump(data, f)

print(f"[INFO] Total faces encoded: {len(known_names)}")
print("[INFO] Encoding completed successfully!")