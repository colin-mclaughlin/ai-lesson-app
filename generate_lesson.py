import sys
from prompt_builder import build_grammar_lesson_prompt
from openai_client import generate_lesson

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_lesson.py \"your grammar topic or prompt here\"")
        return

    user_topic = " ".join(sys.argv[1:])
    print(f"Building lesson on: {user_topic}")
    prompt = build_grammar_lesson_prompt(user_topic)

    print("Generating lesson from OpenAI...")
    lesson = generate_lesson(prompt)

    print("\nGenerated Lesson:\n")
    print(lesson)

if __name__ == "__main__":
    main() 