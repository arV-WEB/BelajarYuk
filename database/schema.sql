-- QUERY TRUNCATED
-- ============================================================
-- BelajarYuk Database Schema
-- PostgreSQL / Supabase
-- ============================================================
DROP TABLE IF EXISTS user_achievements CASCADE;
DROP TABLE IF EXISTS calendar_events CASCADE;
DROP TABLE IF EXISTS academic_goals CASCADE;
DROP TABLE IF EXISTS study_notes CASCADE;
DROP TABLE IF EXISTS user_settings CASCADE;
DROP TABLE IF EXISTS password_resets CASCADE;
DROP TABLE IF EXISTS achievements CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS users CASCADE;
-- ============================================================
-- TABLE 1: users
-- ============================================================

CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT chk_username
        CHECK (
            char_length(username) BETWEEN 3 AND 50
            AND username !~ '\s'
        ),
    email VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT chk_email
        CHECK (
            email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        ),
    password_hash VARCHAR(255) NOT NULL,

    full_name VARCHAR(100)
        CHECK (
            full_name IS NULL
            OR char_length(trim(full_name)) >= 3
        ),
    profile_photo VARCHAR(255),
    phone_number VARCHAR(20),
    bio TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    deleted_at TIMESTAMP
);

-- ============================================================
-- TABLE 2: subjects
-- ============================================================

CREATE TABLE subjects (
    subject_id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,

    name VARCHAR(100) NOT NULL,
    CONSTRAINT chk_subject_name
        CHECK (char_length(name) >= 2),
    description TEXT,
    color VARCHAR(20),
    icon VARCHAR(100),

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_subjects_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_subjects_user_name
        UNIQUE (user_id, name)
);

-- ============================================================
-- TABLE 3: study_notes
-- ============================================================

CREATE TABLE study_notes (
    note_id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,

    title VARCHAR(150) NOT NULL
    CHECK (char_length(title) >= 3),
    content TEXT,

    duration_minutes INTEGER DEFAULT 0,

    study_date DATE NOT NULL,

    status VARCHAR(20) DEFAULT 'Belum Dimulai',

    is_favorite BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,

    CONSTRAINT fk_study_notes_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_study_notes_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_study_notes_duration
        CHECK (duration_minutes >= 0),

    CONSTRAINT chk_study_notes_status
        CHECK (
            status IN (
                'Belum Dimulai',
                'Sedang Berjalan',
                'Selesai'
            )
        )
);

-- ============================================================
-- TABLE 4: academic_goals
-- ============================================================

CREATE TABLE academic_goals (
    goal_id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,

    title VARCHAR(150) NOT NULL
    CHECK (char_length(title) >= 3),
    description TEXT,

    target_value INTEGER NOT NULL,
    current_value INTEGER DEFAULT 0,

    target_date DATE NOT NULL,

    priority SMALLINT DEFAULT 3,

    status VARCHAR(20) DEFAULT 'Belum Dimulai',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_academic_goals_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_academic_goals_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_academic_goals_target
        CHECK (target_value > 0),

    CONSTRAINT chk_academic_goals_current
        CHECK (current_value >= 0),

    CONSTRAINT chk_academic_goals_progress
        CHECK (current_value <= target_value),

    CONSTRAINT chk_academic_goals_priority
        CHECK (priority BETWEEN 1 AND 5),

    CONSTRAINT chk_academic_goals_status
        CHECK (
            status IN (
                'Belum Dimulai',
                'Sedang Berjalan',
                'Selesai'
            )
        )
);

-- ============================================================
-- TABLE 5: calendar_events
-- ============================================================

CREATE TABLE calendar_events (
    event_id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,

    title VARCHAR(150) NOT NULL,
    CONSTRAINT chk_study_notes_title
        CHECK (char_length(title) >= 3),
    description TEXT,
    event_type VARCHAR(50),
    location VARCHAR(150),

    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,

    reminder_minutes INTEGER DEFAULT 30,

    status VARCHAR(20) DEFAULT 'Terjadwal',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_calendar_events_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_calendar_events_time
        CHECK (end_datetime >= start_datetime),

    CONSTRAINT chk_calendar_events_reminder
        CHECK (reminder_minutes >= 0),

    CONSTRAINT chk_calendar_events_status
        CHECK (
            status IN (
                'Terjadwal',
                'Selesai',
                'Dibatalkan'
            )
        )
);

