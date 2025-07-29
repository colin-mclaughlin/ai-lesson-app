#!/usr/bin/env python3
"""
Test script for the SQLite database functionality
"""

import os
import tempfile
import json
from database import LessonDatabase

def test_database_operations():
    """Test basic database operations"""
    print("🧪 Testing SQLite database functionality...")
    
    # Use a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        # Initialize database
        db = LessonDatabase(db_path)
        print("✅ Database initialized successfully")
        
        # Test saving a lesson
        test_topics = ["Nouns", "Verbs"]
        test_lesson_text = "This is a test lesson about nouns and verbs."
        test_grade = 3
        test_age = 8
        
        lesson_id = db.save_lesson(test_topics, test_grade, test_lesson_text, test_age)
        print(f"✅ Lesson saved with ID: {lesson_id}")
        
        # Test retrieving the lesson
        retrieved_lesson = db.get_lesson(lesson_id)
        if retrieved_lesson:
            print("✅ Lesson retrieved successfully")
            assert retrieved_lesson['topics'] == test_topics
            assert retrieved_lesson['grade'] == test_grade
            assert retrieved_lesson['age'] == test_age
            assert retrieved_lesson['lesson_text'] == test_lesson_text
            print("✅ Lesson data matches saved data")
        else:
            print("❌ Failed to retrieve lesson")
            return False
        
        # Test listing lessons
        lessons = db.list_lessons()
        if len(lessons) == 1:
            print("✅ Lesson listing works correctly")
        else:
            print(f"❌ Expected 1 lesson, found {len(lessons)}")
            return False
        
        # Test searching lessons
        search_results = db.search_lessons("nouns")
        if len(search_results) == 1:
            print("✅ Lesson search works correctly")
        else:
            print(f"❌ Expected 1 search result, found {len(search_results)}")
            return False
        
        # Test lesson count
        count = db.get_lesson_count()
        if count == 1:
            print("✅ Lesson count is correct")
        else:
            print(f"❌ Expected 1 lesson count, got {count}")
            return False
        
        # Test deleting lesson
        if db.delete_lesson(lesson_id):
            print("✅ Lesson deletion works correctly")
        else:
            print("❌ Failed to delete lesson")
            return False
        
        # Verify lesson is deleted
        deleted_lesson = db.get_lesson(lesson_id)
        if deleted_lesson is None:
            print("✅ Lesson deletion verified")
        else:
            print("❌ Lesson still exists after deletion")
            return False
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    finally:
        # Clean up temporary database
        if os.path.exists(db_path):
            os.unlink(db_path)
            print("🧹 Temporary database cleaned up")

def test_database_schema():
    """Test database schema creation"""
    print("\n🔧 Testing database schema...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        db = LessonDatabase(db_path)
        
        # Test that the lessons table exists and has correct structure
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(lessons)")
            columns = cursor.fetchall()
            
            expected_columns = [
                ('id', 'INTEGER', 1, 1, None, 1),
                ('topics', 'TEXT', 1, 0, None, 0),
                ('grade', 'INTEGER', 1, 0, None, 0),
                ('age', 'INTEGER', 0, 0, None, 0),
                ('date_generated', 'TIMESTAMP', 1, 0, None, 0),
                ('lesson_text', 'TEXT', 1, 0, None, 0),
                ('tags', 'TEXT', 0, 0, None, 0)
            ]
            
            for i, (name, type_, notnull, pk, default, cid) in enumerate(columns):
                expected_name, expected_type, expected_notnull, expected_pk, _, _ = expected_columns[i]
                if name == expected_name and type_ == expected_type and notnull == expected_notnull and pk == expected_pk:
                    print(f"✅ Column '{name}' is correct")
                else:
                    print(f"❌ Column '{name}' does not match expected schema")
                    return False
        
        print("✅ Database schema is correct")
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed with error: {e}")
        return False
    
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)

if __name__ == "__main__":
    print("🚀 Starting database tests...\n")
    
    schema_test = test_database_schema()
    operations_test = test_database_operations()
    
    if schema_test and operations_test:
        print("\n🎉 All tests passed! Database functionality is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        exit(1)