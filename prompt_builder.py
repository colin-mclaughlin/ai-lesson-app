def build_grammar_lesson_prompt(rule_title):
    return (
        f"You are an expert elementary ELA teacher. Create a reproducible worksheet for Grade 4 students based on the following grammar rule: \"{rule_title}\".\n\n"
        "The worksheet should follow this structure (do NOT copy any real content, generate everything originally):\n\n"
        "1. **Rule Heading**\n"
        "   - Begin with a bold rule title (e.g., 'Rule 1: Kinds of Sentences')\n\n"
        "2. **Rule Explanation**\n"
        "   - Write a short, student-friendly explanation of the rule.\n"
        "   - Include 3–5 clearly formatted examples of the rule in action.\n"
        "   - Use bold to highlight key grammar terms (e.g., **declarative**, **interrogative**).\n\n"
        "3. **Activity Section A**\n"
        "   - Include 6–8 sentence fragments or items where students must apply the rule (e.g., punctuate, identify sentence type, etc.).\n"
        "   - Add blanks or lines for student writing.\n"
        "   - Include simple instructions at the top.\n\n"
        "4. **Activity Section B**\n"
        "   - Have students write 1 of each kind of sentence (or whatever applies to the rule).\n"
        "   - Add lines and labels for each type (e.g., statement, question, command, exclamation).\n\n"
        "5. **Activity Section C** (optional but encouraged)\n"
        "   - Bonus creative task like matching sentences to pictures, rewriting text, or another imaginative grammar-based activity.\n\n"
        "Make the worksheet engaging, clear, and appropriate for Grade 4. Do not copy from any real worksheets or books. Generate all content originally, but keep the structure, length, and style similar to the Evan-Moor Grade 4 Grammar & Punctuation worksheets."
    )


def build_multi_rule_grammar_lesson_prompt(rule_titles):
    intro = (
        "You are an expert elementary ELA teacher. Create a comprehensive, multi-part lesson for Grade 4 students covering the following grammar rules. "
        "For each rule, generate a separate lesson section using the structure and style described below. Do NOT copy any real content; generate everything originally.\n\n"
        "For each rule, include:\n"
        "1. A clear, student-friendly explanation of the rule, with at least 4 examples (some correct, some incorrect, and explain why).\n"
        "2. Activity A: Identification (e.g., underline, circle, or highlight the relevant part in each sentence).\n"
        "3. Activity B: Application (e.g., fill in the blank, rewrite sentences, correct errors).\n"
        "4. Activity C: Production (e.g., write your own sentences, short paragraph, or creative task).\n"
        "5. Activity D: Higher-order thinking (e.g., explain why a sentence is correct/incorrect, match sentences to rules, or write questions for given answers).\n"
        "For each activity, provide clear, student-friendly instructions and at least 6 items.\n"
        "Do not include answer keys.\n\n"
        "All content must be original and appropriate for Grade 4.\n\n"
    )
    sections = []
    for idx, rule in enumerate(rule_titles, 1):
        sections.append(f"## Rule {idx}: {rule}\n")
        sections.append(
            f"**Rule Explanation**\n"
            f"Provide a clear, student-friendly explanation of the rule. Include at least 4 examples: some correct, some incorrect, and explain why each is correct or incorrect.\n\n"
            f"**Activity A: Identification**\n"
            f"Provide clear instructions for identifying the relevant part in each sentence (e.g., underline, circle, or highlight). Include at least 6 items.\n\n"
            f"**Activity B: Application**\n"
            f"Provide clear instructions for applying the rule (e.g., fill in the blank, rewrite sentences, correct errors). Include at least 6 items.\n\n"
            f"**Activity C: Production**\n"
            f"Provide clear instructions for students to produce their own sentences, a short paragraph, or a creative task. Include at least 6 prompts.\n\n"
            f"**Activity D: Higher-order Thinking**\n"
            f"Provide clear instructions for a higher-order thinking task (e.g., explain why a sentence is correct/incorrect, match sentences to rules, or write questions for given answers). Include at least 6 items.\n\n"
        )
    return intro + "\n".join(sections) 