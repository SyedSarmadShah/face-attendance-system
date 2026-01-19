# 🎥 Face Attendance System (Backend + React Frontend)

Real-time face-recognition attendance with a Flask API and a React dashboard. Webcam captures faces, matches them against the dataset, and logs attendance to CSV with date/time. Secure login (hashed passwords), duplicate-prevention per day, and cross-platform camera launcher.

---

## 🚀 Features

- 📷 Real-time webcam face detection/recognition (OpenCV + face_recognition)
- 🔐 Secure teacher login (bcrypt hashing) via Flask API
- 🧠 Confidence threshold and duplicate prevention (one mark per person per day)
- 🗂️ Dataset-per-person folders; encodings auto-loaded at startup
- 📝 Attendance saved to CSV; dashboard shows records and stats
- 🌐 React frontend with API calls, session handling, and camera launcher

---

## 💻 Technologies Used

- **Python 3** (Flask, flask-cors)
- **OpenCV**, **face_recognition**, **NumPy**
- **bcrypt** for password hashing
- **React + Vite** for the web UI
- **CSV** for attendance storage

---

## 📁 Project Structure

```
face-attendance-system/
├── app.py                 # Flask API (auth, stats, attendance, camera start)
├── face_attendance.py     # Camera + recognition loop
├── gui.py                 # Legacy Tkinter app (optional)
├── attendance.csv         # Attendance log (auto-created)
├── teacher_credentials.csv# Hashed credentials (auto-created)
├── dataset/               # Images per person (one folder per identity)
├── templates/             # Legacy Flask templates (not used by React)
└── frontend/              # React + Vite SPA
```

Each subfolder inside `dataset/` is one person's identity. Images should contain a single clear face.

---

## ⚙️ Setup

### Backend (Flask)
```bash
cd face-attendance-system
# activate your venv, then:
pip install -r requirements.txt  # or install: flask flask-cors opencv-python face_recognition numpy bcrypt

# start backend (allows React at port 5173 by default)
FRONTEND_ORIGIN=http://localhost:5173 python app.py
```

### Frontend (React + Vite)
```bash
cd face-attendance-system/frontend
npm install
npm run dev -- --host  # serves at http://localhost:5173
```

### Open the app
- Visit: http://localhost:5173
- Login or register; then click “Open Camera” to launch the desktop camera window (press `q` to quit).

### Direct camera (without React)
```bash
python face_attendance.py  # press q to quit
```

---

## 📦 Output

- Camera window draws boxes + confidence scores; green for known, red for unknown.
- Attendance logged to `attendance.csv` with Name, Date, Time (one entry per person per day).

---

## ❓ Notes on Recognition

- Uses `face_recognition` (dlib CNN) for encodings and matching.
- Confidence threshold is configurable in `face_attendance.py` (`CONFIDENCE_THRESHOLD`).
- HOG model is used for fast face location; adjust to CNN if you need higher accuracy.

---

## 🧩 Dataset Tips
- One folder per person under `dataset/`.
- Use clear, front-facing images; one face per image.
- Add images, then restart `face_attendance.py` so encodings reload.

---

## 🙌 Credits

Developed by **Syed Sarmad Shah**
Contributions welcome.

---

## 📌 License

This project is open-source and free to use for educational and non-commercial purposes.

```

---

Let me know when you push this — I can generate a clean project description + hashtags for your GitHub or LinkedIn bio too!
```
