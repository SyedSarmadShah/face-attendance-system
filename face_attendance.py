import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import csv
import logging

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
CSV_FILE = os.path.join(DATA_DIR, 'attendance.csv')
CONFIDENCE_THRESHOLD = 0.6  # Lower threshold = stricter matching (0-1)
ATTENDANCE_CACHE = {}  # Track attendance within session

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

known_encodings = []
known_names = []

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

logger.info("Loading encodings...")

if not os.path.isdir(DATASET_DIR):
    logger.warning(f"Dataset directory not found at {DATASET_DIR}. No faces loaded.")
else:
    for person_name in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue

    for img_name in os.listdir(person_dir):
        try:
            img_path = os.path.join(person_dir, img_name)
            image = face_recognition.load_image_file(img_path)
            locations = face_recognition.face_locations(image)

            if len(locations) != 1:
                logger.warning(f"Skipping {img_name}: found {len(locations)} faces.")
                continue

            encoding = face_recognition.face_encodings(image, known_face_locations=locations)[0]
            known_encodings.append(encoding)
            known_names.append(person_name)
            logger.debug(f"Loaded: {person_name}/{img_name}")
        except Exception as e:
            logger.error(f"Error loading {img_name}: {e}")

logger.info(f"Encodings loaded successfully. Total faces: {len(known_encodings)}")

def mark_attendance(name):
    """Mark attendance in CSV file, preventing duplicates within same day"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check session cache first (prevents multiple marks within minutes)
        if name in ATTENDANCE_CACHE and ATTENDANCE_CACHE[name] == today:
            return False
        
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Date', 'Time'])

        # Check if already marked today
        with open(CSV_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2 and row[0] == name and row[1] == today:
                    logger.info(f"Attendance already marked for {name} today.")
                    return False

        # Mark new attendance
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            writer.writerow([name, date, time])
            ATTENDANCE_CACHE[name] = today
            logger.info(f"Attendance marked: {name} at {time}")
            return True
    except Exception as e:
        logger.error(f"Error marking attendance: {e}")
        return False


try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Failed to open camera. Check if webcam is connected.")
        exit(1)
    logger.info("Camera started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to read from camera.")
            break

        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small, model='hog')  # Fast model
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            # Apply confidence threshold
            if face_distances[best_match_index] < CONFIDENCE_THRESHOLD:
                name = known_names[best_match_index]
                confidence = 1 - face_distances[best_match_index]
                mark_attendance(name)
            else:
                name = "Unknown"
                confidence = 0

            # Draw box and label with confidence score
            top, right, bottom, left = [v * 4 for v in face_location]
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            label = f"{name} ({confidence:.2f})" if name != "Unknown" else name
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Face Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    logger.error(f"Camera error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Camera released and all windows closed.")
