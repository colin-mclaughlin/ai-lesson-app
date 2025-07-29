#!/usr/bin/env python3
"""
Test script for curriculum-aligned topic suggestions functionality.
This script tests the loading and display of grade-based topic suggestions.
"""

import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_lesson import load_grade_topics, display_grade_suggestions

def test_grade_topics_loading():
    """Test loading the grade_topics.json file"""
    print("Testing grade_topics.json loading...")
    
    # Test loading the file
    grade_topics = load_grade_topics()
    
    if not grade_topics:
        print("❌ Failed to load grade_topics.json")
        return False
    
    print("✅ Successfully loaded grade_topics.json")
    
    # Check that all expected grades are present
    expected_grades = ["1", "2", "3", "4", "5", "6"]
    for grade in expected_grades:
        if grade not in grade_topics:
            print(f"❌ Missing grade {grade} in grade_topics.json")
            return False
    
    print("✅ All expected grades (1-6) are present")
    
    # Check that each grade has topics
    for grade in expected_grades:
        topics = grade_topics[grade]
        if not topics or not isinstance(topics, list):
            print(f"❌ Grade {grade} has no topics or invalid format")
            return False
        print(f"✅ Grade {grade} has {len(topics)} topics")
    
    return True

def test_display_suggestions():
    """Test displaying suggestions for different grades"""
    print("\nTesting suggestion display...")
    
    grade_topics = load_grade_topics()
    if not grade_topics:
        print("❌ Cannot test display without loaded topics")
        return False
    
    # Test display for grade 3
    print("\nTesting display for Grade 3:")
    topics = display_grade_suggestions(grade_topics, 3)
    
    if not topics:
        print("❌ No topics returned for Grade 3")
        return False
    
    print(f"✅ Successfully displayed {len(topics)} topics for Grade 3")
    
    # Test display for grade 5
    print("\nTesting display for Grade 5:")
    topics = display_grade_suggestions(grade_topics, 5)
    
    if not topics:
        print("❌ No topics returned for Grade 5")
        return False
    
    print(f"✅ Successfully displayed {len(topics)} topics for Grade 5")
    
    return True

def test_invalid_grade():
    """Test handling of invalid grade"""
    print("\nTesting invalid grade handling...")
    
    grade_topics = load_grade_topics()
    if not grade_topics:
        print("❌ Cannot test invalid grade without loaded topics")
        return False
    
    # Test display for non-existent grade
    topics = display_grade_suggestions(grade_topics, 99)
    
    if topics:
        print("❌ Should not return topics for invalid grade")
        return False
    
    print("✅ Correctly handled invalid grade")
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Curriculum-Aligned Topic Suggestions")
    print("=" * 50)
    
    tests = [
        test_grade_topics_loading,
        test_display_suggestions,
        test_invalid_grade
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The curriculum suggestions are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())