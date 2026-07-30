-- ============================================
-- Membuat Database (BelajarYuk)
-- ============================================
CREATE DATABASE IF NOT EXISTS db_belajaryuk
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE db_belajaryuk;

-- ============================================
-- Tabel Users (akun mahasiswa/pengguna)
-- ============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    phone VARCHAR(20),
    field_of_study VARCHAR(128),
    bio TEXT,
    profile_pic VARCHAR(256),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Tabel Settings (preferensi tiap user)
-- ============================================
CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    email_notifications BOOLEAN DEFAULT 1,
    study_reminders BOOLEAN DEFAULT 1,
    weekly_summary BOOLEAN DEFAULT 1,
    goal_alerts BOOLEAN DEFAULT 1,
    theme VARCHAR(10) DEFAULT 'light',
    language VARCHAR(20) DEFAULT 'en-US',
    timezone VARCHAR(50) DEFAULT 'Mountain Time (MT)',
    CONSTRAINT fk_settings_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ============================================
-- Tabel Events (jadwal / kalender akademik)
-- ============================================
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    category VARCHAR(50) DEFAULT 'Study Sessions',
    all_day BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_events_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ============================================
-- Tabel Goals (target akademik)
-- ============================================
CREATE TABLE goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(128) NOT NULL,
    category VARCHAR(50) DEFAULT 'Academic',
    description TEXT,
    target_date DATE,
    progress INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'In Progress',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_goals_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

USE db_belajaryuk;

-- ============================================
-- Data Contoh: Users
-- Catatan: password_hash di bawah adalah hash asli (scrypt/Werkzeug)
-- untuk password "password123", jadi akun ini bisa langsung dipakai
-- login lewat aplikasi Flask-nya.
-- ============================================
INSERT INTO users (username, email, password_hash, full_name, phone, field_of_study, bio)
VALUES
('alexjohnson', 'alex.johnson@student.edu',
 'scrypt:32768:8:1$aw9upKvOcVSXvESH$a1ee554338c1cac2399bf9e526a9b37abaaed6df2985359dca095b0deaa1d0d782a1b7f7ee3193265f7b8250b48c61c825d22c528d6d3c5963ce49198f647592',
 'Alex Johnson', '+1 (555) 000-0000', 'Computer Science',
 'Passionate about software engineering and machine learning.');

-- ============================================
-- Data Contoh: Settings
-- ============================================
INSERT INTO settings (user_id, email_notifications, study_reminders, weekly_summary, goal_alerts, theme, language, timezone)
VALUES
(1, 1, 1, 1, 1, 'light', 'en-US', 'Mountain Time (MT)');

-- ============================================
-- Data Contoh: Events
-- ============================================
INSERT INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES
(1, 'Algorithmic Study', 'Focusing on sorting and graph search algorithms.', '2024-05-10 10:00:00', '2024-05-10 12:00:00', 'Study Sessions', 0),
(1, 'Database Assignment', 'SQL query optimization homework submission.', '2024-05-20 23:59:00', '2024-05-20 23:59:00', 'Deadlines', 1),
(1, 'Midterm Exam', 'Computer Systems midterm examination.', '2024-05-25 09:00:00', '2024-05-25 11:30:00', 'Exams', 0);

-- ============================================
-- Data Contoh: Goals
-- ============================================
INSERT INTO goals (user_id, title, category, description, target_date, progress, status)
VALUES
(1, 'Achieve GPA >= 3.8', 'Academic', 'Maintain a strong GPA throughout the semester.', '2024-06-30', 85, 'In Progress'),
(1, 'Complete Operating Systems Project', 'Academic', 'Finish the semester-long OS project with the team.', '2024-05-28', 50, 'In Progress');
