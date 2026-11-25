-- ====================================================================
-- CodeSystem PRODUCTION DATABASE SCHEMA (MySQL 8.0+)
-- WCAG 2.2 AA Compliant, Relational, Indexed, Foreign Key Constrained
-- ====================================================================

CREATE DATABASE IF NOT EXISTS codesystem CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE codesystem;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'ROLE_USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_username (username),
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- 2. User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(512),
    level INT NOT NULL DEFAULT 1,
    xp INT NOT NULL DEFAULT 0,
    streak_days INT NOT NULL DEFAULT 0,
    problems_solved INT NOT NULL DEFAULT 0,
    total_learning_minutes INT NOT NULL DEFAULT 0,
    last_active_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_profile_xp (xp DESC),
    INDEX idx_profile_streak (streak_days DESC)
) ENGINE=InnoDB;

-- 3. DSA Topics Table
CREATE TABLE IF NOT EXISTS dsa_topics (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    category ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED') NOT NULL,
    description TEXT NOT NULL,
    real_world_example TEXT,
    time_complexity_best VARCHAR(64),
    time_complexity_average VARCHAR(64),
    time_complexity_worst VARCHAR(64),
    space_complexity VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_topic_category (category)
) ENGINE=InnoDB;

-- 4. Practice Problems Table
CREATE TABLE IF NOT EXISTS practice_problems (
    id VARCHAR(64) PRIMARY KEY,
    topic_id VARCHAR(64) NOT NULL,
    title VARCHAR(128) NOT NULL,
    slug VARCHAR(128) NOT NULL UNIQUE,
    difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL,
    description TEXT NOT NULL,
    constraints_json JSON,
    starter_code_java TEXT,
    starter_code_python TEXT,
    solution_code_java TEXT,
    solution_code_python TEXT,
    time_complexity_optimal VARCHAR(32),
    space_complexity_optimal VARCHAR(32),
    FOREIGN KEY (topic_id) REFERENCES dsa_topics(id) ON DELETE CASCADE,
    INDEX idx_problem_difficulty (difficulty)
) ENGINE=InnoDB;

-- 5. Submissions Table
CREATE TABLE IF NOT EXISTS submissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    problem_id VARCHAR(64) NOT NULL,
    status ENUM('ACCEPTED', 'WRONG_ANSWER', 'TIME_LIMIT_EXCEEDED', 'RUNTIME_ERROR', 'COMPILATION_ERROR') NOT NULL,
    language VARCHAR(20) NOT NULL,
    execution_time_ms INT,
    memory_mb DOUBLE,
    code_submitted TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES practice_problems(id) ON DELETE CASCADE,
    INDEX idx_sub_user_problem (user_id, problem_id)
) ENGINE=InnoDB;

-- 6. Achievements Catalog Table
CREATE TABLE IF NOT EXISTS achievements (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description VARCHAR(255) NOT NULL,
    icon VARCHAR(64) NOT NULL,
    category ENUM('STREAK', 'MASTERY', 'SPEED', 'PRACTICE') NOT NULL,
    required_value INT NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- 7. User Achievements Progress
CREATE TABLE IF NOT EXISTS user_achievements (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    achievement_id VARCHAR(64) NOT NULL,
    progress_percent INT NOT NULL DEFAULT 0,
    unlocked_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_achievement (user_id, achievement_id)
) ENGINE=InnoDB;

-- 8. User Topic Progress
CREATE TABLE IF NOT EXISTS user_topic_progress (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    topic_id VARCHAR(64) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES dsa_topics(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_topic (user_id, topic_id)
) ENGINE=InnoDB;
