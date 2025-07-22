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
        "1. A clear, student-friendly explanation of the rule, with at least 2 correct and 2 incorrect examples. For each example, explain why it is correct or incorrect.\n"
        "2. Activity A: Identification. Provide at least 6 sentences. At least one should be tricky or ambiguous, and at least one should not fit the rule (students should answer 'none of the above').\n"
        "3. Activity B: Application. Provide at least 6 items, mixing fill-in-the-blank, rewrite, and error correction. At least one item must require students to correct a mistake.\n"
        "4. Activity C: Production. Provide at least 6 prompts that encourage creativity, such as writing a short story, a dialogue, or a creative writing prompt using the rule.\n"
        "5. Activity D: Higher-order thinking. Provide at least 6 items, mixing explain, match, error analysis, and 'find the mistake' tasks.\n"
        "For every activity, provide explicit, student-friendly instructions.\n"
        "All content must be original, age-appropriate, and varied.\n\n"
    )
    sections = []
    for idx, rule in enumerate(rule_titles, 1):
        sections.append(f"## Rule {idx}: {rule}\n")
        sections.append(
            f"**Rule Explanation**\n"
            f"Write a clear, student-friendly explanation of the rule. Provide at least 2 correct and 2 incorrect examples, and for each, explain why it is correct or incorrect.\n\n"
            f"**Activity A: Identification**\n"
            f"Instructions: Read each sentence and identify if it fits the rule. Write the type or 'none of the above' if it does not fit. At least one sentence should be tricky or ambiguous, and at least one should not fit the rule. Provide at least 6 sentences.\n\n"
            f"**Activity B: Application**\n"
            f"Instructions: Complete each item as directed. Items should include a mix of fill-in-the-blank, rewrite, and error correction. At least one item must require correcting a mistake. Provide at least 6 items.\n\n"
            f"**Activity C: Production**\n"
            f"Instructions: Use your creativity! Write a short story, a dialogue, or respond to a creative writing prompt using the rule. Provide at least 6 prompts.\n\n"
            f"**Activity D: Higher-order Thinking**\n"
            f"Instructions: For each item, complete the higher-order thinking task. Items should include a mix of explain, match, error analysis, and 'find the mistake' tasks. Provide at least 6 items.\n\n"
        )
    return intro + "\n".join(sections) 