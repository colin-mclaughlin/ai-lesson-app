import sys
import argparse
from prompt_builder import build_grammar_lesson_prompt, build_multi_rule_grammar_lesson_prompt
from openai_client import generate_lesson

def main():
    parser = argparse.ArgumentParser(
        description="Generate customizable grammar lessons using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_lesson.py "Nouns" "Verbs"
  python generate_lesson.py "Kinds of Sentences" --grade 3 --section-a-questions 8
  python generate_lesson.py "Adjectives" "Adverbs" --section-b-questions 4 --section-c-questions 3
  python generate_lesson.py "Prepositions" --age 10 --section-d-questions 5
        """
    )
    
    # Required arguments
    parser.add_argument(
        "topics",
        nargs="+",
        help="Grammar topics to generate lessons for (e.g., 'Nouns' 'Verbs' 'Adjectives')"
    )
    
    # Optional arguments for customization
    parser.add_argument(
        "--grade",
        type=int,
        choices=range(1, 9),
        default=4,
        help="Grade level for the lesson (1-8, default: 4)"
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
    
    args = parser.parse_args()
    
    # Determine grade level (age takes precedence)
    if args.age:
        # Rough age to grade conversion
        grade_level = max(1, min(8, args.age - 5))
    else:
        grade_level = args.grade
    
    # Create lesson configuration
    lesson_config = {
        "grade_level": grade_level,
        "section_a_questions": args.section_a_questions,
        "section_b_questions": args.section_b_questions,
        "section_c_questions": args.section_c_questions,
        "section_d_questions": args.section_d_questions
    }
    
    print(f"Building lessons for: {', '.join(args.topics)}")
    print(f"Grade level: {grade_level}")
    print(f"Section A questions: {args.section_a_questions}")
    print(f"Section B questions: {args.section_b_questions}")
    print(f"Section C questions: {args.section_c_questions}")
    print(f"Section D questions: {args.section_d_questions}")
    
    if len(args.topics) == 1:
        prompt = build_grammar_lesson_prompt(args.topics[0], lesson_config)
    else:
        prompt = build_multi_rule_grammar_lesson_prompt(args.topics, lesson_config)

    print("\nGenerating lesson(s) from OpenAI...")
    lesson = generate_lesson(prompt)

    print("\nGenerated Lesson(s):\n")
    print(lesson)

    # Write output to file
    output_filename = "lesson_output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(lesson)
    print(f"\nLesson(s) saved to {output_filename}")

if __name__ == "__main__":
    main() 