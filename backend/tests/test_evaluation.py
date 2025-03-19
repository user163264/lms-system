import pytest
import asyncio
from typing import Dict, Any

from app.services.exercise_evaluator import evaluate_exercise_response
from app.schemas.exercise_schemas import ExerciseTypeEnum


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_multiple_choice_evaluation():
    """Test evaluation of multiple choice exercises"""
    # Single selection, correct answer
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.MULTIPLE_CHOICE.value,
        user_response={"selected_options": ["A"]},
        correct_answers=["A"],
        validation_rules={"allow_multiple": False},
        scoring_mechanism={"correct_points": 5, "incorrect_points": 0}
    )
    assert result.is_correct is True
    assert result.score == 5
    
    # Single selection, incorrect answer
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.MULTIPLE_CHOICE.value,
        user_response={"selected_options": ["B"]},
        correct_answers=["A"],
        validation_rules={"allow_multiple": False},
        scoring_mechanism={"correct_points": 5, "incorrect_points": 0}
    )
    assert result.is_correct is False
    assert result.score == 0
    
    # Multiple selection, all correct
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.MULTIPLE_CHOICE.value,
        user_response={"selected_options": ["A", "C"]},
        correct_answers=["A", "C"],
        validation_rules={"allow_multiple": True},
        scoring_mechanism={"correct_points": 5, "incorrect_points": 0}
    )
    assert result.is_correct is True
    assert result.score == 5
    
    # Multiple selection, partial correct with partial credit
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.MULTIPLE_CHOICE.value,
        user_response={"selected_options": ["A", "B"]},
        correct_answers=["A", "C"],
        validation_rules={"allow_multiple": True},
        scoring_mechanism={"correct_points": 10, "incorrect_points": 0, "allow_partial": True}
    )
    assert result.is_correct is False
    assert result.score == 5  # Half credit for getting one correct


@pytest.mark.asyncio
async def test_word_scramble_evaluation():
    """Test evaluation of word scramble exercises"""
    # Correct answer
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.WORD_SCRAMBLE.value,
        user_response={"answer": "python"},
        correct_answers=["python"],
        validation_rules={"case_sensitive": False}
    )
    assert result.is_correct is True
    assert result.score > 0
    
    # Correct answer with different case
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.WORD_SCRAMBLE.value,
        user_response={"answer": "PYTHON"},
        correct_answers=["python"],
        validation_rules={"case_sensitive": False}
    )
    assert result.is_correct is True
    
    # Case-sensitive comparison
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.WORD_SCRAMBLE.value,
        user_response={"answer": "PYTHON"},
        correct_answers=["python"],
        validation_rules={"case_sensitive": True}
    )
    assert result.is_correct is False
    
    # Incorrect answer
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.WORD_SCRAMBLE.value,
        user_response={"answer": "ruby"},
        correct_answers=["python"],
        validation_rules={"case_sensitive": False}
    )
    assert result.is_correct is False
    assert result.score == 0


@pytest.mark.asyncio
async def test_fill_blank_evaluation():
    """Test evaluation of fill-in-the-blank exercises"""
    # Correct answer
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.FILL_BLANK.value,
        user_response={"answers": ["Paris", "London"]},
        correct_answers=["Paris", "London"],
        alternate_answers=[["paris", "PARIS"], ["london", "LONDON"]],
        validation_rules={"case_sensitive": False}
    )
    assert result.is_correct is True
    assert result.score > 0
    
    # Partial correct
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.FILL_BLANK.value,
        user_response={"answers": ["Paris", "Berlin"]},
        correct_answers=["Paris", "London"],
        alternate_answers=[["paris", "PARIS"], ["london", "LONDON"]],
        validation_rules={"case_sensitive": False},
        scoring_mechanism={"points_per_correct": 1}
    )
    assert result.is_correct is False
    assert result.score == 1
    
    # All incorrect
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.FILL_BLANK.value,
        user_response={"answers": ["Berlin", "Madrid"]},
        correct_answers=["Paris", "London"],
        alternate_answers=[["paris", "PARIS"], ["london", "LONDON"]],
        validation_rules={"case_sensitive": False}
    )
    assert result.is_correct is False
    assert result.score == 0


@pytest.mark.asyncio
async def test_matching_words_evaluation():
    """Test evaluation of matching words exercises"""
    # All correct matches
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.MATCHING_WORDS.value,
        user_response={"matches": {"France": "Paris", "UK": "London"}},
        correct_answers=[{"left": "France", "right": "Paris"}, {"left": "UK", "right": "London"}],
        validation_rules={"case_sensitive": False}
    )
    assert result.is_correct is True
    assert result.score > 0
    
    # Partial matches
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.MATCHING_WORDS.value,
        user_response={"matches": {"France": "Paris", "UK": "Berlin"}},
        correct_answers=[{"left": "France", "right": "Paris"}, {"left": "UK", "right": "London"}],
        validation_rules={"case_sensitive": False},
        scoring_mechanism={"points_per_correct": 1}
    )
    assert result.is_correct is False
    assert result.score == 1


@pytest.mark.asyncio
async def test_short_answer_evaluation():
    """Test evaluation of short answer exercises"""
    # Contains all key terms
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.SHORT_ANSWER.value,
        user_response={"answer": "Python is a high-level programming language with dynamic typing."},
        correct_answers=["Python", "high-level", "programming", "dynamic"],
        validation_rules={"min_required_terms": 3}
    )
    assert result.is_correct is True
    assert result.score > 0
    
    # Contains some key terms
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.SHORT_ANSWER.value,
        user_response={"answer": "Python is easy to learn."},
        correct_answers=["Python", "high-level", "programming", "dynamic"],
        validation_rules={"min_required_terms": 3}
    )
    assert result.is_correct is False
    
    # Contains minimum required terms
    result = await evaluate_exercise_response(
        exercise_type=ExerciseTypeEnum.SHORT_ANSWER.value,
        user_response={"answer": "Python is a high-level language."},
        correct_answers=["Python", "high-level", "programming", "dynamic"],
        validation_rules={"min_required_terms": 2},
        scoring_mechanism={"partial_credit": True}
    )
    assert result.is_correct is True  # Passes with just 2 terms 