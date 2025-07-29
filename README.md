# Coding Cat - AI Grammar Lesson Generator

An AI-powered tool for generating customizable grammar lessons with curriculum-aligned topic suggestions and SQLite database storage.

## Features

- **Curriculum-Aligned Topics**: Pre-loaded suggestions for grades 1-6 based on official curriculum standards
- **Interactive Topic Selection**: Choose from suggested topics or enter custom ones
- **Customizable Lesson Structure**: Adjust the number of questions for each activity section
- **Multi-Topic Support**: Generate lessons covering multiple grammar concepts
- **Grade-Level Customization**: Tailored content for specific grade levels (1-8)
- **Age-Based Override**: Use age instead of grade for more flexible targeting
- **SQLite Database Storage**: Save, retrieve, and manage generated lessons
- **Lesson Management**: List, view, and search saved lessons

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```bash
   # Create a .env file with your API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

## Usage

### Basic Usage

Generate a lesson for specific topics:
```bash
python generate_lesson.py "Nouns" "Verbs"
```

### Interactive Topic Selection

When you specify a grade without topics, the app will show curriculum-aligned suggestions:

```bash
python generate_lesson.py --grade 4
```

This will:
1. Display curriculum-aligned topics for Grade 4
2. Allow you to select topics by number
3. Let you enter custom topics
4. Proceed with lesson generation

### Advanced Customization

```bash
# Customize question counts for each section
python generate_lesson.py "Kinds of Sentences" --grade 3 --section-a-questions 8 --section-b-questions 4

# Use age instead of grade
python generate_lesson.py "Adjectives" --age 10 --section-d-questions 5

# Multiple topics with custom configuration
python generate_lesson.py "Prepositions" "Conjunctions" --grade 5 --section-c-questions 3
```

### Database Operations

#### Saving Lessons
After generating a lesson, you'll be prompted to save it to the database:
```
Do you want to save this lesson? [Y/n]:
```
- Press `Y` or `Enter` to save the lesson
- Press `N` to skip saving

#### Listing Saved Lessons
View all saved lessons with summary information:
```bash
python generate_lesson.py --list
```

Output example:
```
📚 Found 3 saved lesson(s):
================================================================================
ID   Grade  Age  Date Generated        Topics
================================================================================
1    4      N/A  2024-01-15 14:30:22   Nouns, Verbs, Adjectives
2    3      8    2024-01-15 13:45:10   Kinds of Sentences
3    5      N/A  2024-01-15 12:20:05   Prepositions, Conjunctions
```

#### Viewing a Specific Lesson
Display the full content of a saved lesson by its ID:
```bash
python generate_lesson.py --view 5
```

#### Searching Lessons
Search for lessons containing specific keywords in topics, content, or tags:
```bash
python generate_lesson.py --search "nouns"
python generate_lesson.py --search "grade 3"
python generate_lesson.py --search "sentences"
```

## Database Schema

The SQLite database (`lessons.db`) contains a `lessons` table with the following columns:

- **id**: Auto-incrementing primary key
- **topics**: JSON array of lesson topics
- **grade**: Integer grade level (1-8)
- **age**: Integer age level (nullable, 5-14)
- **date_generated**: Timestamp when the lesson was created
- **lesson_text**: Full lesson content
- **tags**: JSON array of optional tags (nullable)

## Curriculum-Aligned Topics

The app includes a `grade_topics.json` file with curriculum-aligned suggestions for grades 1-6:

- **Grade 1**: Capitalization, End Punctuation, Nouns, Verbs, Adjectives, etc.
- **Grade 2**: Common and Proper Nouns, Plural Nouns, Action Verbs, etc.
- **Grade 3**: Kinds of Sentences, Subjects and Predicates, Compound Sentences, etc.
- **Grade 4**: Complete Sentences, Run-on Sentences, Helping Verbs, etc.
- **Grade 5**: Subject-Verb Agreement, Verb Tenses, Perfect Tenses, etc.
- **Grade 6**: Parts of Speech Review, Clause Types, Verbals, etc.

You can edit `grade_topics.json` to add, remove, or modify topics for your specific curriculum needs.

## Lesson Structure

Each generated lesson includes:

1. **Rule Heading**: Clear title and explanation
2. **Rule Explanation**: Student-friendly explanation with examples
3. **Activity A**: Identification exercises
4. **Activity B**: Application exercises
5. **Activity C**: Production/creative exercises
6. **Activity D**: Higher-order thinking exercises

## Testing

Run the test suite to verify functionality:

```bash
python test_curriculum_suggestions.py
```

## File Structure

```
ai-lesson-app/
├── generate_lesson.py          # Main CLI application
├── prompt_builder.py           # Lesson prompt generation
├── openai_client.py           # OpenAI API integration
├── database.py                # SQLite database operations
├── grade_topics.json          # Curriculum-aligned topic suggestions
├── test_curriculum_suggestions.py  # Test suite
├── requirements.txt           # Python dependencies
├── lessons.db                 # SQLite database (created automatically)
└── README.md                 # This file
```

## Examples

### Generate and Save a Lesson
```bash
python generate_lesson.py "Nouns" "Verbs" --grade 3
# After generation, you'll be prompted to save the lesson
```

### View All Saved Lessons
```bash
python generate_lesson.py --list
```

### View a Specific Lesson
```bash
python generate_lesson.py --view 2
```

### Search for Lessons
```bash
python generate_lesson.py --search "adjectives"
```

### Generate Multi-Topic Lesson
```bash
python generate_lesson.py "Nouns" "Verbs" "Adjectives" --grade 3
```

### Custom Lesson with Specific Question Counts
```bash
python generate_lesson.py "Kinds of Sentences" --grade 4 --section-a-questions 10 --section-b-questions 8 --section-c-questions 6 --section-d-questions 4
```

## Notes

- Lessons are saved to `lesson_output.txt` by default
- Saved lessons are stored in `lessons.db` (SQLite database)
- The app gracefully handles missing `grade_topics.json` files
- All content is generated originally (no copying from existing materials)
- Lessons are tailored to the specified grade level and age appropriateness
- Database operations are atomic and include error handling