import sqlite3
import os
from datetime import datetime, timezone, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'comment_gen.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_input TEXT NOT NULL,
            language TEXT DEFAULT 'python',
            nlp_comment TEXT,
            alsi_comment TEXT,
            nlp_score REAL,
            alsi_score REAL,
            nlp_bleu REAL,
            alsi_bleu REAL,
            nlp_precision REAL,
            alsi_precision REAL,
            nlp_recall REAL,
            alsi_recall REAL,
            nlp_f1 REAL,
            alsi_f1 REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_submission(data):
    conn = get_db()
    cursor = conn.cursor()
    # Store local IST time (UTC+5:30)
    ist = timezone(timedelta(hours=5, minutes=30))
    local_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO submissions (
            code_input, language, nlp_comment, alsi_comment,
            nlp_score, alsi_score,
            nlp_bleu, alsi_bleu,
            nlp_precision, alsi_precision,
            nlp_recall, alsi_recall,
            nlp_f1, alsi_f1,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['code_input'], data.get('language', 'python'),
        data['nlp_comment'], data['alsi_comment'],
        data['nlp_score'], data['alsi_score'],
        data['nlp_bleu'], data['alsi_bleu'],
        data['nlp_precision'], data['alsi_precision'],
        data['nlp_recall'], data['alsi_recall'],
        data['nlp_f1'], data['alsi_f1'],
        local_time
    ))
    conn.commit()
    submission_id = cursor.lastrowid
    conn.close()
    return submission_id

def get_all_submissions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_submission_by_id(submission_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions WHERE id = ?', (submission_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_submission(submission_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM submissions WHERE id = ?', (submission_id,))
    conn.commit()
    conn.close()

def get_aggregate_metrics():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            COUNT(*) as total_submissions,
            AVG(nlp_score) as avg_nlp_score,
            AVG(alsi_score) as avg_alsi_score,
            AVG(nlp_bleu) as avg_nlp_bleu,
            AVG(alsi_bleu) as avg_alsi_bleu,
            AVG(nlp_precision) as avg_nlp_precision,
            AVG(alsi_precision) as avg_alsi_precision,
            AVG(nlp_recall) as avg_nlp_recall,
            AVG(alsi_recall) as avg_alsi_recall,
            AVG(nlp_f1) as avg_nlp_f1,
            AVG(alsi_f1) as avg_alsi_f1
        FROM submissions
    ''')
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
