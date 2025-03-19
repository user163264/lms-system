"""
Exercise evaluation service for scoring and providing feedback on user responses
"""
from typing import Dict, Any, List, Tuple, Optional
import json
from ..models.exercise import ExerciseTemplate, ExerciseContent
from ..schemas.exercise_schemas import ExerciseTypeEnum


class EvaluationResult:
    """Result of an exercise evaluation"""
    def __init__(self, 
                 score: int, 
                 is_correct: bool, 
                 feedback: str,
                 max_score: int):
        self.score = score
        self.is_correct = is_correct
        self.feedback = feedback
        self.max_score = max_score


class BaseEvaluator:
    """Base class for exercise evaluators"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """
        Evaluate a user response to an exercise
        
        Args:
            exercise_content: The exercise content being evaluated
            template: The exercise template
            user_response: The user's response data
            
        Returns:
            EvaluationResult with score and feedback
        """
        raise NotImplementedError("Evaluator subclasses must implement evaluate method")


class WordScrambleEvaluator(BaseEvaluator):
    """Evaluator for word scramble exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a word scramble response"""
        correct_answers = exercise_content.correct_answers
        user_answers = user_response.get("answer", "")
        
        # Normalize answers for comparison
        normalized_correct = [str(ans).strip().lower() for ans in correct_answers]
        normalized_user = str(user_answers).strip().lower()
        
        is_correct = normalized_user in normalized_correct
        score = exercise_content.difficulty_level if is_correct else 0
        max_score = exercise_content.difficulty_level
        
        feedback = "Correct! Good job." if is_correct else f"Not quite right. The correct answer is: {correct_answers[0]}"
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class MultipleChoiceEvaluator(BaseEvaluator):
    """Evaluator for multiple choice exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a multiple choice response"""
        correct_answers = exercise_content.correct_answers
        user_answer = user_response.get("answer", "")
        
        # Normalize for comparison
        normalized_correct = [str(ans).strip().lower() for ans in correct_answers]
        normalized_user = str(user_answer).strip().lower()
        
        is_correct = normalized_user in normalized_correct
        score = exercise_content.difficulty_level if is_correct else 0
        max_score = exercise_content.difficulty_level
        
        feedback = "Correct! Good job." if is_correct else f"Not quite right. The correct answer is: {correct_answers[0]}"
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class FillBlankEvaluator(BaseEvaluator):
    """Evaluator for fill-in-the-blank exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a fill-in-the-blank response"""
        correct_answers = exercise_content.correct_answers
        alternate_answers = exercise_content.alternate_answers or []
        user_answer = user_response.get("answer", "")
        
        # Combine correct and alternate answers
        all_valid_answers = correct_answers + alternate_answers
        
        # Normalize for comparison
        normalized_valid = [str(ans).strip().lower() for ans in all_valid_answers]
        normalized_user = str(user_answer).strip().lower()
        
        is_correct = normalized_user in normalized_valid
        score = exercise_content.difficulty_level if is_correct else 0
        max_score = exercise_content.difficulty_level
        
        feedback = "Correct! Good job." if is_correct else f"Not quite right. The correct answer is: {correct_answers[0]}"
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class TrueFalseEvaluator(BaseEvaluator):
    """Evaluator for true/false exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a true/false response"""
        correct_answer = str(exercise_content.correct_answers[0]).strip().lower()
        user_answer = str(user_response.get("answer", "")).strip().lower()
        
        is_correct = user_answer == correct_answer
        score = exercise_content.difficulty_level if is_correct else 0
        max_score = exercise_content.difficulty_level
        
        feedback = "Correct! Good job." if is_correct else f"Not quite right. The statement is {correct_answer}."
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class SentenceReorderingEvaluator(BaseEvaluator):
    """Evaluator for sentence reordering exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a sentence reordering response"""
        correct_order = exercise_content.correct_answers
        user_order = user_response.get("answer", [])
        
        # Convert to string for comparison if needed
        if isinstance(correct_order[0], str) and isinstance(user_order[0], str):
            normalized_correct = [str(item).strip().lower() for item in correct_order]
            normalized_user = [str(item).strip().lower() for item in user_order]
        else:
            normalized_correct = correct_order
            normalized_user = user_order
        
        is_correct = normalized_user == normalized_correct
        score = exercise_content.difficulty_level if is_correct else 0
        max_score = exercise_content.difficulty_level
        
        feedback = "Correct! The sentences are in the right order." if is_correct else "Not quite right. Check the order again."
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class MatchingWordsEvaluator(BaseEvaluator):
    """Evaluator for matching words exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a matching words response"""
        correct_matches = exercise_content.correct_answers
        user_matches = user_response.get("answer", {})
        
        # Count correct matches
        correct_count = 0
        total = len(correct_matches)
        
        for key, value in correct_matches.items():
            if key in user_matches and str(user_matches[key]).strip().lower() == str(value).strip().lower():
                correct_count += 1
        
        # Calculate score proportionally
        max_score = exercise_content.difficulty_level
        score = round(max_score * (correct_count / total)) if total > 0 else 0
        is_correct = score == max_score
        
        feedback = f"You matched {correct_count} out of {total} correctly."
        if is_correct:
            feedback = "Perfect! All matches are correct."
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class ShortAnswerEvaluator(BaseEvaluator):
    """Evaluator for short answer exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a short answer response"""
        # For short answers, we check if key terms are present
        correct_answers = exercise_content.correct_answers
        user_answer = str(user_response.get("answer", "")).strip().lower()
        
        # Count how many required terms are present
        present_terms = 0
        for term in correct_answers:
            if str(term).strip().lower() in user_answer:
                present_terms += 1
        
        # Calculate score based on percentage of terms present
        total_terms = len(correct_answers)
        max_score = exercise_content.difficulty_level
        score = round(max_score * (present_terms / total_terms)) if total_terms > 0 else 0
        is_correct = score >= max_score * 0.7  # Consider 70% or more as correct
        
        feedback = f"You included {present_terms} out of {total_terms} key concepts."
        if is_correct:
            feedback = "Good answer! You covered the key points."
        else:
            feedback = f"Your answer could be improved. Make sure to include these key concepts: {', '.join(correct_answers)}"
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class ClozeTestEvaluator(BaseEvaluator):
    """Evaluator for cloze test (gap-filling) exercises"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a cloze test response"""
        correct_answers = exercise_content.correct_answers
        user_answers = user_response.get("answers", [])
        
        # Count correct fills
        correct_count = 0
        for i, ans in enumerate(correct_answers):
            if i < len(user_answers) and str(user_answers[i]).strip().lower() == str(ans).strip().lower():
                correct_count += 1
        
        total = len(correct_answers)
        max_score = exercise_content.difficulty_level
        score = round(max_score * (correct_count / total)) if total > 0 else 0
        is_correct = score >= max_score * 0.7  # Consider 70% or more as correct
        
        feedback = f"You filled {correct_count} out of {total} gaps correctly."
        if is_correct:
            feedback = "Good job! Most of your answers are correct."
        
        return EvaluationResult(score, is_correct, feedback, max_score)


