import cv2
import numpy as np

class LivenessDetector:
    def __init__(self):
        self.prev_gray = None
        self.motion_counter = 0
def is_live(self, frame, face_box):
    (top, right, bottom, left) = face_box
    face = frame[top:bottom, left:right]

    if face.size == 0:
        return False

    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)

    if self.prev_gray is None:
        self.prev_gray = gray
        return False

    diff = cv2.absdiff(self.prev_gray, gray)
    self.prev_gray = gray

    motion_score = np.sum(diff)

    # Normalize by face size
    area = gray.shape[0] * gray.shape[1]
    normalized_motion = motion_score / area

    # Adjusted threshold (much safer)
    if normalized_motion > 8:
        self.motion_counter += 1
    else:
        self.motion_counter = 0

    if self.motion_counter >= 3:
        return True
    else:
        return False