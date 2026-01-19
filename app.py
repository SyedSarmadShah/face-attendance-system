"""
Flask Web Application for Face Attendance System with SQLite Database
"""

from flask import Flask, render_template, request, jsonify, redirect, session
from flask_cors import CORS
from models import db, User, Attendance, Dataset
import os
from datetime import datetime, date
import logging
import re
import subprocess
import sys
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'face-attendance-secret-key-2026'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# Database Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f'sqlite:///{os.path.join(DATA_DIR, "attendance.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS Configuration
CORS(app, 
     supports_credentials=True, 
     origins=['http://localhost:5173', 'http://localhost:5174', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174'],
     allow_headers=['Content-Type'],
     methods=['GET', 'POST', 'OPTIONS'])

# Helper Functions
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

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        logger.info("Database initialized")
        
        if not User.query.filter_by(username='sarmad').first():
            demo_user = User(username='sarmad')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            logger.info("Demo user created")

# Routes
@app.route('/')
def index():
    """Home page"""
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
        
        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
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
    
    try:
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"New registration: {username}")
        return jsonify({'success': True, 'message': 'Registration successful! You can now login.'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': f'Registration error: {e}'})

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'username' not in session:
        return redirect('/login')
    
    records = Attendance.query.all()
    dataset_info = get_dataset_info()
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         attendance_records=[r.to_dict() for r in records],
                         dataset_info=dataset_info)

@app.route('/api/attendance')
def api_attendance():
    """API endpoint to get attendance data"""
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    records = Attendance.query.all()
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).all()
    
    stats = {
        'total_records': len(records),
        'today_attendance': len(today_attendance),
        'today_date': today.isoformat()
    }
    
    return jsonify({
        'records': [r.to_dict() for r in records],
        'stats': stats
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint to get system statistics"""
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    records = Attendance.query.all()
    dataset_info = get_dataset_info()
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).all()
    unique_people = db.session.query(func.count(func.distinct(Attendance.name))).scalar()
    
    return jsonify({
        'total_faces_in_dataset': len(dataset_info),
        'total_attendance_records': len(records),
        'unique_people': unique_people or 0,
        'today_attendance': len(today_attendance),
        'dataset_faces': dataset_info
    })

@app.route('/api/analytics', methods=['GET'])
def api_analytics():
    """Advanced analytics endpoint with trends and insights"""
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    from datetime import timedelta
    from sqlalchemy import extract
    
    # Get date range from query params
    days_back = int(request.args.get('days', 30))
    start_date = date.today() - timedelta(days=days_back)
    
    # Daily attendance trend
    daily_query = db.session.query(
        Attendance.date,
        func.count(Attendance.id).label('count')
    ).filter(Attendance.date >= start_date).group_by(Attendance.date).order_by(Attendance.date).all()
    
    daily_trend = [{'date': str(d.date), 'count': d.count} for d in daily_query]
    
    # Attendance by person
    person_query = db.session.query(
        Attendance.name,
        func.count(Attendance.id).label('count')
    ).filter(Attendance.date >= start_date).group_by(Attendance.name).order_by(func.count(Attendance.id).desc()).all()
    
    attendance_by_person = [{'name': p.name, 'count': p.count} for p in person_query]
    
    # Weekly summary (last 4 weeks)
    weekly_data = []
    for week in range(4):
        week_start = date.today() - timedelta(days=(week + 1) * 7)
        week_end = date.today() - timedelta(days=week * 7)
        week_count = Attendance.query.filter(
            Attendance.date >= week_start,
            Attendance.date < week_end
        ).count()
        weekly_data.append({
            'week': f'Week {4-week}',
            'count': week_count,
            'start': str(week_start),
            'end': str(week_end)
        })
    
    # Attendance rate calculation
    total_registered = len(get_dataset_info())
    avg_daily_attendance = len(daily_trend) and sum(d['count'] for d in daily_trend) / len(daily_trend) or 0
    attendance_rate = (avg_daily_attendance / total_registered * 100) if total_registered > 0 else 0
    
    # Peak attendance times (by hour)
    time_query = db.session.query(
        extract('hour', Attendance.time).label('hour'),
        func.count(Attendance.id).label('count')
    ).filter(Attendance.date >= start_date).group_by('hour').order_by('hour').all()
    
    peak_times = [{'hour': int(t.hour), 'count': t.count} for t in time_query]
    
    return jsonify({
        'daily_trend': daily_trend,
        'weekly_summary': weekly_data,
        'attendance_by_person': attendance_by_person,
        'peak_times': peak_times,
        'attendance_rate': round(attendance_rate, 1),
        'total_registered': total_registered,
        'avg_daily_attendance': round(avg_daily_attendance, 1),
        'date_range': {
            'start': str(start_date),
            'end': str(date.today())
        }
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
        user = User.query.filter_by(username=session['username']).first()
        return jsonify({
            'authenticated': True, 
            'username': session['username'],
            'user_id': user.id if user else None
        })
    return jsonify({'authenticated': False}), 401

if __name__ == '__main__':
    init_db()
    print("\n" + "="*70)
    print("🚀 FACE ATTENDANCE SYSTEM - WEB APPLICATION")
    print("="*70)
    print("\n📱 Access the application at: http://localhost:5000")
    print("\n🔐 Features:")
    print("   ✓ Teacher Login/Registration")
    print("   ✓ Real-time attendance dashboard")
    print("   ✓ Attendance statistics and records")
    print("   ✓ SQLite Database Backend ⭐ NEW")
    print("\n💡 Demo Credentials:")
    print("   Username: sarmad")
    print("   Password: demo123")
    print("\n" + "="*70 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)