class ManualEvaluator(BaseEvaluator):
    """Placeholder evaluator for exercises requiring manual grading"""
    
    def evaluate(self, 
                exercise_content: ExerciseContent,
                template: ExerciseTemplate,
                user_response: Dict[str, Any]) -> EvaluationResult:
        """Record the response and return a pending result"""
        max_score = exercise_content.difficulty_level
        
        return EvaluationResult(
            score=0, 
            is_correct=False, 
            feedback="Your answer has been submitted and will be reviewed by an instructor.",
            max_score=max_score
        )


# Factory class to get the appropriate evaluator
class EvaluatorFactory:
    """Factory for creating exercise evaluators"""
    
    @staticmethod
    def get_evaluator(exercise_type: str) -> BaseEvaluator:
        """Get the appropriate evaluator for the exercise type"""
        evaluators = {
            ExerciseTypeEnum.WORD_SCRAMBLE: WordScrambleEvaluator(),
            ExerciseTypeEnum.MULTIPLE_CHOICE: MultipleChoiceEvaluator(),
            ExerciseTypeEnum.FILL_BLANK: FillBlankEvaluator(),
            ExerciseTypeEnum.TRUE_FALSE: TrueFalseEvaluator(),
            ExerciseTypeEnum.SENTENCE_REORDERING: SentenceReorderingEvaluator(),
            ExerciseTypeEnum.MATCHING_WORDS: MatchingWordsEvaluator(),
            ExerciseTypeEnum.SHORT_ANSWER: ShortAnswerEvaluator(),
            ExerciseTypeEnum.CLOZE_TEST: ClozeTestEvaluator(),
            
            # These types require manual evaluation
            ExerciseTypeEnum.LONG_ANSWER: ManualEvaluator(),
            ExerciseTypeEnum.COMPREHENSION: ManualEvaluator(),
            ExerciseTypeEnum.SYN_ANT: ShortAnswerEvaluator(),  # Simplification - could have specific evaluator
            ExerciseTypeEnum.IMAGE_LABELING: MatchingWordsEvaluator(),  # Simplification - could have specific evaluator
        }
        
        return evaluators.get(exercise_type, ManualEvaluator())


# Main evaluation function
def evaluate_exercise_response(
    exercise_content: ExerciseContent,
    template: ExerciseTemplate,
    user_response: Dict[str, Any]
) -> EvaluationResult:
    """
    Evaluate a user's response to an exercise
    
    Args:
        exercise_content: The exercise content
        template: The exercise template
        user_response: The user's response data
        
    Returns:
        EvaluationResult with score and feedback
    """
    evaluator = EvaluatorFactory.get_evaluator(template.type)
    return evaluator.evaluate(exercise_content, template, user_response) 