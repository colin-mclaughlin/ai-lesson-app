import sys
import argparse
import json
import os
from prompt_builder import build_grammar_lesson_prompt, build_multi_rule_grammar_lesson_prompt
from openai_client import generate_lesson
from database import LessonDatabase

def load_grade_topics():
    """Load curriculum-aligned topics for each grade from grade_topics.json"""
    try:
        with open('grade_topics.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: grade_topics.json not found. Curriculum-aligned suggestions will not be available.")
        return {}
    except json.JSONDecodeError:
        print("Warning: grade_topics.json is invalid. Curriculum-aligned suggestions will not be available.")
        return {}

def display_grade_suggestions(grade_topics, grade_level):
    """Display curriculum-aligned topic suggestions for a specific grade"""
    if str(grade_level) not in grade_topics:
        print(f"No curriculum-aligned topics found for grade {grade_level}")
        return []
    
    topics = grade_topics[str(grade_level)]
    print(f"\nCurriculum-aligned topics for Grade {grade_level}:")
    print("=" * 50)
    for i, topic in enumerate(topics, 1):
        print(f"{i:2d}. {topic}")
    print("=" * 50)
    return topics

def get_user_topic_selection(suggested_topics):
    """Get user selection from suggested topics or custom input"""
    while True:
        print("\nOptions:")
        print("1. Select topics by number (e.g., '1 3 5' for topics 1, 3, and 5)")
        print("2. Enter custom topics (e.g., 'Nouns Verbs Adjectives')")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            try:
                numbers = input("Enter topic numbers separated by spaces: ").strip().split()
                selected_topics = []
                for num in numbers:
                    idx = int(num) - 1
                    if 0 <= idx < len(suggested_topics):
                        selected_topics.append(suggested_topics[idx])
                    else:
                        print(f"Invalid topic number: {num}")
                        return None
                return selected_topics
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
                continue
        elif choice == "2":
            custom_topics = input("Enter custom topics separated by spaces: ").strip()
            if custom_topics:
                return custom_topics.split()
            else:
                print("Please enter at least one topic.")
                continue
        elif choice == "3":
            return None
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def prompt_save_lesson(db: LessonDatabase, topics: list, grade_level: int, lesson: str, age: int = None) -> bool:
    """Prompt user to save the lesson and handle the save operation"""
    while True:
        save_choice = input("\nDo you want to save this lesson? [Y/n]: ").strip().lower()
        
        if save_choice in ['', 'y', 'yes']:
            try:
                lesson_id = db.save_lesson(topics, grade_level, lesson, age)
                print(f"✅ Lesson saved successfully with ID: {lesson_id}")
                return True
            except Exception as e:
                print(f"❌ Error saving lesson: {e}")
                return False
        elif save_choice in ['n', 'no']:
            print("Lesson not saved.")
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def list_lessons(db: LessonDatabase):
    """List all saved lessons with summary information"""
    lessons = db.list_lessons()
    
    if not lessons:
        print("No lessons found in the database.")
        return
    
    print(f"\n📚 Found {len(lessons)} saved lesson(s):")
    print("=" * 80)
    print(f"{'ID':<4} {'Grade':<6} {'Age':<4} {'Date Generated':<20} {'Topics'}")
    print("=" * 80)
    
    for lesson in lessons:
        topics_str = ", ".join(lesson['topics'][:3])  # Show first 3 topics
        if len(lesson['topics']) > 3:
            topics_str += "..."
        
        age_str = str(lesson['age']) if lesson['age'] else "N/A"
        date_str = lesson['date_generated'][:19]  # Truncate to remove microseconds
        
        print(f"{lesson['id']:<4} {lesson['grade']:<6} {age_str:<4} {date_str:<20} {topics_str}")

def view_lesson(db: LessonDatabase, lesson_id: int):
    """Display the full content of a saved lesson"""
    lesson = db.get_lesson(lesson_id)
    
    if not lesson:
        print(f"❌ Lesson with ID {lesson_id} not found.")
        return
    
    print(f"\n📖 Lesson #{lesson_id}")
    print("=" * 80)
    print(f"Topics: {', '.join(lesson['topics'])}")
    print(f"Grade: {lesson['grade']}")
    if lesson['age']:
        print(f"Age: {lesson['age']}")
    print(f"Generated: {lesson['date_generated']}")
    if lesson['tags']:
        print(f"Tags: {', '.join(lesson['tags'])}")
    print("=" * 80)
    print("\nContent:")
    print("-" * 40)
    print(lesson['lesson_text'])

def search_lessons(db: LessonDatabase, keyword: str):
    """Search lessons by keyword"""
    lessons = db.search_lessons(keyword)
    
    if not lessons:
        print(f"No lessons found matching '{keyword}'.")
        return
    
    print(f"\n🔍 Found {len(lessons)} lesson(s) matching '{keyword}':")
    print("=" * 80)
    print(f"{'ID':<4} {'Grade':<6} {'Age':<4} {'Date Generated':<20} {'Topics'}")
    print("=" * 80)
    
    for lesson in lessons:
        topics_str = ", ".join(lesson['topics'][:3])  # Show first 3 topics
        if len(lesson['topics']) > 3:
            topics_str += "..."
        
        age_str = str(lesson['age']) if lesson['age'] else "N/A"
        date_str = lesson['date_generated'][:19]  # Truncate to remove microseconds
        
        print(f"{lesson['id']:<4} {lesson['grade']:<6} {age_str:<4} {date_str:<20} {topics_str}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate customizable grammar lessons using AI with curriculum-aligned topic suggestions and SQLite storage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate lessons
  python generate_lesson.py "Nouns" "Verbs"
  python generate_lesson.py "Kinds of Sentences" --grade 3 --section-a-questions 8
  python generate_lesson.py "Adjectives" "Adverbs" --section-b-questions 4 --section-c-questions 3
  python generate_lesson.py "Prepositions" --age 10 --section-d-questions 5
  python generate_lesson.py --grade 4  # Interactive topic selection with curriculum suggestions

  # Database operations
  python generate_lesson.py --list  # List all saved lessons
  python generate_lesson.py --view 5  # View lesson with ID 5
  python generate_lesson.py --search "nouns"  # Search lessons containing "nouns"

Note: When specifying only a grade without topics, the app will display curriculum-aligned 
suggestions from grade_topics.json and allow interactive selection. You can also enter 
custom topics or select from the suggestions by number.
        """
    )
    
    # Make topics optional to enable interactive selection
    parser.add_argument(
        "topics",
        nargs="*",
        help="Grammar topics to generate lessons for (e.g., 'Nouns' 'Verbs' 'Adjectives'). If not provided and grade is specified, interactive topic selection will be available."
    )
    
    # Optional arguments for customization
    parser.add_argument(
        "--grade",
        type=int,
        choices=range(1, 9),
        default=4,
        help="Grade level for the lesson (1-8, default: 4). When specified without topics, enables curriculum-aligned topic suggestions."
    )
    
    parser.add_argument(
        "--age",
        type=int,
        choices=range(5, 15),
        help="Age level for the lesson (5-14, overrides grade if specified)"
    )
    
    # Section question counts
    parser.add_argument(
        "--section-a-questions",
        type=int,
        default=6,
        help="Number of questions for Activity A: Identification (default: 6)"
    )
    
    parser.add_argument(
        "--section-b-questions",
        type=int,
        default=6,
        help="Number of questions for Activity B: Application (default: 6)"
    )
    
    parser.add_argument(
        "--section-c-questions",
        type=int,
        default=6,
        help="Number of questions for Activity C: Production (default: 6)"
    )
    
    parser.add_argument(
        "--section-d-questions",
        type=int,
        default=6,
        help="Number of questions for Activity D: Higher-order Thinking (default: 6)"
    )
    
    # Database operations
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all saved lessons with summary information"
    )
    
    parser.add_argument(
        "--view",
        type=int,
        metavar="LESSON_ID",
        help="View the full content of a saved lesson by its ID"
    )
    
    parser.add_argument(
        "--search",
        type=str,
        metavar="KEYWORD",
        help="Search lessons by keyword in topics, content, or tags"
    )
    
    args = parser.parse_args()
    
    # Initialize database
    db = LessonDatabase()
    
    # Handle database operations first
    if args.list:
        list_lessons(db)
        return
    
    if args.view:
        view_lesson(db, args.view)
        return
    
    if args.search:
        search_lessons(db, args.search)
        return
    
    # Determine grade level (age takes precedence)
    if args.age:
        # Rough age to grade conversion
        grade_level = max(1, min(8, args.age - 5))
    else:
        grade_level = args.grade
    
    # Handle topic selection
    topics = args.topics
    
    # If no topics provided, check if we should show curriculum suggestions
    if not topics:
        # Load curriculum-aligned topics
        grade_topics = load_grade_topics()
        
        if grade_topics:
            print(f"\nNo topics specified. Showing curriculum-aligned suggestions for Grade {grade_level}.")
            suggested_topics = display_grade_suggestions(grade_topics, grade_level)
            
            if suggested_topics:
                selected_topics = get_user_topic_selection(suggested_topics)
                if selected_topics:
                    topics = selected_topics
                else:
                    print("No topics selected. Exiting.")
                    return
            else:
                print("No curriculum suggestions available for this grade. Please specify topics manually.")
                return
        else:
            print("No topics specified and no curriculum suggestions available. Please specify topics manually.")
            return
    
    # Create lesson configuration
    lesson_config = {
        "grade_level": grade_level,
        "section_a_questions": args.section_a_questions,
        "section_b_questions": args.section_b_questions,
        "section_c_questions": args.section_c_questions,
        "section_d_questions": args.section_d_questions
    }
    
    print(f"Building lessons for: {', '.join(topics)}")
    print(f"Grade level: {grade_level}")
    print(f"Section A questions: {args.section_a_questions}")
    print(f"Section B questions: {args.section_b_questions}")
    print(f"Section C questions: {args.section_c_questions}")
    print(f"Section D questions: {args.section_d_questions}")
    
    if len(topics) == 1:
        prompt = build_grammar_lesson_prompt(topics[0], lesson_config)
    else:
        prompt = build_multi_rule_grammar_lesson_prompt(topics, lesson_config)

    print("\nGenerating lesson(s) from OpenAI...")
    lesson = generate_lesson(prompt)

    print("\nGenerated Lesson(s):\n")
    print(lesson)

    # Write output to file
    output_filename = "lesson_output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(lesson)
    print(f"\nLesson(s) saved to {output_filename}")
    
    # Prompt user to save to database
    prompt_save_lesson(db, topics, grade_level, lesson, args.age)

if __name__ == "__main__":
    main() 