-- Seed data for BelajarYuk database

-- Default user: Alex Johnson (username: alexjohnson, password: password123)
-- password_hash: pbkdf2:sha256:600000$gNlD5H6eT6qCjZ5s$f02db4f1412ceec035bf40ff26922221297e682cb4ab0167389c922abce6087d
-- Note: It's safer to generate hashes dynamically in Python, but we include it here for reference.
INSERT OR IGNORE INTO users (id, username, email, password_hash, full_name, phone, field_of_study, bio, profile_pic, created_at)
VALUES (1, 'alexjohnson', 'alex.johnson@student.edu', 'scrypt:32768:8:1$jMlhJ75PEx3N8Xj0$3ad5298a0ea1e847c29e1eb1c52d6a5eead9070a7b4582f3efad723bfb3ee7556a3375836a0fb4fdf1dfb1b16e87f87bf3a1be125d0c75cbfe5c7965bead27ca', 'Alex Johnson', '+1 (555) 000-0000', 'Computer Science', 'Passionate about software engineering and machine learning. Currently focusing on building consistent study habits.', NULL, '2024-05-01 08:00:00');

-- Default settings for user 1
INSERT OR IGNORE INTO settings (id, user_id, email_notifications, study_reminders, weekly_summary, goal_alerts, theme, language, timezone)
VALUES (1, 1, 1, 1, 1, 1, 'light', 'en-US', 'Mountain Time (MT)');

-- Sample events for user 1 (May 2024)
-- May 10: Algorithmic Study Session (Study Sessions)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Algorithmic Study', 'Focusing on sorting and graph search algorithms.', '2024-05-10 10:00:00', '2024-05-10 12:00:00', 'Study Sessions', 0);

-- May 15: Data Structures (Study Sessions)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Data Structures', 'Reviewing Trees, Heaps, and Tries.', '2024-05-15 13:00:00', '2024-05-15 15:00:00', 'Study Sessions', 0);

-- May 15: Library Return (Reminders)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Library Return', 'Return textbook: Introduction to Algorithms.', '2024-05-15 17:00:00', '2024-05-15 17:30:00', 'Reminders', 0);

-- May 18: Biology Revision (Study Sessions)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Biology Revision', 'Study session on Genetics and DNA replication.', '2024-05-18 10:00:00', '2024-05-18 12:00:00', 'Study Sessions', 0);

-- May 18: Biology Lab (Study Sessions)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Biology Lab', 'Genetics lab assignment submission.', '2024-05-18 14:00:00', '2024-05-18 16:00:00', 'Study Sessions', 0);

-- May 20: Database Assignment (Deadlines)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Database Assignment', 'SQL query optimization homework submission.', '2024-05-20 23:59:00', '2024-05-20 23:59:00', 'Deadlines', 1);

-- May 20: DB Project (Deadlines)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'DB Project', 'Database design phase 2 documentation.', '2024-05-20 15:00:00', '2024-05-20 17:00:00', 'Deadlines', 0);

-- May 22: English Presentation (Study Sessions)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'English Presentation', 'Prepare and deliver presentation on Tech & Society.', '2024-05-22 14:30:00', '2024-05-22 16:00:00', 'Study Sessions', 0);

-- May 25: Midterm Exam (Exams)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Midterm Exam', 'Computer Systems midterm examination.', '2024-05-25 09:00:00', '2024-05-25 11:30:00', 'Exams', 0);

-- May 25: Final Calculus (Exams)
INSERT OR IGNORE INTO events (user_id, title, description, start_time, end_time, category, all_day)
VALUES (1, 'Final Calculus', 'Calculus III exam prep and test.', '2024-05-25 13:00:00', '2024-05-25 15:00:00', 'Exams', 0);
