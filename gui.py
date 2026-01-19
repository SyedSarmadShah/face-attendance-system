import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import csv
import subprocess
import sys
import logging
import re

# Try to import bcrypt, fallback to hashlib if not available
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    import hashlib
    BCRYPT_AVAILABLE = False

# Configuration
BG_IMAGE = 'gui_page.jpeg'
USER_ICON = 'user.png'
LOCK_ICON = 'lock.png'
CSV_FILE = 'attendance.csv'
CREDENTIALS_FILE = 'teacher_credentials.csv'

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash password using bcrypt or fallback to SHA256"""
    if BCRYPT_AVAILABLE:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    else:
        return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    if BCRYPT_AVAILABLE:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    else:
        return hashlib.sha256(password.encode()).hexdigest() == hashed

def validate_input(username, password):
    """Validate username and password input"""
    if not username or not password:
        messagebox.showerror("Validation Error", "Username and Password cannot be empty.")
        return False
    if len(username) < 3:
        messagebox.showerror("Validation Error", "Username must be at least 3 characters.")
        return False
    if len(password) < 4:
        messagebox.showerror("Validation Error", "Password must be at least 4 characters.")
        return False
    # Basic alphanumeric validation for username
    if not re.match("^[a-zA-Z0-9_]+$", username):
        messagebox.showerror("Validation Error", "Username must contain only letters, numbers, and underscores.")
        return False
    return True

def register_teacher(username, password):
    try:
        if not validate_input(username, password):
            return False
            
        if not os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Username', 'PasswordHash'])

        with open(CREDENTIALS_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) > 0 and row[0] == username:
                    messagebox.showerror("Error", "Username already exists.")
                    return False

        hashed_pwd = hash_password(password)
        with open(CREDENTIALS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, hashed_pwd])
        
        logger.info(f"Teacher registered: {username}")
        return True
    except Exception as e:
        logger.error(f"Registration error: {e}")
        messagebox.showerror("Error", f"Registration failed: {e}")
        return False

def verify_login(username, password):
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            return False
        with open(CREDENTIALS_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2 and row[0] == username:
                    return verify_password(password, row[1])
        return False
    except Exception as e:
        logger.error(f"Login verification error: {e}")
        return False

def open_file_platform(filepath):
    """Open file using platform-specific command"""
    try:
        if sys.platform == 'win32':
            os.startfile(filepath)
        elif sys.platform == 'darwin':  # macOS
            subprocess.Popen(['open', filepath])
        else:  # Linux and others
            subprocess.Popen(['xdg-open', filepath])
    except Exception as e:
        logger.error(f"Error opening file: {e}")
        messagebox.showerror("Error", f"Failed to open file: {e}")


class FaceTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceTrack - Teacher Login")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Load images safely with fallback colors
        self.bg_img = None
        self.user_icon = None
        self.lock_icon = None
        
        try:
            if os.path.exists(BG_IMAGE):
                self.bg_img = ImageTk.PhotoImage(Image.open(BG_IMAGE).resize((800, 500)))
            if os.path.exists(USER_ICON):
                self.user_icon = ImageTk.PhotoImage(Image.open(USER_ICON).resize((25, 25)))
            if os.path.exists(LOCK_ICON):
                self.lock_icon = ImageTk.PhotoImage(Image.open(LOCK_ICON).resize((25, 25)))
        except Exception as e:
            logger.warning(f"Could not load images: {e}")
            messagebox.showwarning("Warning", f"Some images could not be loaded. Using default interface.\n{e}")

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        # Background image or color fallback
        if self.bg_img:
            bg_label = tk.Label(self.root, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            bg_label = tk.Label(self.root, bg="#f0f0f0")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Teacher Login", font=("Helvetica", 20, "bold"), bg="white", fg="black").place(x=200, y=100)

        # Username field with icon or placeholder
        if self.user_icon:
            tk.Label(self.root, image=self.user_icon, bg="white").place(x=150, y=160)
        else:
            tk.Label(self.root, text="👤", font=("Helvetica", 16), bg="white").place(x=155, y=160)
        
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.place(x=190, y=160, width=250)

        # Password field with icon or placeholder
        if self.lock_icon:
            tk.Label(self.root, image=self.lock_icon, bg="white").place(x=150, y=210)
        else:
            tk.Label(self.root, text="🔒", font=("Helvetica", 16), bg="white").place(x=155, y=210)
        
        self.password_entry = tk.Entry(self.root, show='*', font=("Arial", 14))
        self.password_entry.place(x=190, y=210, width=250)

        tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12), bg="#4CAF50", fg="white").place(x=190, y=260, width=100)
        tk.Button(self.root, text="Register", command=self.register, font=("Arial", 12), bg="#2196F3", fg="white").place(x=340, y=260, width=100)

    def create_dashboard(self, username):
        self.clear_screen()

        if self.bg_img:
            bg_label = tk.Label(self.root, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            bg_label = tk.Label(self.root, bg="#f0f0f0")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text=f"Welcome, {username}", font=("Helvetica", 20, "bold"), bg="white", fg="black").pack(pady=20)

        tk.Button(self.root, text="📷 Open Camera", command=self.open_camera, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="📁 Open Attendance CSV", command=self.open_csv, font=("Arial", 14), bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="🚪 Logout", command=self.create_login_screen, font=("Arial", 14), bg="#f44336", fg="white").pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if verify_login(username, password):
            logger.info(f"Login successful: {username}")
            self.create_dashboard(username)
        else:
            logger.warning(f"Failed login attempt for: {username}")
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if register_teacher(username, password):
            messagebox.showinfo("Registered", "Registration successful. You can now log in.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_camera(self):
        try:
            logger.info("Opening camera application...")
            subprocess.Popen([sys.executable, "face_attendance.py"])
        except Exception as e:
            logger.error(f"Failed to open camera: {e}")
            messagebox.showerror("Error", f"Failed to open camera: {e}")

    def open_csv(self):
        try:
            if os.path.exists(CSV_FILE):
                open_file_platform(CSV_FILE)
                logger.info("Opened attendance CSV file")
            else:
                messagebox.showwarning("Warning", "Attendance CSV file not found.")
        except Exception as e:
            logger.error(f"Error opening CSV: {e}")
            messagebox.showerror("Error", f"Failed to open CSV: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceTrackApp(root)
    root.mainloop()
