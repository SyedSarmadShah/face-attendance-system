import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import csv


DATASET_DIR = 'dataset' 
CSV_FILE = 'attendance.csv'


known_encodings = []
known_names = []

print("✅ Loading encodings...")

for person_name in os.listdir(DATASET_DIR):
    person_dir = os.path.join(DATASET_DIR, person_name)
    if not os.path.isdir(person_dir):
        continue

    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        image = face_recognition.load_image_file(img_path)
        locations = face_recognition.face_locations(image)

        if len(locations) != 1:
            print(f"⚠️ Skipping {img_name}: found {len(locations)} faces.")
            continue

        encoding = face_recognition.face_encodings(image, known_face_locations=locations)[0]
        known_encodings.append(encoding)
        known_names.append(person_name)

print("✅ Encodings loaded successfully.")

def mark_attendance(name):
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Date', 'Time'])

    with open(CSV_FILE, 'r+') as f:
        data = f.readlines()
        names_logged = [line.split(',')[0] for line in data[1:]]  # Skip header
        if name not in names_logged:
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            f.write(f'{name},{date},{time}\n')
            print(f"📝 Attendance marked: {name}")


cap = cv2.VideoCapture(0)
print("📷 Camera started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read from camera.")
        break


    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]
            mark_attendance(name)

     
        top, right, bottom, left = [v * 4 for v in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("🛑 Camera released and all windows closed.")
