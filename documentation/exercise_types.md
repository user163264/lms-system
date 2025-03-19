# LMS Exercise Types

This document provides an overview of all the exercise types available in the Learning Management System (LMS). These exercise types can be used by instructors to create interactive learning experiences for students.

## Overview

The LMS currently supports **10 different exercise types**, each designed for specific learning scenarios and objectives. All exercise types are demonstrated in the Exercise Showcase page, which can be accessed at:
- http://13.42.249.90:3001/exercise-showcase (original showcase with all types)
- http://13.42.249.90:3001/direct-showcase (simplified showcase with a subset of types)

## Available Exercise Types

### 1. Word Scramble
- **Type ID**: `word_scramble`
- **Description**: Students rearrange words to form a complete, meaningful sentence.
- **Use Case**: Assessing sentence structure comprehension, grammar, and language syntax.
- **Required Properties**: 
  - `question`: Text prompt
  - `sentence`: The scrambled sentence to arrange
  - `correct_answer`: Array containing the correctly ordered sentence

### 2. Multiple Choice
- **Type ID**: `multiple_choice`
- **Description**: Students select one correct option from several choices.
- **Use Case**: Assessing factual knowledge, concepts, or comprehension.
- **Required Properties**: 
  - `question`: Question prompt
  - `options`: Array of possible answers
  - `correct_answer`: Array containing the index of the correct option

### 3. Short Answer
- **Type ID**: `short_answer`
- **Description**: Students provide a concise answer (typically a few words or a sentence).
- **Use Case**: Testing recall, definitions, or brief explanations.
- **Required Properties**: 
  - `question`: Question prompt
  - `correct_answer`: Array of acceptable answers
  - `max_words` (optional): Maximum word limit

### 4. Long Answer
- **Type ID**: `long_answer`
- **Description**: Students write extended responses, essays, or paragraphs.
- **Use Case**: Assessing critical thinking, analytical skills, or detailed explanations.
- **Required Properties**: 
  - `question`: Essay prompt
  - `min_words` (optional): Minimum word requirement
  - `max_words` (optional): Maximum word limit
  - `required_keywords` (optional): Keywords that should appear in the answer

### 5. True/False
- **Type ID**: `true_false`
- **Description**: Students determine whether a statement is true or false.
- **Use Case**: Quick assessment of factual knowledge or understanding.
- **Required Properties**: 
  - `question`: Statement to evaluate
  - `correct_answer`: Array containing either "true" or "false"

### 6. Fill in the Blanks
- **Type ID**: `fill_blank` or `fill_in_blanks`
- **Description**: Students complete sentences by filling in missing words.
- **Use Case**: Testing vocabulary, grammar, or specific knowledge points.
- **Required Properties**: 
  - `question`: Prompt for the fill-in-the-blank exercise
  - `correct_answer`: Array containing the complete sentence(s)

### 7. Matching Words
- **Type ID**: `matching_words`
- **Description**: Students match items from two columns (e.g., terms with definitions).
- **Use Case**: Testing relationships between concepts, terms, or cause and effect.
- **Required Properties**: 
  - `question`: Instructions for the matching exercise
  - `items_a`: Array of items in the first column
  - `items_b`: Array of items in the second column
  - `correct_matches`: Array of indices representing correct matches

### 8. Image Labeling
- **Type ID**: `image_labeling`
- **Description**: Students label specific parts of an image.
- **Use Case**: Anatomy, geography, diagram identification, visual comprehension.
- **Required Properties**: 
  - `question`: Instructions for the labeling exercise
  - `image_url`: URL of the image to be labeled
  - `labels`: Array of available labels
  - `label_points`: Array of points on the image to be labeled
  - `correct_answer`: Object mapping point IDs to correct labels

### 9. Sentence Reordering
- **Type ID**: `sentence_reordering`
- **Description**: Students arrange sentences in the correct logical order.
- **Use Case**: Testing narrative comprehension, logical sequencing, or procedural understanding.
- **Required Properties**: 
  - `question`: Instructions for the reordering exercise
  - `sentences`: Array of sentences to be reordered
  - `correct_order`: Array representing the correct order of sentences

### 10. Cloze Test with Word Bank
- **Type ID**: `cloze_test`
- **Description**: Students fill in blanks in a text using words from a provided word bank.
- **Use Case**: Vocabulary in context, grammar, reading comprehension.
- **Required Properties**: 
  - `question`: Instructions for the cloze test
  - `word_bank`: Array of words to choose from
  - `correct_answer`: Array of correct placements

## Technical Implementation

All exercise types are implemented as React components in the `frontend/app/components/exercises` directory. The central dispatcher for all exercise types is the `ExerciseRenderer` component, which renders the appropriate exercise component based on the `exercise_type` property.

Each exercise type supports the following common functionality:
- Question display
- Answer submission
- Feedback display (optional)
- Scoring (automatic or manual depending on the exercise type)

## Adding a New Exercise Type

To add a new exercise type to the system:

1. Create a new React component in the `frontend/app/components/exercises` directory
2. Update the `ExerciseRenderer` component to include the new exercise type
3. Add the new exercise type to the `ExerciseShowcasePage` component
4. Update the backend schemas and database models to support the new exercise type
5. Update the exercise creation and grading functionality in the backend

## Best Practices

When designing exercises, consider:
- Clear instructions and examples
- Appropriate difficulty level
- Alignment with learning objectives
- Meaningful feedback
- Accessibility considerations
- Mobile responsiveness 