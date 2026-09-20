# -*- coding: utf-8 -*-
"""
MÓDULO DE BASE DE DATOS (db_manager.py)
Gestión de registros, autenticación y almacenamiento de calificaciones con SQLite3.
"""

import sqlite3

DB_NAME = "english_explorers.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('estudiante', 'docente')),
            grade INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla de Historial de Puntuaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            grade INTEGER NOT NULL,
            unit INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            xp_gained INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Usuario docente por defecto (Credenciales: admin / admin123)
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (username, password, full_name, role, grade)
            VALUES ('admin', 'admin123', 'Profesor Administrador', 'docente', 0)
        ''')
        
    conn.commit()
    conn.close()

def register_user(username, password, full_name, role='estudiante', grade=1):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, full_name, role, grade)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, full_name, role, grade))
        conn.commit()
        conn.close()
        return True, "Registro exitoso."
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya está registrado."

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, full_name, role, grade FROM users
        WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def save_score(user_id, grade, unit, score, total, xp_gained):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scores (user_id, grade, unit, score, total, xp_gained)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, grade, unit, score, total, xp_gained))
    conn.commit()
    conn.close()

def get_student_scores(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT grade, unit, score, total, xp_gained, date FROM scores
        WHERE user_id = ? ORDER BY date DESC
    ''', (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_all_students_progress():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.full_name, u.grade, 
               COALESCE(SUM(s.score), 0) as total_correct,
               COALESCE(SUM(s.total), 0) as total_asked,
               COALESCE(SUM(s.xp_gained), 0) as total_xp,
               COUNT(s.id) as units_completed
        FROM users u
        LEFT JOIN scores s ON u.id = s.user_id
        WHERE u.role = 'estudiante'
        GROUP BY u.id
        ORDER BY total_xp DESC
    ''')
    records = cursor.fetchall()
    conn.close()
    return records