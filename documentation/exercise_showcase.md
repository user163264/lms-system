# Exercise Showcase Page

## Overview

The Exercise Showcase page is a comprehensive demonstration of all 10 exercise types available in the Spotvogel LMS. This page is designed to showcase the functionality of each exercise type in a single, accessible interface.

## URL Access

The showcase is accessible at:

```
http://13.42.249.90/exercise-showcase
```

## Features

- Displays all 10 exercise types in a single page
- Provides example questions for each exercise type
- Allows users to interact with and submit answers for each exercise
- Shows feedback for submitted answers
- Uses the centralized API service architecture

## Exercise Types Included

1. **Multiple Choice**: Selection from predefined options
2. **True/False**: Binary decision exercises
3. **Fill in the Blank**: Complete sentences with missing words
4. **Short Answer**: Brief text responses
5. **Matching Words**: Connect related items
6. **Word Scramble**: Rearrange words to form a sentence
7. **Sentence Reordering**: Place sentences in the correct sequence
8. **Image Labeling**: Identify and label parts of an image
9. **Long Answer**: Extended essay-style responses
10. **Cloze Test**: Fill in missing words using a word bank

## Implementation Notes

- Each exercise type is rendered using the shared `ExerciseRenderer` component
- Exercise data is provided as static examples rather than from the API
- Evaluation is performed locally for demonstration purposes
- The page uses the same styling and components as the regular exercise pages

## Technical Details

- File path: `/frontend/app/exercise-showcase/page.tsx`
- Component architecture:
  ```
  ExerciseShowcase
  └── ExerciseRenderer
      └── Type-specific exercise component
  ```
- Local evaluation logic is implemented for immediate feedback

## Usage

This page serves as:

1. A demonstration for stakeholders and users
2. A testing ground for exercise functionality
3. A reference for developers implementing new exercise types
4. A publicly accessible showcase of the system's capabilities

## Maintenance

When updating exercise types or creating new ones, this page should be updated to include examples of any new functionality. 