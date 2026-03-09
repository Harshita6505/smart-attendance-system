Smart Attendance System using Computer Vision
Overview
A real-time Face Recognition Based Attendance System with Liveness Detection to prevent spoofing using photos.

This project uses Computer Vision and Face Recognition to automatically mark attendance when a registered student is detected on camera.
Features
• Real-time face detection and recognition
• Blink-based liveness detection (prevents photo spoofing)
• Automatic attendance marking
• Subject-wise attendance logging
• Attendance saved in CSV and Excel format
• Easy dataset registration for new users
• Terminal display showing whose attendance is marked
Tech Stack
Python
OpenCV
face_recognition
Dlib
NumPy
Pandas
Project Structure
smart_attendance_system
│
├── capture_dataset.py
├── encode_faces.py
├── main.py
├── face_recognition_module.py
├── liveness_detection.py
├── attendance_logic.py
├── camera.py
├── utils.py
│
├── dataset/      (ignored from GitHub)
├── encodings/    (ignored from GitHub)
├── attendance/   (ignored from GitHub)
│
├── requirements.txt
└── README.md
Installation
1. Clone the repository
git clone https://github.com/Harshita6505/smart-attendance-system.git

2. Move to project folder
cd smart-attendance-system

3. Create virtual environment
python -m venv venv

4. Activate environment (Windows)
venv\Scripts\activate

5. Install dependencies
pip install -r requirements.txt
Usage
1. Capture Face Dataset
python capture_dataset.py

2. Encode Faces
python encode_faces.py

3. Run Attendance System
python main.py

Enter subject name when prompted.
Example:
Enter Subject Name: AIML
Attendance Output
Attendance is stored in:
attendance/attendance.csv

Format:
Name, Date, Time, Subject

Example:
Harshita_Grover,2026-03-09,22:06:28,AIML
## Screenshots

### Attendance Marked in Terminal

![Terminal Output](images/terminal_output.png)

### Attendance CSV File

![CSV Output](images/attendance_csv.png)

Sensitive biometric data such as:
• Face images
• Face encodings
• Attendance logs
are not included in the repository and are ignored using .gitignore.

Author
Harshita Grover
Suhani Chhabra

