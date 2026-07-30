import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from config import Config
from database.connection import db
from database.models import User, Settings, Event, Goal

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def initialize_database():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='alexjohnson').first():
            user = User(
                username='alexjohnson',
                email='alex.johnson@student.edu',
                full_name='Alex Johnson',
                phone='+1 (555) 000-0000',
                field_of_study='Computer Science',
                bio='Passionate about software engineering and machine learning. Currently focusing on building consistent study habits.',
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Add default settings
            settings = Settings(
                user_id=user.id,
                email_notifications=True,
                study_reminders=True,
                weekly_summary=True,
                goal_alerts=True,
                theme='light',
                language='en-US',
                timezone='Mountain Time (MT)'
            )
            db.session.add(settings)
            
            # Add mock events for May 2024
            mock_events = [
                Event(user_id=user.id, title='Algorithmic Study', description='Focusing on sorting and graph search algorithms.', start_time=datetime(2024, 5, 10, 10, 0), end_time=datetime(2024, 5, 10, 12, 0), category='Study Sessions', all_day=False),
                Event(user_id=user.id, title='Data Structures', description='Reviewing Trees, Heaps, and Tries.', start_time=datetime(2024, 5, 15, 13, 0), end_time=datetime(2024, 5, 15, 15, 0), category='Study Sessions', all_day=False),
                Event(user_id=user.id, title='Library Return', description='Return textbook: Introduction to Algorithms.', start_time=datetime(2024, 5, 15, 17, 0), end_time=datetime(2024, 5, 15, 17, 30), category='Reminders', all_day=False),
                Event(user_id=user.id, title='Biology Revision', description='Study session on Genetics and DNA replication.', start_time=datetime(2024, 5, 18, 10, 0), end_time=datetime(2024, 5, 18, 12, 0), category='Study Sessions', all_day=False),
                Event(user_id=user.id, title='Biology Lab', description='Genetics lab assignment submission.', start_time=datetime(2024, 5, 18, 14, 0), end_time=datetime(2024, 5, 18, 16, 0), category='Study Sessions', all_day=False),
                Event(user_id=user.id, title='Database Assignment', description='SQL query optimization homework submission.', start_time=datetime(2024, 5, 20, 23, 59), end_time=datetime(2024, 5, 20, 23, 59), category='Deadlines', all_day=True),
                Event(user_id=user.id, title='DB Project', description='Database design phase 2 documentation.', start_time=datetime(2024, 5, 20, 15, 0), end_time=datetime(2024, 5, 20, 17, 0), category='Deadlines', all_day=False),
                Event(user_id=user.id, title='English Presentation', description='Prepare and deliver presentation on Tech & Society.', start_time=datetime(2024, 5, 22, 14, 30), end_time=datetime(2024, 5, 22, 16, 0), category='Study Sessions', all_day=False),
                Event(user_id=user.id, title='Midterm Exam', description='Computer Systems midterm examination.', start_time=datetime(2024, 5, 25, 9, 0), end_time=datetime(2024, 5, 25, 11, 30), category='Exams', all_day=False),
                Event(user_id=user.id, title='Final Calculus', description='Calculus III exam prep and test.', start_time=datetime(2024, 5, 25, 13, 0), end_time=datetime(2024, 5, 25, 15, 0), category='Exams', all_day=False),
            ]
            db.session.bulk_save_objects(mock_events)
            db.session.commit()

            # Add mock academic goals
            mock_goals = [
                Goal(user_id=user.id, title='Achieve GPA >= 3.8', category='Academic', description='Maintain a strong GPA throughout the semester.', progress=85, status='In Progress'),
                Goal(user_id=user.id, title='Complete Operating Systems Project', category='Academic', description='Finish the semester-long OS project with the team.', progress=50, status='In Progress'),
            ]
            db.session.bulk_save_objects(mock_goals)
            db.session.commit()
        db.session.remove()


if not app.config['IS_VERCEL'] or os.environ.get('INIT_DB_ON_STARTUP') == '1':
    initialize_database()

# --- Auth Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('calendar_view'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('calendar_view'))
        flash('Invalid username or password.', 'danger')
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('calendar_view'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Add default settings
        settings = Settings(
            user_id=user.id,
            email_notifications=True,
            study_reminders=True,
            weekly_summary=True,
            goal_alerts=True,
            theme='light',
            language='en-US',
            timezone='Mountain Time (MT)'
        )
        db.session.add(settings)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('calendar_view'))
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Main Views ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('calendar_view'))
    return redirect(url_for('login'))

