import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import csv
import subprocess


BG_IMAGE = 'gui_page.jpeg'
USER_ICON = 'user.png'
LOCK_ICON = 'lock.png'
CSV_FILE = 'attendance.csv'
CREDENTIALS_FILE = 'teacher_credentials.csv'


def register_teacher(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Password'])

    with open(CREDENTIALS_FILE, 'r') as f:
        existing = [line.split(',')[0] for line in f.readlines()[1:]]

    if username in existing:
        messagebox.showerror("Error", "Username already exists.")
        return False

    with open(CREDENTIALS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])
    return True


def verify_login(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    with open(CREDENTIALS_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader) 
        for user, pwd in reader:
            if user == username and pwd == password:
                return True
    return False


class FaceTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceTrack - Teacher Login")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        self.bg_img = ImageTk.PhotoImage(Image.open(BG_IMAGE).resize((800, 500)))
        self.user_icon = ImageTk.PhotoImage(Image.open(USER_ICON).resize((25, 25)))
        self.lock_icon = ImageTk.PhotoImage(Image.open(LOCK_ICON).resize((25, 25)))

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        bg_label = tk.Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Teacher Login", font=("Helvetica", 20, "bold"), bg="white", fg="black").place(x=200, y=100)

      
        tk.Label(self.root, image=self.user_icon, bg="white").place(x=150, y=160)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.place(x=190, y=160, width=250)

       
        tk.Label(self.root, image=self.lock_icon, bg="white").place(x=150, y=210)
        self.password_entry = tk.Entry(self.root, show='*', font=("Arial", 14))
        self.password_entry.place(x=190, y=210, width=250)

        tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12), bg="#4CAF50", fg="white").place(x=190, y=260, width=100)
        tk.Button(self.root, text="Register", command=self.register, font=("Arial", 12), bg="#2196F3", fg="white").place(x=340, y=260, width=100)

    def create_dashboard(self, username):
        self.clear_screen()

        bg_label = tk.Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text=f"Welcome, {username}", font=("Helvetica", 20, "bold"), bg="white", fg="black").pack(pady=20)

        tk.Button(self.root, text="📷 Open Camera", command=self.open_camera, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="📁 Open Attendance CSV", command=self.open_csv, font=("Arial", 14), bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="🚪 Logout", command=self.create_login_screen, font=("Arial", 14), bg="#f44336", fg="white").pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if verify_login(username, password):
            self.create_dashboard(username)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if register_teacher(username, password):
                messagebox.showinfo("Registered", "Registration successful. You can now log in.")
        else:
            messagebox.showerror("Error", "Username and Password cannot be empty.")

    def open_camera(self):
        try:
            subprocess.Popen(["python", "face_attendance.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open camera: {e}")

    def open_csv(self):
        if os.path.exists(CSV_FILE):
            os.startfile(CSV_FILE)
        else:
            messagebox.showwarning("Warning", "Attendance CSV file not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceTrackApp(root)
    root.mainloop()
