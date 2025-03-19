# Technical Overview: Exercise System Architecture in Spotvogel LMS

## Database Structure

### Models
1. **Exercise Model** (`backend/app/models/exercise.py`)
   - Core table: `exercises` - Basic exercise entity with fields for lesson ID, title, content, and correct answers
   - `submissions` - Records user submissions with scores
   - `exercise_templates` - Reusable structures for different exercise types
   - `exercise_content` - Specific instances/questions linked to templates

2. **Exercise Types**
   - Defined as an enum: MULTIPLE_CHOICE, TRUE_FALSE, FILL_BLANK, SHORT_ANSWER, MATCHING_WORDS, WORD_SCRAMBLE, etc.
   - Each type has specific schema requirements for content and answers

## Backend API Structure

### Exercise Routes
1. **Basic Exercise Routes** (`backend/app/routes/exercises.py`)
   - `GET /api/exercises/` - List exercises, optionally filtered by lesson ID
   - `GET /api/exercises/{exercise_id}` - Get specific exercise
   - `POST /api/exercises/` - Create a new exercise
   - `POST /api/exercises/batch/` - Create multiple exercises from a template

2. **Advanced Exercise Routes** (`backend/app/routes/exercise_routes.py`)
   - Template management: `/api/exercises/templates/`
   - Content management: `/api/exercises/content/`
   - Submission endpoint: `/api/exercises/submit/`

3. **Submission Endpoint** (`/api/submit/`)
   - Legacy endpoint for backward compatibility
   - Processes exercise answers and returns scores

## Evaluation System

### Evaluation Logic (`backend/app/services/exercise_evaluator.py`)
1. **Base Evaluator** - Abstract class for all evaluators
2. **Type-Specific Evaluators**:
   - Each exercise type has a dedicated evaluator (e.g., MultipleChoiceEvaluator, FillBlankEvaluator)
   - Evaluators analyze user responses based on correct answers, awarding scores and providing feedback
3. **EvaluatorFactory** - Returns the appropriate evaluator for each exercise type

## Frontend Architecture

### Components Structure
1. **Factory Component** (`frontend/app/components/exercises/ExerciseFactory.tsx`)
   - Central dispatcher for rendering the appropriate exercise component
   - Renders a specific component based on the `exercise_type` property

2. **Exercise Components**:
   - `BaseExercise.tsx` - Common wrapper for all exercise types
   - Type-specific components (e.g., MultipleChoiceExercise, TrueFalseExercise)
   - Specialized components (e.g., SelectionExercise for choice-based exercises)

3. **Rendering Flow**:
   ```
   ExerciseFactory → Type-specific component → BaseExercise
   ```

### State Management
1. **Exercise Context** (`frontend/app/context/ExerciseContext.tsx`)
   - Handles exercise state with React Context API
   - Manages user answers, submission status, and feedback
   - Provides functions: setExercise, updateAnswer, submitAnswer, resetExercise

2. **Exercise Provider** - Wraps exercise components to provide context access
   ```tsx
   <ExerciseProvider onSubmit={handleSubmit}>
     <ExerciseFactory exercise={selectedExercise} />
   </ExerciseProvider>
   ```

## Data Flow

### Fetching Exercises
1. Page component (e.g., `exercises/[lessonId]/page.tsx`) fetches exercises from the API:
   ```javascript
   fetch(`${process.env.NEXT_PUBLIC_API_URL}/exercises/?lesson_id=${lessonId}`)
   ```

2. Exercises are stored in component state and passed to the renderer

### Answer Submission Flow
1. User interacts with exercise component
2. Component updates answer in ExerciseContext
3. On submit:
   - Current implementation: Mostly client-side validation with mock submission
   - Production (commented out): API call to `/api/submit/` endpoint

### Submission API Integration Status
- Basic structure exists for connecting to the backend API
- Currently uses local state rather than actually submitting to API
- Code for real API submission is commented out in `exercises/[lessonId]/page.tsx`

## File Structure Summary

### Backend
- Models: `backend/app/models/exercise.py`
- Routes: `backend/app/routes/exercises.py`, `backend/app/routes/exercise_routes.py`
- Evaluation: `backend/app/services/exercise_evaluator.py`

### Frontend
- Components: `frontend/app/components/exercises/`
- Context: `frontend/app/context/ExerciseContext.tsx`
- Pages: `frontend/app/exercises/[lessonId]/page.tsx`, `frontend/app/exercises/demo/page.tsx`

## Current Implementation Status
- All exercise types are implemented as React components
- Backend API structure exists but frontend-backend integration is incomplete
- Exercise rendering and client-side state management works correctly
- Actual submission to the API needs to be implemented

This architecture provides a flexible system for rendering and evaluating different types of exercises, with clean separation between the database models, API endpoints, and frontend components. 