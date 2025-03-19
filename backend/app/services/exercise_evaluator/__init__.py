"""
Exercise evaluator module for evaluating different types of exercise responses.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    """Result of exercise evaluation"""
    score: float
    max_score: float
    feedback: Optional[str] = None
    is_correct: bool
    details: Optional[Dict[str, Any]] = None

async def evaluate_exercise_response(exercise_type: str, user_response: str, 
                                    correct_answers: List[str], 
                                    evaluation_params: Optional[Dict[str, Any]] = None) -> EvaluationResult:
    """
    Evaluate a user response to an exercise
    
    Args:
        exercise_type: Type of exercise (multiple_choice, fill_blank, etc.)
        user_response: User's answer as string
        correct_answers: List of possible correct answers
        evaluation_params: Optional parameters for evaluation
        
    Returns:
        EvaluationResult with score and feedback
    """
    if not evaluation_params:
        evaluation_params = {}
    
    max_score = evaluation_params.get('max_score', 1.0)
    
    # Simple exact match for now - can be extended with more sophisticated evaluation
    normalized_user_response = user_response.strip().lower()
    normalized_correct_answers = [a.strip().lower() for a in correct_answers]
    
    is_correct = normalized_user_response in normalized_correct_answers
    score = max_score if is_correct else 0.0
    
    feedback = "Correct!" if is_correct else "Incorrect. Try again."
    
    return EvaluationResult(
        score=score,
        max_score=max_score,
        feedback=feedback,
        is_correct=is_correct,
        details={"matched": is_correct}
    ) 