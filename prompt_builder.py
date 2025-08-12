def build_grammar_lesson_prompt(rule_title, lesson_config=None):
    if lesson_config is None:
        lesson_config = {
            "grade_level": 4,
            "section_a_questions": 6,
            "section_b_questions": 6,
            "section_c_questions": 6,
            "section_d_questions": 6
        }
    
    grade_level = lesson_config.get("grade_level", 4)
    section_a_count = lesson_config.get("section_a_questions", 6)
    section_b_count = lesson_config.get("section_b_questions", 6)
    section_c_count = lesson_config.get("section_c_questions", 6)
    section_d_count = lesson_config.get("section_d_questions", 6)
    
    return (
        f"You are an expert elementary ELA teacher. Create a reproducible worksheet for Grade {grade_level} students based on the following grammar rule: \"{rule_title}\".\n\n"
        "The worksheet should follow this structure (do NOT copy any real content, generate everything originally):\n\n"
        "1. **Rule Heading**\n"
        "   - Begin with a bold rule title (e.g., 'Rule 1: Kinds of Sentences')\n\n"
        "2. **Rule Explanation**\n"
        "   - Write a short, student-friendly explanation of the rule.\n"
        "   - Include 3–5 clearly formatted examples of the rule in action.\n"
        "   - Use bold to highlight key grammar terms (e.g., **declarative**, **interrogative**).\n\n"
        f"3. **Activity Section A**\n"
        f"   - Include {section_a_count} sentence fragments or items where students must apply the rule (e.g., punctuate, identify sentence type, etc.).\n"
        "   - Add blanks or lines for student writing.\n"
        "   - Include simple instructions at the top.\n\n"
        f"4. **Activity Section B**\n"
        f"   - Have students write {section_b_count} items applying the rule.\n"
        "   - Add lines and labels for each type (e.g., statement, question, command, exclamation).\n\n"
        f"5. **Activity Section C**\n"
        f"   - Include {section_c_count} creative tasks like matching sentences to pictures, rewriting text, or another imaginative grammar-based activity.\n\n"
        f"6. **Activity Section D**\n"
        f"   - Include {section_d_count} higher-order thinking tasks like explaining, matching, error analysis, or 'find the mistake' activities.\n\n"
        f"Make the worksheet engaging, clear, and appropriate for Grade {grade_level}. Do not copy from any real worksheets or books. Generate all content originally, but keep the structure, length, and style similar to the Evan-Moor Grade {grade_level} Grammar & Punctuation worksheets.\n\n"
        "IMPORTANT CONSTRAINTS:\n"
        "Do NOT include any tasks that require pictures, drawings, diagrams, or image generation.\n"
        f"All questions must be directly related to the provided topic: {rule_title}. Do not introduce unrelated subtopics."
    )


def build_multi_rule_grammar_lesson_prompt(rule_titles, lesson_config=None):
    if lesson_config is None:
        lesson_config = {
            "grade_level": 4,
            "section_a_questions": 6,
            "section_b_questions": 6,
            "section_c_questions": 6,
            "section_d_questions": 6
        }
    
    grade_level = lesson_config.get("grade_level", 4)
    section_a_count = lesson_config.get("section_a_questions", 6)
    section_b_count = lesson_config.get("section_b_questions", 6)
    section_c_count = lesson_config.get("section_c_questions", 6)
    section_d_count = lesson_config.get("section_d_questions", 6)
    
    intro = (
        f"You are an expert elementary ELA teacher. Create a comprehensive, multi-part lesson for Grade {grade_level} students covering the following grammar rules. "
        "For each rule, generate a separate lesson section using the structure and style described below. Do NOT copy any real content; generate everything originally.\n\n"
        "For each rule, include:\n"
        "1. A clear, student-friendly explanation of the rule, with at least 2 correct and 2 incorrect examples. For each example, explain why it is correct or incorrect.\n"
        f"2. Activity A: Identification. Provide at least {section_a_count} sentences. At least one should be tricky or ambiguous, and at least one should not fit the rule (students should answer 'none of the above').\n"
        f"3. Activity B: Application. Provide at least {section_b_count} items, mixing fill-in-the-blank, rewrite, and error correction. At least one item must require students to correct a mistake.\n"
        f"4. Activity C: Production. Provide at least {section_c_count} prompts that encourage creativity, such as writing a short story, a dialogue, or a creative writing prompt using the rule.\n"
        f"5. Activity D: Higher-order thinking. Provide at least {section_d_count} items, mixing explain, match, error analysis, and 'find the mistake' tasks.\n"
        "For every activity, provide explicit, student-friendly instructions.\n"
        f"All content must be original, age-appropriate for Grade {grade_level}, and varied.\n\n"
        "IMPORTANT CONSTRAINTS:\n"
        "Do NOT include any tasks that require pictures, drawings, diagrams, or image generation.\n"
        f"All questions must be directly related to the provided topics: {', '.join(rule_titles)}. Do not introduce unrelated subtopics.\n\n"
    )
    sections = []
    for idx, rule in enumerate(rule_titles, 1):
        sections.append(f"## Rule {idx}: {rule}\n")
        sections.append(
            f"**Rule Explanation**\n"
            f"Write a clear, student-friendly explanation of the rule. Provide at least 2 correct and 2 incorrect examples, and for each, explain why it is correct or incorrect.\n\n"
            f"**Activity A: Identification**\n"
            f"Instructions: Read each sentence and identify if it fits the rule. Write the type or 'none of the above' if it does not fit. At least one sentence should be tricky or ambiguous, and at least one should not fit the rule. Provide at least {section_a_count} sentences.\n\n"
            f"**Activity B: Application**\n"
            f"Instructions: Complete each item as directed. Items should include a mix of fill-in-the-blank, rewrite, and error correction. At least one item must require correcting a mistake. Provide at least {section_b_count} items.\n\n"
            f"**Activity C: Production**\n"
            f"Instructions: Use your creativity! Write a short story, a dialogue, or respond to a creative writing prompt using the rule. Provide at least {section_c_count} prompts.\n\n"
            f"**Activity D: Higher-order Thinking**\n"
            f"Instructions: For each item, complete the higher-order thinking task. Items should include a mix of explain, match, error analysis, and 'find the mistake' tasks. Provide at least {section_d_count} items.\n\n"
        )
    return intro + "\n".join(sections) 