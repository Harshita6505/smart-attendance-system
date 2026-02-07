import cv2
import os

# ====== CONFIG ======
person_name = "Harshita_Grover"   # Change name for each person
save_path = f"dataset/{person_name}"
img_count = 0
max_images = 30   # Number of images to capture

# Create folder if not exists
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

print("[INFO] Press 'c' to capture image")
print("[INFO] Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        face_img = frame[y:y+h, x:x+w]

        if cv2.waitKey(1) & 0xFF == ord('c'):
            img_count += 1
            img_name = f"{person_name}_{img_count}.jpg"
            cv2.imwrite(os.path.join(save_path, img_name), face_img)
            print(f"[SAVED] {img_name}")

    cv2.putText(frame, f"Images: {img_count}/{max_images}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Dataset Capture", frame)

    if img_count >= max_images:
        print("[INFO] Dataset collection completed")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
