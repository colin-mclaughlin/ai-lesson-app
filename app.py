from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union, List, Optional
import logging

# Import our existing lesson generation functions
from prompt_builder import build_grammar_lesson_prompt, build_multi_rule_grammar_lesson_prompt
from openai_client import generate_lesson
from database import LessonDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Coding Cat Lesson Generator API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class LessonRequest(BaseModel):
    grade: Union[int, str]
    subject: str
    topic: str
    questions_per_section: int = 6

# Response model
class LessonResponse(BaseModel):
    lessonText: str
    success: bool = True

# Lesson history models
class LessonSummary(BaseModel):
    id: int
    topics: List[str]
    grade: int
    age: Optional[int]
    date_generated: str

class LessonsListResponse(BaseModel):
    lessons: List[LessonSummary]
    total: int

# Initialize database
db = LessonDatabase()

@app.get("/")
async def root():
    return {"message": "Coding Cat Lesson Generator API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/generate-lesson", response_model=LessonResponse)
async def generate_lesson_endpoint(request: LessonRequest):
    """
    Generate a lesson based on the provided parameters.
    """
    try:
        logger.info(f"Generating lesson for grade {request.grade}, subject {request.subject}, topic {request.topic}")
        
        # Convert grade to int if it's a string
        grade_level = int(request.grade) if isinstance(request.grade, str) else request.grade
        
        # Validate grade level
        if grade_level < 1 or grade_level > 8:
            raise HTTPException(status_code=400, detail="Grade level must be between 1 and 8")
        
        # Validate questions per section
        if request.questions_per_section < 1 or request.questions_per_section > 20:
            raise HTTPException(status_code=400, detail="Questions per section must be between 1 and 20")
        
        # Create lesson configuration
        lesson_config = {
            "grade_level": grade_level,
            "section_a_questions": request.questions_per_section,
            "section_b_questions": request.questions_per_section,
            "section_c_questions": request.questions_per_section,
            "section_d_questions": request.questions_per_section
        }
        
        # For now, we'll focus on single topic lessons
        # In the future, we could split the topic by commas or other delimiters for multi-topic lessons
        topics = [topic.strip() for topic in request.topic.split(',') if topic.strip()]
        
        if not topics:
            raise HTTPException(status_code=400, detail="At least one topic must be provided")
        
        # Generate the prompt based on number of topics
        if len(topics) == 1:
            prompt = build_grammar_lesson_prompt(topics[0], lesson_config)
        else:
            prompt = build_multi_rule_grammar_lesson_prompt(topics, lesson_config)
        
        logger.info("Calling OpenAI API to generate lesson...")
        
        # Generate the lesson using OpenAI
        lesson_text = generate_lesson(prompt)
        
        logger.info("Lesson generated successfully")
        
        # Save lesson to database (optional - you can remove this if you don't want to auto-save)
        try:
            lesson_id = db.save_lesson(topics, grade_level, lesson_text)
            logger.info(f"Lesson saved to database with ID: {lesson_id}")
        except Exception as e:
            logger.warning(f"Failed to save lesson to database: {e}")
            # Don't fail the request if database save fails
        
        return LessonResponse(lessonText=lesson_text)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error generating lesson: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")

@app.get("/api/lessons", response_model=LessonsListResponse)
async def get_lessons_list():
    """
    Get all lessons from the database, ordered by date descending.
    Returns a list of lesson summaries with basic information.
    """
    try:
        logger.info("Fetching all lessons from database")
        lessons = db.list_lessons()
        
        # Convert to response format
        lesson_summaries = [
            LessonSummary(
                id=lesson['id'],
                topics=lesson['topics'],
                grade=lesson['grade'],
                age=lesson['age'],
                date_generated=lesson['date_generated']
            )
            for lesson in lessons
        ]
        
        return LessonsListResponse(
            lessons=lesson_summaries,
            total=len(lesson_summaries)
        )
        
    except Exception as e:
        logger.error(f"Error fetching lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch lessons: {str(e)}")

@app.get("/api/lessons/{lesson_id}")
async def get_lesson_by_id(lesson_id: int):
    """
    Get a specific lesson by ID, including full lesson content.
    Returns 404 if lesson not found.
    """
    try:
        logger.info(f"Fetching lesson with ID: {lesson_id}")
        lesson = db.get_lesson(lesson_id)
        
        if not lesson:
            raise HTTPException(status_code=404, detail=f"Lesson with ID {lesson_id} not found")
        
        return lesson
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error fetching lesson {lesson_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch lesson: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)