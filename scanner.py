import cv2
import face_recognition
import sys
import os

def scan_face():
    owner_path = "/usr/local/bin/skyid/owner.jpg"
    if not os.path.exists(owner_path):
        sys.exit(1)

    owner_image = face_recognition.load_image_file(owner_path)
    owner_encoding = face_recognition.face_encodings(owner_image)[0]
    video_capture = cv2.VideoCapture(0)
    
    for i in range(20):
        ret, frame = video_capture.read()
        if not ret: continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([owner_encoding], face_encoding)
            if match[0]:
                video_capture.release()
                return True
    video_capture.release()
    return False

if __name__ == "__main__":
    if scan_face(): sys.exit(0)
    else: sys.exit(1)
