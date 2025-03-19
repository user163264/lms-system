"""
Exercise evaluator service for evaluating responses to different types of exercises.
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Evaluation result dataclass
@dataclass
class ExerciseEvaluationResult:
    """Result of evaluating an exercise response"""
    is_correct: bool
    score: int
    feedback: Optional[str] = None
    detailed_results: Optional[Dict[str, Any]] = None


class EvaluationStrategy(Enum):
    """Enum for different evaluation strategies"""
    EXACT_MATCH = "exact_match"
    FUZZY_MATCH = "fuzzy_match"
    CASE_INSENSITIVE = "case_insensitive"
    NUMERIC_RANGE = "numeric_range"
    CONTAINS_KEYWORDS = "contains_keywords"
    PATTERN_MATCH = "pattern_match"


async def evaluate_exercise_response(
    exercise_type: str,
    user_response: Dict[str, Any],
    correct_answers: List[Any],
    alternate_answers: Optional[List[Any]] = None,
    validation_rules: Optional[Dict[str, Any]] = None,
    scoring_mechanism: Optional[Dict[str, Any]] = None,
) -> ExerciseEvaluationResult:
    """
    Evaluate a user's response to an exercise
    
    Args:
        exercise_type: Type of exercise (word_scramble, multiple_choice, etc.)
        user_response: User's response data
        correct_answers: List of correct answers
        alternate_answers: List of alternative acceptable answers
        validation_rules: Rules for validating the response
        scoring_mechanism: Mechanism for scoring the response
        
    Returns:
        ExerciseEvaluationResult with evaluation details
    """
    # Default scoring parameters
    default_scoring = {
        "points_per_correct": 1,
        "correct_points": 1,
        "incorrect_points": 0,
    }
    
    # Combine with provided scoring mechanism or use defaults
    scoring = {**default_scoring, **(scoring_mechanism or {})}
    
    # Select evaluation method based on exercise type
    if exercise_type.lower() == "word_scramble":
        return await evaluate_word_scramble(user_response, correct_answers, alternate_answers, validation_rules, scoring)
    elif exercise_type.lower() == "multiple_choice":
        return await evaluate_multiple_choice(user_response, correct_answers, validation_rules, scoring)
    elif exercise_type.lower() == "fill_blank":
        return await evaluate_fill_blank(user_response, correct_answers, alternate_answers, validation_rules, scoring)
    elif exercise_type.lower() == "true_false":
        return await evaluate_true_false(user_response, correct_answers, scoring)
    elif exercise_type.lower() == "matching_words":
        return await evaluate_matching_words(user_response, correct_answers, validation_rules, scoring)
    elif exercise_type.lower() == "short_answer":
        return await evaluate_short_answer(user_response, correct_answers, alternate_answers, validation_rules, scoring)
    else:
        # For complex evaluation types that might need human review
        return ExerciseEvaluationResult(
            is_correct=False,
            score=0,
            feedback="This exercise type requires manual evaluation.",
            detailed_results={"needs_review": True, "response": user_response}
        )


async def evaluate_word_scramble(
    user_response: Dict[str, Any],
    correct_answers: List[Any],
    alternate_answers: Optional[List[Any]] = None,
    validation_rules: Optional[Dict[str, Any]] = None,
    scoring: Dict[str, Any] = None
) -> ExerciseEvaluationResult:
    """Evaluate a word scramble exercise response"""
    validation = validation_rules or {}
    case_sensitive = validation.get("case_sensitive", False)
    
    user_answer = user_response.get("answer", "")
    
    # Check if answer matches any correct or alternate answer
    is_correct = False
    
    # Process the correct answers based on case sensitivity
    processed_correct_answers = [
        answer if case_sensitive else answer.lower() 
        for answer in correct_answers
    ]
    
    processed_user_answer = user_answer if case_sensitive else user_answer.lower()
    
    # Check against primary correct answers
    if processed_user_answer in processed_correct_answers:
        is_correct = True
    
    # Check against alternate answers if provided
    if not is_correct and alternate_answers:
        processed_alternates = [
            answer if case_sensitive else answer.lower() 
            for answer in alternate_answers
        ]
        if processed_user_answer in processed_alternates:
            is_correct = True
    
    # Calculate score
    score = scoring.get("correct_points", 1) if is_correct else scoring.get("incorrect_points", 0)
    
    # Provide feedback
    feedback = "Correct! Well done." if is_correct else "Incorrect. Try again."
    
    return ExerciseEvaluationResult(
        is_correct=is_correct,
        score=score,
        feedback=feedback,
        detailed_results={"user_answer": user_answer, "expected_answers": correct_answers}
    )


async def evaluate_multiple_choice(
    user_response: Dict[str, Any],
    correct_answers: List[Any],
    validation_rules: Optional[Dict[str, Any]] = None,
    scoring: Dict[str, Any] = None
) -> ExerciseEvaluationResult:
    """Evaluate a multiple choice exercise response"""
    validation = validation_rules or {}
    allow_multiple = validation.get("allow_multiple", False)
    
    user_selections = user_response.get("selected_options", [])
    
    # For single-selection questions
    if not allow_multiple and len(user_selections) > 1:
        return ExerciseEvaluationResult(
            is_correct=False,
            score=0,
            feedback="Please select only one option.",
            detailed_results={"error": "multiple_selections_not_allowed"}
        )
    
    # Convert both to sets for comparison
    user_set = set(user_selections)
    correct_set = set(correct_answers)
    
    # Check if the answer is correct
    is_correct = user_set == correct_set
    
    # Calculate score - for partial credit, we can adjust here
    if is_correct:
        score = scoring.get("correct_points", 1)
    else:
        score = scoring.get("incorrect_points", 0)
        
        # Optional: Partial credit for partially correct answers
        if scoring.get("allow_partial", False) and user_set.intersection(correct_set):
            correct_count = len(user_set.intersection(correct_set))
            total_correct = len(correct_set)
            score = int(scoring.get("correct_points", 1) * (correct_count / total_correct))
    
    # Provide feedback
    if is_correct:
        feedback = "Correct! Well done."
    else:
        feedback = "Incorrect. Please try again."
    
    return ExerciseEvaluationResult(
        is_correct=is_correct,
        score=score,
        feedback=feedback,
        detailed_results={
            "user_selections": user_selections,
            "correct_answers": correct_answers,
            "partially_correct": bool(user_set.intersection(correct_set)) if not is_correct else False
        }
    )


async def evaluate_fill_blank(
    user_response: Dict[str, Any],
    correct_answers: List[Any],
    alternate_answers: Optional[List[Any]] = None,
    validation_rules: Optional[Dict[str, Any]] = None,
    scoring: Dict[str, Any] = None
) -> ExerciseEvaluationResult:
    """Evaluate a fill-in-the-blank exercise response"""
    validation = validation_rules or {}
    case_sensitive = validation.get("case_sensitive", False)
    
    user_answers = user_response.get("answers", {})
    
    # Track correct and incorrect answers
    correct_count = 0
    total_blanks = len(correct_answers)
    results = {}
    
    # Evaluate each blank
    for idx, correct in enumerate(correct_answers):
        # Get user answer for this blank (using string index as key)
        user_answer = user_answers.get(str(idx), "")
        
        # Prepare for comparison
        if not case_sensitive:
            user_answer = user_answer.lower()
            processed_correct = correct.lower()
        else:
            processed_correct = correct
            
        # Check primary answer
        blank_correct = user_answer == processed_correct
        
        # Check alternate answers if available
        if not blank_correct and alternate_answers and idx < len(alternate_answers):
            alt_answers_for_blank = alternate_answers[idx]
            if not isinstance(alt_answers_for_blank, list):
                alt_answers_for_blank = [alt_answers_for_blank]
                
            processed_alternates = [
                alt if case_sensitive else alt.lower() 
                for alt in alt_answers_for_blank
            ]
            
            blank_correct = user_answer in processed_alternates
            
        if blank_correct:
            correct_count += 1
            
        # Record result for this blank
        results[f"blank_{idx}"] = {
            "user_answer": user_answers.get(str(idx), ""),
            "is_correct": blank_correct,
            "expected": correct
        }
    
    # Calculate score
    points_per_correct = scoring.get("points_per_correct", 1)
    score = correct_count * points_per_correct
    
    # Determine overall correctness
    is_correct = correct_count == total_blanks
    
    # Provide feedback
    if is_correct:
        feedback = "All blanks filled correctly. Well done!"
    else:
        feedback = f"You got {correct_count} out of {total_blanks} blanks correct."
    
    return ExerciseEvaluationResult(
        is_correct=is_correct,
        score=score,
        feedback=feedback,
        detailed_results={
            "blank_results": results,
            "correct_count": correct_count,
            "total_blanks": total_blanks
        }
    )


async def evaluate_true_false(
    user_response: Dict[str, Any],
    correct_answers: List[bool],
    scoring: Dict[str, Any] = None
) -> ExerciseEvaluationResult:
    """Evaluate a true/false exercise response"""
    user_answers = user_response.get("answers", [])
    
    # Ensure we have valid boolean values
    try:
        processed_user_answers = [bool(answer) for answer in user_answers]
    except (ValueError, TypeError):
        return ExerciseEvaluationResult(
            is_correct=False,
            score=0,
            feedback="Invalid response format. Please provide boolean values.",
            detailed_results={"error": "invalid_format"}
        )
    
    # Match lengths of answers and questions
    total_questions = len(correct_answers)
    if len(processed_user_answers) != total_questions:
        return ExerciseEvaluationResult(
            is_correct=False,
            score=0,
            feedback=f"Please answer all {total_questions} questions.",
            detailed_results={"error": "incomplete_answers"}
        )
    
    # Calculate correct answers
    results = {}
    correct_count = 0
    
    for idx, (user_answer, correct_answer) in enumerate(zip(processed_user_answers, correct_answers)):
        is_correct = user_answer == correct_answer
        if is_correct:
            correct_count += 1
        
        results[f"question_{idx}"] = {
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        }
    
    # Calculate score
    points_per_correct = scoring.get("points_per_correct", 1)
    score = correct_count * points_per_correct
    
    # Determine overall correctness
    is_perfect = correct_count == total_questions
    
    # Provide feedback
    if is_perfect:
        feedback = "All answers correct!"
    else:
        feedback = f"You got {correct_count} out of {total_questions} correct."
    
    return ExerciseEvaluationResult(
        is_correct=is_perfect,
        score=score,
        feedback=feedback,
        detailed_results={
            "question_results": results,
            "correct_count": correct_count,
            "total_questions": total_questions
        }
    )


async def evaluate_matching_words(
    user_response: Dict[str, Any],
    correct_answers: List[Dict[str, str]],
    validation_rules: Optional[Dict[str, Any]] = None,
    scoring: Dict[str, Any] = None
) -> ExerciseEvaluationResult:
    """Evaluate a matching words exercise response"""
    validation = validation_rules or {}
    case_sensitive = validation.get("case_sensitive", False)
    
    user_matches = user_response.get("matches", {})
    
    # Prepare correct matches dictionary
    correct_matches = {}
    for match in correct_answers:
        if "left" in match and "right" in match:
            correct_matches[match["left"]] = match["right"]
    
    # Track results
    results = {}
    correct_count = 0
    total_matches = len(correct_matches)
    
    # Evaluate each match
    for left, expected_right in correct_matches.items():
        user_right = user_matches.get(left, "")
        
        # Apply case sensitivity rules
        if not case_sensitive:
            processed_expected = expected_right.lower()
            processed_user = user_right.lower()
        else:
            processed_expected = expected_right
            processed_user = user_right
            
        is_correct = processed_user == processed_expected
        
        if is_correct:
            correct_count += 1
            
        results[left] = {
            "user_match": user_right,
            "correct_match": expected_right,
            "is_correct": is_correct
        }
    
    # Calculate score
    points_per_correct = scoring.get("points_per_correct", 1)
    score = correct_count * points_per_correct
    
    # Determine overall correctness
    is_correct = correct_count == total_matches
    
    # Provide feedback
    if is_correct:
        feedback = "All matches are correct. Well done!"
    else:
        feedback = f"You matched {correct_count} out of {total_matches} correctly."
    
    return ExerciseEvaluationResult(
        is_correct=is_correct,
        score=score,
        feedback=feedback,
        detailed_results={
            "match_results": results,
            "correct_count": correct_count,
            "total_matches": total_matches
        }
    )


async def evaluate_short_answer(
    user_response: Dict[str, Any],
    correct_answers: List[str],
    alternate_answers: Optional[List[List[str]]] = None,
    validation_rules: Optional[Dict[str, Any]] = None,
    scoring: Dict[str, Any] = None
) -> ExerciseEvaluationResult:
    """Evaluate a short answer exercise response"""
    validation = validation_rules or {}
    evaluation_strategy = validation.get("strategy", "case_insensitive")
    keyword_match_threshold = validation.get("keyword_match_threshold", 0.7)  # For keyword matching
    
    user_answer = user_response.get("answer", "")
    
    # Default to no match
    is_correct = False
    matched_answer = None
    match_details = {"strategy_used": evaluation_strategy}
    
    # Case-insensitive exact matching
    if evaluation_strategy == "case_insensitive":
        user_lower = user_answer.lower()
        for answer in correct_answers:
            if user_lower == answer.lower():
                is_correct = True
                matched_answer = answer
                break
                
        # Check alternate answers if not correct
        if not is_correct and alternate_answers:
            for alt_group in alternate_answers:
                for alt in alt_group:
                    if user_lower == alt.lower():
                        is_correct = True
                        matched_answer = alt
                        break
                if is_correct:
                    break
    
    # Keyword matching (checks if the answer contains required keywords)
    elif evaluation_strategy == "contains_keywords":
        keywords = set()
        for answer in correct_answers:
            keywords.update(answer.lower().split())
        
        user_words = set(user_answer.lower().split())
        matched_keywords = keywords.intersection(user_words)
        
        # Calculate match percentage
        match_percentage = len(matched_keywords) / len(keywords) if keywords else 0
        is_correct = match_percentage >= keyword_match_threshold
        match_details["keyword_match"] = {
            "matched_keywords": list(matched_keywords),
            "expected_keywords": list(keywords),
            "match_percentage": match_percentage
        }
    
    # Calculate score
    if is_correct:
        score = scoring.get("correct_points", 1)
    else:
        score = scoring.get("incorrect_points", 0)
    
    # Provide feedback
    if is_correct:
        feedback = "Correct! Your answer matches what we were looking for."
    else:
        feedback = "Your answer doesn't match what we were looking for."
    
    return ExerciseEvaluationResult(
        is_correct=is_correct,
        score=score,
        feedback=feedback,
        detailed_results={
            "user_answer": user_answer,
            "matched_answer": matched_answer,
            "match_details": match_details
        }
    ) 