-- ============================================================
-- TABLE 6: achievements
-- ============================================================

CREATE TABLE achievements (
    achievement_id BIGSERIAL PRIMARY KEY,

    title VARCHAR(100) NOT NULL,
    description TEXT,

    achievement_type VARCHAR(30),

    required_value INTEGER NOT NULL,

    badge_icon VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_achievements_type
        CHECK (
            achievement_type IN (
                'Study',
                'Goal',
                'Calendar',
                'Login'
            )
        ),

    CONSTRAINT chk_achievements_required
        CHECK (required_value >= 0)
);

-- ============================================================
-- TABLE 7: user_achievements
-- ============================================================

CREATE TABLE user_achievements (
    id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,
    achievement_id BIGINT NOT NULL,

    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_achievements_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_achievements_achievement
        FOREIGN KEY (achievement_id)
        REFERENCES achievements(achievement_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_user_achievement
        UNIQUE (user_id, achievement_id)
);

-- ============================================================
-- TABLE 8: user_settings
-- ============================================================

CREATE TABLE user_settings (
    user_id BIGINT PRIMARY KEY,

    theme VARCHAR(10) DEFAULT 'light',

    language VARCHAR(10) DEFAULT 'id',

    timezone VARCHAR(50) DEFAULT 'Asia/Jakarta',

    email_notifications BOOLEAN DEFAULT TRUE,
    study_reminders BOOLEAN DEFAULT TRUE,
    weekly_summary BOOLEAN DEFAULT TRUE,
    goal_alerts BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_settings_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_user_settings_theme
        CHECK (
            theme IN (
                'light',
                'dark'
            )
        ),

    CONSTRAINT chk_user_settings_language
        CHECK (
            language IN (
                'id',
                'en'
            )
        )
);

-- ============================================================
-- TABLE 9: password_resets
-- ============================================================

CREATE TABLE password_resets (
    reset_id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,

    token_hash VARCHAR(255) NOT NULL UNIQUE,

    expires_at TIMESTAMP NOT NULL,

    used_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_password_resets_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_users_username
ON users(username);

CREATE INDEX idx_users_email
ON users(email);

CREATE INDEX idx_subjects_user
ON subjects(user_id);

CREATE INDEX idx_study_notes_user
ON study_notes(user_id);

CREATE INDEX idx_study_notes_subject
ON study_notes(subject_id);

CREATE INDEX idx_study_notes_status
ON study_notes(status);

CREATE INDEX idx_study_notes_date
ON study_notes(study_date);

CREATE INDEX idx_academic_goals_user
ON academic_goals(user_id);

CREATE INDEX idx_academic_goals_subject
ON academic_goals(subject_id);

CREATE INDEX idx_academic_goals_status
ON academic_goals(status);

CREATE INDEX idx_calendar_events_user
ON calendar_events(user_id);

CREATE INDEX idx_calendar_events_start
ON calendar_events(start_datetime);

CREATE INDEX idx_user_achievements_user
ON user_achievements(user_id);

CREATE INDEX idx_password_resets_user
ON password_resets(user_id);

CREATE INDEX idx_password_resets_token
ON password_resets(token_hash);

CREATE INDEX idx_password_resets_expires
ON password_resets(expires_at);

-- ============================================================
-- DEFAULT ACHIEVEMENTS
-- ============================================================

INSERT INTO achievements (
    title,
    description,
    achievement_type,
    required_value,
    badge_icon
)
VALUES
(
    'Langkah Pertama',
    'Login pertama kali.',
    'Login',
    1,
    'bi-door-open'
),
(
    'Rajin Belajar',
    'Menyelesaikan 10 sesi belajar.',
    'Study',
    10,
    'bi-book'
),
(
    'Pemburu Target',
    'Menyelesaikan 5 target akademik.',
    'Goal',
    5,
    'bi-bullseye'
),
(
    'Tepat Waktu',
    'Menyelesaikan 10 jadwal belajar.',
    'Calendar',
    10,
    'bi-calendar-check'
);

-- ============================================================
-- END OF SCHEMA
-- ============================================================
