import sys
from prompt_builder import build_grammar_lesson_prompt, build_multi_rule_grammar_lesson_prompt
from openai_client import generate_lesson

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_lesson.py \"grammar topic 1\" \"grammar topic 2\" ...")
        return

    rule_titles = sys.argv[1:]
    print(f"Building lessons for: {', '.join(rule_titles)}")
    if len(rule_titles) == 1:
        prompt = build_grammar_lesson_prompt(rule_titles[0])
    else:
        prompt = build_multi_rule_grammar_lesson_prompt(rule_titles)

    print("Generating lesson(s) from OpenAI...")
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