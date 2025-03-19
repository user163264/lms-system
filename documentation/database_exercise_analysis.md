# Database Schema Analysis for Exercise Types

## Overview

This document analyzes the current database schema for exercises in the LMS system and assesses whether it properly supports all 10 exercise types identified in the [Exercise Types](./exercise_types.md) documentation.

## Current Database Schema

### Exercise Table Structure

```sql
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id),
    exercise_type VARCHAR NOT NULL,
    question TEXT NOT NULL,
    options JSON,
    correct_answer JSON NOT NULL,
    max_score INTEGER,
    grading_type VARCHAR
)
```

### Exercise Base Model (SQLAlchemy)

```python
class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    exercise_type = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)
    correct_answer = Column(JSON, nullable=False)
    max_score = Column(Integer, default=1)
    grading_type = Column(String, default="auto")
```

### API Schema Models

The backend defines specialized Pydantic models for each exercise type:

1. `FillBlankExercise` - fill_blank
2. `TrueFalseExercise` - true_false
3. `MultipleChoiceExercise` - multiple_choice
4. `SummaryExercise` - summary
5. `SynAntExercise` - syn_ant
6. `SentenceOrderExercise` - sentence_order
7. `WordMatchExercise` - word_match
8. `ShortAnswerExercise` - short_answer
9. `GapTextExercise` - gap_text
10. `ComprehensionExercise` - comprehension

## Analysis of Database Support for Exercise Types

The current database schema uses a **flexible JSON-based approach** where all exercise types share the same table structure, with exercise-specific data stored in JSON columns.

### Strengths of Current Approach

1. **Flexibility**: The JSON columns (`options` and `correct_answer`) allow storing different data structures for different exercise types.
2. **Simplicity**: A single table is easier to maintain than multiple tables with complex relationships.
3. **Future-proofing**: New exercise types can be added without changing the database schema.

### Exercise Type Mapping Analysis

Here's how each exercise type maps to the current database schema:

| Frontend Exercise Type | Backend Schema Type | Database Support | JSON Fields Used |
|------------------------|---------------------|------------------|------------------|
| Word Scramble | Not directly mapped | Partial | sentence (in options), correct_answer |
| Multiple Choice | MultipleChoiceExercise | Full | options, correct_answer |
| Short Answer | ShortAnswerExercise | Full | correct_answer |
| Long Answer | Not directly mapped (ComprehensionExercise?) | Partial | max_length (in options) |
| True/False | TrueFalseExercise | Full | correct_answer |
| Fill in the Blanks | FillBlankExercise | Full | correct_answer |
| Matching Words | WordMatchExercise | Partial | word_bank (in options), correct_answer |
| Image Labeling | Not directly mapped | Inadequate | image_url, labels, label_points (all need to be in options) |
| Sentence Reordering | SentenceOrderExercise | Full | scrambled_text (in options), correct_order (in options) |
| Cloze Test with Word Bank | GapTextExercise | Full | word_bank (in options), correct_answer |

## Gaps and Inconsistencies

1. **Type Name Mismatches**: Frontend and backend types don't always match
   - Frontend: `word_scramble` ≠ Backend: No direct mapping
   - Frontend: `matching_words` ≠ Backend: `word_match`
   - Frontend: `sentence_reordering` ≠ Backend: `sentence_order`
   - Frontend: `image_labeling` has no backend equivalent
   - Frontend: `long_answer` has no exact backend equivalent

2. **Missing Schema Definitions**: Some frontend exercise types lack specific backend schema models
   - `WordScramble`
   - `ImageLabeling`
   - `LongAnswer` (might be using `ComprehensionExercise`)

3. **Structure Discrepancies**: Several exercise types have properties that don't clearly map to the database
   - Image Labeling requires structured data for image_url, labels, and label_points
   - Word Scramble needs to store both the scrambled sentence and the correct order

## Recommendations

### 1. Align Type Names

Standardize exercise type identifiers between frontend and backend:

```python
# Example of aligned naming
class WordScrambleExercise(BaseModel):
    exercise_type: str = "word_scramble"  # Match frontend
    # properties...
```

### 2. Add Missing Schema Models

Create Pydantic models for all frontend exercise types:

```python
# Example for ImageLabeling
class ImageLabelingExercise(BaseModel):
    exercise_type: str = "image_labeling"
    question: str
    image_url: str
    labels: List[str]
    label_points: List[Dict[str, Union[str, int, float]]]
    correct_answer: Dict[str, str]
    max_score: int = 1
    grading_type: str = "auto"
```

### 3. Consider Database Extensions

For better structured data and validation, consider one of these approaches:

#### Option A: Add Specific Columns

Add exercise-specific columns to the exercise table:

```sql
ALTER TABLE exercises 
ADD COLUMN image_url TEXT,
ADD COLUMN labels JSON,
ADD COLUMN label_points JSON,
ADD COLUMN sentences JSON,
ADD COLUMN word_bank JSON;
```

#### Option B: Use PostgreSQL JSONB with Validation

Maintain the flexible JSON structure but add validation constraints:

```sql
-- Example JSON schema validation for PostgreSQL
ALTER TABLE exercises ADD CONSTRAINT validate_image_labeling 
CHECK (
  exercise_type != 'image_labeling' OR 
  (options ? 'image_url' AND options ? 'labels' AND options ? 'label_points')
);
```

#### Option C: Create Exercise Type Views

Create database views for each exercise type for easier querying:

```sql
CREATE VIEW image_labeling_exercises AS
SELECT id, lesson_id, question, 
       options->>'image_url' as image_url,
       options->'labels' as labels,
       options->'label_points' as label_points,
       correct_answer
FROM exercises
WHERE exercise_type = 'image_labeling';
```

### 4. Update Documentation

Update the `ExerciseUnion` type in `schemas.py` to include all exercise types with their correct identifiers.

## Conclusion

The current database schema for exercises provides a flexible foundation that can support all 10 exercise types, but there are several inconsistencies and gaps that need addressing. The most urgent issues are:

1. **Adding schema definitions** for missing exercise types
2. **Aligning type identifiers** between frontend and backend
3. **Documenting the expected JSON structure** for each exercise type

These improvements will ensure that all exercise types are properly supported by the database and that the frontend and backend code can interact consistently.

With these changes, the LMS system will have a more robust foundation for handling all current exercise types and will be better prepared for adding new types in the future. 