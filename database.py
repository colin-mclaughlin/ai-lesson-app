import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class LessonDatabase:
    def __init__(self, db_path: str = "lessons.db"):
        """Initialize the lesson database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the lessons table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topics TEXT NOT NULL,
                    grade INTEGER NOT NULL,
                    age INTEGER,
                    date_generated TIMESTAMP NOT NULL,
                    lesson_text TEXT NOT NULL,
                    tags TEXT
                )
            ''')
            conn.commit()
    
    def save_lesson(self, topics: List[str], grade: int, lesson_text: str, 
                   age: Optional[int] = None, tags: Optional[List[str]] = None) -> int:
        """Save a lesson to the database and return the lesson ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO lessons (topics, grade, age, date_generated, lesson_text, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                json.dumps(topics),
                grade,
                age,
                datetime.now().isoformat(),
                lesson_text,
                json.dumps(tags) if tags else None
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_lesson(self, lesson_id: int) -> Optional[Dict]:
        """Retrieve a lesson by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, topics, grade, age, date_generated, lesson_text, tags
                FROM lessons WHERE id = ?
            ''', (lesson_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'topics': json.loads(row[1]),
                    'grade': row[2],
                    'age': row[3],
                    'date_generated': row[4],
                    'lesson_text': row[5],
                    'tags': json.loads(row[6]) if row[6] else None
                }
            return None
    
    def list_lessons(self) -> List[Dict]:
        """List all lessons with summary information"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, topics, grade, age, date_generated
                FROM lessons
                ORDER BY date_generated DESC
            ''')
            
            lessons = []
            for row in cursor.fetchall():
                lessons.append({
                    'id': row[0],
                    'topics': json.loads(row[1]),
                    'grade': row[2],
                    'age': row[3],
                    'date_generated': row[4]
                })
            return lessons
    
    def search_lessons(self, keyword: str) -> List[Dict]:
        """Search lessons by keyword in topics, lesson text, or tags"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, topics, grade, age, date_generated, lesson_text, tags
                FROM lessons
                WHERE topics LIKE ? OR lesson_text LIKE ? OR tags LIKE ?
                ORDER BY date_generated DESC
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            
            lessons = []
            for row in cursor.fetchall():
                lessons.append({
                    'id': row[0],
                    'topics': json.loads(row[1]),
                    'grade': row[2],
                    'age': row[3],
                    'date_generated': row[4],
                    'lesson_text': row[5],
                    'tags': json.loads(row[6]) if row[6] else None
                })
            return lessons
    
    def delete_lesson(self, lesson_id: int) -> bool:
        """Delete a lesson by ID. Returns True if successful, False if not found."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM lessons WHERE id = ?', (lesson_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_lesson_count(self) -> int:
        """Get the total number of lessons in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM lessons')
            return cursor.fetchone()[0]