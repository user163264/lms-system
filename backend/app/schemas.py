# /home/ubuntu/lms/backend/app/schemas.py
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# ===== Basic Models =====

class LessonBase(BaseModel):
    title: str
    content: str
    description: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True

# ===== Exercise Models =====

class ExerciseBase(BaseModel):
    lesson_id: int
    exercise_type: str
    question: str
    correct_answer: List[str]
    max_score: Optional[int] = 1
    grading_type: Optional[str] = "auto"
    
    # Optional fields for different exercise types
    options: Optional[List[str]] = None
    max_length: Optional[int] = None
    scrambled_text: Optional[str] = None
    correct_order: Optional[List[str]] = None
    word_bank: Optional[List[str]] = None

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True

# ===== Submission Models =====

class SubmissionBase(BaseModel):
    user_id: int
    exercise_id: int
    user_answer: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    score: int

    class Config:
        orm_mode = True

# ===== Request/Response Models =====

class SubmissionRequest(BaseModel):
    user_id: int
    exercise_id: int
    user_answer: str

class SubmissionResponse(BaseModel):
    message: str
    score: int

class LessonRequest(LessonBase):
    pass

class ExerciseRequest(ExerciseBase):
    pass

# ===== Specialized Exercise Type Models =====

class FillBlankExercise(BaseModel):
    exercise_type: str = "fill_blank"
    question: str
    correct_answer: List[str]
    max_score: int = 1
    grading_type: str = "auto"

class TrueFalseExercise(BaseModel):
    exercise_type: str = "true_false"
    question: str
    correct_answer: List[str]  # Should contain "true" or "false"
    max_score: int = 1
    grading_type: str = "auto"

class MultipleChoiceExercise(BaseModel):
    exercise_type: str = "multiple_choice"
    question: str
    options: List[str]
    correct_answer: List[str]
    max_score: int = 1
    grading_type: str = "auto"

class SummaryExercise(BaseModel):
    exercise_type: str = "long_answer"
    question: str
    max_length: int = 150
    max_score: int = 5
    grading_type: str = "manual"

class SynAntExercise(BaseModel):
    exercise_type: str = "syn_ant"
    question: str
    correct_answer: List[str]
    max_score: int = 1
    grading_type: str = "auto"

class SentenceOrderExercise(BaseModel):
    exercise_type: str = "sentence_reordering"
    question: str
    scrambled_text: str
    correct_order: List[str]
    max_score: int = 1
    grading_type: str = "auto"

class WordMatchExercise(BaseModel):
    exercise_type: str = "matching_words"
    question: str
    word_bank: List[str]
    correct_answer: List[str]
    max_score: int = 3
    grading_type: str = "auto"

class ShortAnswerExercise(BaseModel):
    exercise_type: str = "short_answer"
    question: str
    correct_answer: List[str]
    max_score: int = 1
    grading_type: str = "auto"

class GapTextExercise(BaseModel):
    exercise_type: str = "cloze_test"
    question: str
    word_bank: List[str]
    correct_answer: List[str]
    max_score: int = 2
    grading_type: str = "auto"

class ComprehensionExercise(BaseModel):
    exercise_type: str = "comprehension"
    question: str
    max_length: int = 250
    max_score: int = 5
    grading_type: str = "manual"

# Adding the missing exercise types found in frontend
class WordScrambleExercise(BaseModel):
    exercise_type: str = "word_scramble"
    question: str
    sentence: str
    correct_answer: List[str]
    max_score: int = 1
    grading_type: str = "auto"

class ImageLabelingExercise(BaseModel):
    exercise_type: str = "image_labeling"
    question: str
    image_url: str
    labels: List[str]
    label_points: List[Dict[str, Any]]
    correct_answer: Dict[str, str]
    max_score: int = 1
    grading_type: str = "auto"

# Union type for all exercise types
ExerciseUnion = Union[
    FillBlankExercise,
    TrueFalseExercise,
    MultipleChoiceExercise,
    SummaryExercise,
    SynAntExercise,
    SentenceOrderExercise,
    WordMatchExercise,
    ShortAnswerExercise,
    GapTextExercise,
    ComprehensionExercise,
    WordScrambleExercise,
    ImageLabelingExercise
]

# Template for creating multiple exercises at once
class ExerciseTemplate(BaseModel):
    lesson_id: int
    exercises: List[ExerciseUnion]