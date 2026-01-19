"""
Flask Web Application for Face Attendance System
Provides web-based UI for login, registration, and attendance viewing
"""

from flask import Flask, render_template, request, jsonify, redirect, session
from flask_cors import CORS
import csv
import os
from datetime import datetime
import logging
import bcrypt
import re
import subprocess
import sys

app = Flask(__name__)
app.secret_key = 'face-attendance-secret-key-2026'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set True if served over HTTPS

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')
CREDENTIALS_FILE = os.path.join(DATA_DIR, 'teacher_credentials.csv')
CSV_FILE = os.path.join(DATA_DIR, 'attendance.csv')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS for React frontend (allow localhost on any port for development)
CORS(app, 
     supports_credentials=True, 
     origins=['http://localhost:5173', 'http://localhost:5174', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174'],
     allow_headers=['Content-Type'],
     methods=['GET', 'POST', 'OPTIONS'])

# Helper Functions
def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False

def validate_input(username, password):
    """Validate username and password"""
    if not username or not password:
        return False, "Username and Password cannot be empty"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username must contain only letters, numbers, and underscores"
    return True, "Valid"

def user_exists(username):
    """Check if user already exists"""
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    with open(CREDENTIALS_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) > 0 and row[0] == username:
                return True
    return False

def create_credentials_file():
    """Create credentials file if it doesn't exist"""
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'PasswordHash'])

def create_attendance_file():
    """Create attendance file if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Date', 'Time'])

def get_attendance_records():
    """Get all attendance records"""
    if not os.path.exists(CSV_FILE):
        return []
    
    records = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name']:  # Skip empty rows
                records.append(row)
    return records

def get_dataset_info():
    """Get info about stored faces in dataset"""
    faces = {}
    if not os.path.exists(DATASET_DIR):
        return faces
    
    for person in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, person)
        if os.path.isdir(person_dir):
            image_count = len([f for f in os.listdir(person_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
            faces[person] = image_count
    
    return faces

# Routes
@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in"""
    if 'username' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'})
        
        create_credentials_file()
        
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 2 and row[0] == username and verify_password(password, row[1]):
                        session['username'] = username
                        logger.info(f"Login successful: {username}")
                        return jsonify({'success': True, 'message': 'Login successful'})
        except Exception as e:
            logger.error(f"Login error: {e}")
            return jsonify({'success': False, 'message': f'Login error: {e}'})
        
        logger.warning(f"Failed login attempt: {username}")
        return jsonify({'success': False, 'message': 'Invalid username or password'})
    
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    """Register new teacher"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    valid, message = validate_input(username, password)
    if not valid:
        return jsonify({'success': False, 'message': message})
    
    create_credentials_file()
    
    if user_exists(username):
        return jsonify({'success': False, 'message': 'Username already exists'})
    
    try:
        hashed_pwd = hash_password(password)
        with open(CREDENTIALS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, hashed_pwd])
        logger.info(f"New registration: {username}")
        return jsonify({'success': True, 'message': 'Registration successful! You can now login.'})
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': f'Registration error: {e}'})

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'username' not in session:
        return redirect('/login')
    
    create_attendance_file()
    records = get_attendance_records()
    dataset_info = get_dataset_info()
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         attendance_records=records,
                         dataset_info=dataset_info)

@app.route('/api/attendance')
def api_attendance():
    """API endpoint to get attendance data"""
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    create_attendance_file()
    records = get_attendance_records()
    
    # Calculate statistics
    today = datetime.now().strftime('%Y-%m-%d')
    today_attendance = [r for r in records if r.get('Date') == today]
    
    stats = {
        'total_records': len(records),
        'today_attendance': len(today_attendance),
        'today_date': today
    }
    
    return jsonify({
        'records': records,
        'stats': stats
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint to get system statistics"""
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    create_attendance_file()
    records = get_attendance_records()
    dataset_info = get_dataset_info()
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_attendance = [r for r in records if r.get('Date') == today]
    
    # Count unique people
    unique_people = set(r.get('Name', '') for r in records if r.get('Name'))
    
    return jsonify({
        'total_faces_in_dataset': len(dataset_info),
        'total_attendance_records': len(records),
        'unique_people': len(unique_people),
        'today_attendance': len(today_attendance),
        'dataset_faces': dataset_info
    })


@app.route('/api/start-camera', methods=['POST'])
def api_start_camera():
    """Start face_attendance camera script"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    try:
        camera_script = os.path.join(BASE_DIR, 'face_attendance.py')
        subprocess.Popen([sys.executable, camera_script])
        return jsonify({'success': True, 'message': 'Camera started. A window should appear; press q to quit.'})
    except Exception as e:
        logger.error(f"Failed to start camera: {e}")
        return jsonify({'success': False, 'message': f'Failed to start camera: {e}'})

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    logger.info("User logged out")
    return redirect('/login')


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API logout for React frontend"""
    session.clear()
    logger.info("User logged out (API)")
    return jsonify({'success': True})


@app.route('/api/session', methods=['GET'])
def api_session():
    """Return current session user"""
    if 'username' in session:
        return jsonify({'authenticated': True, 'username': session['username']})
    return jsonify({'authenticated': False}), 401

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 FACE ATTENDANCE SYSTEM - WEB APPLICATION")
    print("="*70)
    print("\n📱 Access the application at: http://localhost:5000")
    print("\n🔐 Features:")
    print("   ✓ Teacher Login/Registration with secure password hashing")
    print("   ✓ Real-time attendance dashboard")
    print("   ✓ Attendance statistics and records")
    print("   ✓ Dataset information display")
    print("\n💡 Demo Credentials:")
    print("   Username: demo_teacher")
    print("   Password: demo_pass_2026")
    print("\n" + "="*70 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)
