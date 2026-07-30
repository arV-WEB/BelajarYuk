-- SQL Schema for BelajarYuk database

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    phone VARCHAR(20),
    field_of_study VARCHAR(128),
    bio TEXT,
    profile_pic VARCHAR(256),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    email_notifications BOOLEAN DEFAULT 1,
    study_reminders BOOLEAN DEFAULT 1,
    weekly_summary BOOLEAN DEFAULT 1,
    goal_alerts BOOLEAN DEFAULT 1,
    theme VARCHAR(10) DEFAULT 'light',
    language VARCHAR(20) DEFAULT 'en-US',
    timezone VARCHAR(50) DEFAULT 'Mountain Time (MT)',
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    category VARCHAR(50) DEFAULT 'Study Sessions',
    all_day BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(128) NOT NULL,
    category VARCHAR(50) DEFAULT 'Academic',
    description TEXT,
    target_date DATE,
    progress INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'In Progress',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
