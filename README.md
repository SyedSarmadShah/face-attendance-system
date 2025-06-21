# 🎥 Face Attendance System

An intelligent real-time Face Recognition-based Attendance System built using **Python**, **OpenCV**, and the `face_recognition` library. It uses face encodings to detect and identify individuals from a webcam feed and automatically logs attendance into a CSV file.

---

## 🚀 Features

- 📷 Real-time webcam-based face detection
- 🧠 Face recognition using pre-trained CNN model (via `face_recognition`)
- 📅 Automatic attendance logging with name, date, and time
- 📁 Folder-based dataset system (no need for manual training)
- 📝 Attendance saved in `attendance.csv`

---

## 💻 Technologies Used

- **Python 3**
- **OpenCV**
- **face_recognition** (built on top of dlib + deep CNN)
- **NumPy**
- **CSV module**

---

## 📁 Project Structure

```

face-attendance-system/
│
├── main.py               # Main script to run the system
├── attendance.csv        # Log file (auto-created)
├── dataset/              # Folder containing images of known individuals
│   ├── Sarmad/
│   ├── Ammar/
│   └── Umair/
└── README.md             # This file

````

Each subfolder inside `/dataset` is treated as one person's identity. The system will load all face encodings at the start from here.

---

## ⚙️ Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/SyedSarmadShah/face-attendance-system.git
cd face-attendance-system
````

### 2. Install required packages

```bash
pip install opencv-python face_recognition numpy
```

> `face_recognition` may require `cmake` and `dlib` depending on your system. Use `pip install cmake` or check official docs if needed.

---

## ▶️ How to Run

Make sure your webcam is connected, and run:

```bash
python main.py
```

Press `q` to quit the camera window.

---

## 📦 Output

* Recognized faces will be boxed with their names.
* When a known face is detected, their attendance will be marked in `attendance.csv` with the date and time.

---

## ❓ Why Not CNN from Scratch?

This system uses a **pre-trained CNN under the hood**, via the `face_recognition` library. This avoids the need for:

* Large datasets
* Training custom neural networks
* Long processing times

Instead, it offers high accuracy and real-time speed — perfect for lightweight attendance systems.

---

## 📹 Demo

A full demonstration is available here:
🔗 [LinkedIn Post / YouTube Demo Link](https://www.linkedin.com/in/syed-sarmad-shah-699806294/)

---

## 🙌 Credits

Developed by **Syed Sarmad Shah**
Student of Artificial Neural Networks — HITEC University Taxila
Feel free to contribute or fork the project!

---

## 📌 License

This project is open-source and free to use for educational and non-commercial purposes.

```

---

Let me know when you push this — I can generate a clean project description + hashtags for your GitHub or LinkedIn bio too!
```
