# Frontend Architecture - Exercise Component System

## Overview

This document outlines the architecture for the exercise component system in the LMS frontend. The architecture follows a hierarchical approach where specialized components inherit from base components to maximize code reuse while maintaining flexibility.

## Component Hierarchy

```
                        BaseExercise
                       /     |      \
                      /      |       \
         InputExercise   SelectionExercise   InteractiveExercise
            /   \            /    \               /    \
           /     \          /      \             /      \
 ShortAnswer  FillBlanks  MultipleChoice  TrueFalse  Matching  WordScramble
```

## Core Components

### 1. Exercise Container Components

#### `ExerciseContainer`
- Main wrapper for all exercise components
- Handles layout, theming, and transitions
- Manages exercise lifecycle (loading, active, submitted, reviewed)

#### `ExerciseProvider`
- Context provider for exercise data and state
- Provides exercise data to child components
- Manages exercise state and interactions

### 2. Base Exercise Components

#### `BaseExercise`
- Abstract base component for all exercise types
- Implements common functionality:
  - Question display
  - Instructions
  - Submission handling
  - Feedback display
  - Scoring display

#### `InputExercise`
- Base for text input-based exercises
- Handles text input validation
- Manages keyboard interactions

#### `SelectionExercise`
- Base for selection-based exercises
- Handles option selection logic
- Manages radio/checkbox interactions

#### `InteractiveExercise`
- Base for drag-and-drop and interactive exercises
- Handles drag-and-drop functionality
- Manages touch and mouse interactions

### 3. Exercise Type Components

Each specific exercise type will extend the appropriate base component and implement unique functionality:

- `MultipleChoiceExercise` (from SelectionExercise)
- `TrueFalseExercise` (from SelectionExercise)
- `FillBlanksExercise` (from InputExercise)
- `ShortAnswerExercise` (from InputExercise)
- `MatchingExercise` (from InteractiveExercise)
- `WordScrambleExercise` (from InteractiveExercise)
- `SentenceReorderingExercise` (from InteractiveExercise)
- `ImageLabelingExercise` (from InteractiveExercise)

## Data Flow

The data flow through the exercise components follows this pattern:

1. The `ExerciseProvider` receives exercise data from the API
2. State is managed at the provider level using context
3. User interactions update the local state in the provider
4. On submission, the provider sends data to the API
5. Feedback and scoring are passed back to the components for display

```
API ↔ ExerciseProvider ↔ ExerciseContainer → BaseExercise → Specific Exercise Component
```

## State Management

State will be managed using React Context with reducers for complex state operations:

### `ExerciseContext`
- Current exercise data
- User's current answer/progress
- Submission status
- Feedback and scoring information

### `ExerciseReducer`
- Actions for user interactions:
  - `SELECT_OPTION`
  - `UPDATE_TEXT_INPUT`
  - `MOVE_ITEM`
  - `SUBMIT_ANSWER`
  - `RESET_EXERCISE`
  - `SHOW_FEEDBACK`

## API Integration

A set of custom hooks will handle API interactions:

- `useExerciseData` - Fetch exercise data by ID or type
- `useExerciseSubmission` - Submit exercise responses
- `useExerciseProgress` - Track and retrieve user progress

## UI Components

Shared UI components for consistent look and feel:

- `QuestionDisplay` - Renders question text with optional media
- `OptionsList` - Displays selection options
- `TextInput` - Standardized text input with validation
- `FeedbackDisplay` - Shows feedback based on correctness
- `SubmitButton` - Unified submission button with loading state
- `ScoreDisplay` - Displays user's score for the exercise

## Implementation Plan

1. Create base component structure and context provider
2. Implement SelectionExercise derived components first
   - MultipleChoiceExercise
   - TrueFalseExercise
3. Implement InputExercise derived components
   - ShortAnswerExercise
   - FillBlanksExercise
4. Implement InteractiveExercise derived components
   - MatchingExercise
   - WordScrambleExercise
5. Implement API integration and state management
6. Add scoring, feedback, and analytics features
7. Create comprehensive test suite

## Accessibility Considerations

- All components will support keyboard navigation
- ARIA attributes will be used for screen readers
- Focus management will be implemented for interactive elements
- Color contrast will meet WCAG AA standards
- Animations will respect reduced motion preferences

## Future Extensions

The architecture is designed to be extensible for future exercise types:

- Essay questions with AI grading
- Code-based exercises
- Math equation exercises
- Audio/pronunciation exercises

## Technical Stack

- React 19+ with TypeScript
- Context API for state management
- CSS Modules with Tailwind CSS
- React Testing Library for testing
- Axios for API calls 