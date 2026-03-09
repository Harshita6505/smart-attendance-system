import cv2
import os

person_name = input("Enter person name (use underscore, e.g. Simran_Grover): ").strip()
save_path = os.path.join("dataset", person_name)

max_images = 25
img_count = 0

if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"[INFO] Created folder: {save_path}")
else:
    print(f"[INFO] Using existing folder: {save_path}")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

print("\nPress 'c' to capture | Press 'q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    face_img = None

    for (x, y, w, h) in faces:
        margin = 20
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(frame.shape[1], x + w + margin)
        y2 = min(frame.shape[0], y + h + margin)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        face_img = frame[y1:y2, x1:x2]

    cv2.putText(frame, f"{person_name} {img_count}/{max_images}",
                (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Capture Dataset", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and face_img is not None and len(faces) == 1:
        img_count += 1
        face_resized = cv2.resize(face_img, (256, 256))
        img_name = f"{person_name}_{img_count}.jpg"
        cv2.imwrite(os.path.join(save_path, img_name), face_resized)
        print(f"[SAVED] {img_name}")

    elif key == ord('q'):
        break

    if img_count >= max_images:
        print("[INFO] Dataset completed")
        break

cap.release()
cv2.destroyAllWindows()

print("\nNow run: python encode_faces.py")