@app.route('/calendar')
@login_required
def calendar_view():
    return render_template('calendar/index.html', title='Calendar')

@app.route('/settings')
@login_required
def settings_view():
    return render_template('profile/settings.html', title='Settings')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html', title='Dashboard')

@app.route('/notes')
@login_required
def notes():
    return render_template('notes/index.html', title='Study Note')

@app.route('/notes/create')
@login_required
def notes_create():
    return render_template('notes/create.html', title='New Study Note')

@app.route('/goals')
@login_required
def goals():
    return render_template('goals/index.html', title='Academic Goals')

# --- API Events CRUD ---
@app.route('/api/events', methods=['GET'])
@login_required
def get_events():
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    
    events_query = Event.query.filter_by(user_id=current_user.id)
    
    # Optionally filter by dates if provided by FullCalendar
    if start_str:
        # FullCalendar formats: 'YYYY-MM-DDTHH:mm:ssZ' or similar, we parse ISO
        try:
            start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            events_query = events_query.filter(Event.start_time >= start_dt)
        except ValueError:
            pass
    if end_str:
        try:
            end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            events_query = events_query.filter(Event.end_time <= end_dt)
        except ValueError:
            pass
            
    events = events_query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.get_json() or {}
    if not data.get('title') or not data.get('start') or not data.get('end'):
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        start_time = datetime.fromisoformat(data['start'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(data['end'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
        
    event = Event(
        user_id=current_user.id,
        title=data['title'],
        description=data.get('description'),
        start_time=start_time,
        end_time=end_time,
        category=data.get('category', 'Study Sessions'),
        all_day=data.get('allDay', False)
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 210

@app.route('/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'start' in data:
        try:
            event.start_time = datetime.fromisoformat(data['start'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid start date format'}), 400
    if 'end' in data:
        try:
            event.end_time = datetime.fromisoformat(data['end'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid end date format'}), 400
    if 'category' in data:
        event.category = data['category']
    if 'allDay' in data:
        event.all_day = data['allDay']
        
    db.session.commit()
    return jsonify(event.to_dict())

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'success': True})

# --- API Goals CRUD ---
@app.route('/api/goals', methods=['GET'])
@login_required
def get_goals():
    goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()
    return jsonify([goal.to_dict() for goal in goals])

@app.route('/api/goals', methods=['POST'])
@login_required
def create_goal():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'Goal title is required'}), 400

    target_date = None
    if data.get('targetDate'):
        try:
            target_date = datetime.fromisoformat(data['targetDate']).date()
        except ValueError:
            return jsonify({'error': 'Invalid target date format'}), 400

    try:
        progress = int(data.get('progress', 0))
    except (TypeError, ValueError):
        progress = 0
    progress = max(0, min(100, progress))

    goal = Goal(
        user_id=current_user.id,
        title=data['title'],
        category=data.get('category', 'Academic'),
        description=data.get('description'),
        target_date=target_date,
        progress=progress,
        status='Completed' if progress >= 100 else 'In Progress'
    )
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_dict()), 201

@app.route('/api/goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}

    if 'title' in data:
        goal.title = data['title']
    if 'category' in data:
        goal.category = data['category']
    if 'description' in data:
        goal.description = data['description']
    if 'targetDate' in data:
        if data['targetDate']:
            try:
                goal.target_date = datetime.fromisoformat(data['targetDate']).date()
            except ValueError:
                return jsonify({'error': 'Invalid target date format'}), 400
        else:
            goal.target_date = None
    if 'progress' in data:
        try:
            progress = max(0, min(100, int(data['progress'])))
            goal.progress = progress
            goal.status = 'Completed' if progress >= 100 else 'In Progress'
        except (TypeError, ValueError):
            pass

    db.session.commit()
    return jsonify(goal.to_dict())

@app.route('/api/goals/<int:goal_id>', methods=['DELETE'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'success': True})

# --- API Settings Updates ---
@app.route('/api/settings/profile', methods=['POST'])
@login_required
def update_profile():
    # Regular form submit
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    field_of_study = request.form.get('field_of_study')
    bio = request.form.get('bio')
    
    if not full_name:
        flash('Full Name is required.', 'danger')
        return redirect(url_for('settings_view'))
        
    current_user.full_name = full_name
    current_user.phone = phone
    current_user.field_of_study = field_of_study
    current_user.bio = bio
    
    # Handle Avatar Upload
    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                filename = f"avatar_{current_user.id}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                current_user.profile_pic = filename
            else:
                flash('Invalid image format. JPG, PNG or WEBP only.', 'danger')
                return redirect(url_for('settings_view'))

    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('settings_view'))

@app.route('/api/settings/password', methods=['POST'])
@login_required
def update_password():
    current_pwd = request.form.get('current_password')
    new_pwd = request.form.get('new_password')
    confirm_pwd = request.form.get('confirm_password')
    
    if not current_pwd or not new_pwd or not confirm_pwd:
        flash('All password fields are required.', 'danger')
        return redirect(url_for('settings_view'))
        
    if not current_user.check_password(current_pwd):
        flash('Incorrect current password.', 'danger')
        return redirect(url_for('settings_view'))
        
    if new_pwd != confirm_pwd:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('settings_view'))
        
    if len(new_pwd) < 8:
        flash('New password must be at least 8 characters long.', 'danger')
        return redirect(url_for('settings_view'))
        
    current_user.set_password(new_pwd)
    db.session.commit()
    flash('Password updated successfully!', 'success')
    return redirect(url_for('settings_view'))

@app.route('/api/settings/preferences', methods=['POST'])
@login_required
def update_preferences():
    data = request.get_json() or {}
    
    # Ensure settings object exists
    if not current_user.settings:
        current_user.settings = Settings(user_id=current_user.id)
        db.session.add(current_user.settings)
        
    if 'email_notifications' in data:
        current_user.settings.email_notifications = data['email_notifications']
    if 'study_reminders' in data:
        current_user.settings.study_reminders = data['study_reminders']
    if 'weekly_summary' in data:
        current_user.settings.weekly_summary = data['weekly_summary']
    if 'goal_alerts' in data:
        current_user.settings.goal_alerts = data['goal_alerts']
    if 'theme' in data:
        current_user.settings.theme = data['theme']
    if 'language' in data:
        current_user.settings.language = data['language']
    if 'timezone' in data:
        current_user.settings.timezone = data['timezone']
        
    db.session.commit()
    return jsonify({'success': True, 'theme': current_user.settings.theme})

@app.route('/api/settings/export', methods=['GET'])
@login_required
def export_notes():
    # Return JSON containing mock notes list and calendar events
    events = Event.query.filter_by(user_id=current_user.id).all()
    data = {
        'user': {
            'username': current_user.username,
            'email': current_user.email,
            'full_name': current_user.full_name
        },
        'events': [event.to_dict() for event in events],
        'notes': [
            {
                'id': 1,
                'title': 'Operating Systems Lecture 1',
                'content': 'Notes about kernel vs user mode and process lifecycle.',
                'created_at': '2024-05-12T10:00:00'
            },
            {
                'id': 2,
                'title': 'Database Design Schema',
                'content': 'Notes on ERDs, normalization (1NF, 2NF, 3NF, BCNF) and primary keys.',
                'created_at': '2024-05-18T15:30:00'
            }
        ]
    }
    return jsonify(data)

@app.route('/api/settings/delete-account', methods=['POST'])
@login_required
def delete_account():
    # Remove user details and log out
    user = current_user
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted permanently.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
