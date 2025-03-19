# Frontend API Integration Documentation

## Overview

This document outlines the centralized API integration approach used in the Spotvogel LMS frontend. All API calls are now managed through a unified API service layer, ensuring consistency across the application.

## API Service Structure

The API service is implemented in `/frontend/app/services/api.ts` and provides:

1. A centralized point for all API calls
2. Consistent error handling
3. Typed responses using TypeScript interfaces
4. Separation of concerns by API domain (exercises, lessons, submissions)

## Available API Services

### Exercise API

- `getExercisesByLessonId(lessonId)` - Fetch all exercises for a specific lesson
- `getExerciseById(exerciseId)` - Fetch a single exercise by ID
- `submitAnswer(exerciseId, answer, userId?)` - Submit an answer for evaluation

### Lesson API

- `getLessonById(lessonId)` - Fetch a single lesson by ID
- `getAllLessons()` - Fetch all available lessons

### Submission API

- `getUserSubmissions(userId)` - Fetch all submissions for a user
- `createSubmission(exerciseId, answer, userId?)` - Create a new submission record

## Implementation Notes

1. All direct `fetch()` calls have been replaced with API service calls
2. The ExerciseContext now uses the API service for answer submission
3. Type adapters handle conversion between different exercise types as needed
4. All components follow a consistent pattern for data fetching and submission

## Example Usage

```typescript
// Fetching exercises
useEffect(() => {
  api.exercises.getExercisesByLessonId(lessonId)
    .then((data) => {
      setExercises(data);
    })
    .catch((error) => {
      // Handle error
    });
}, [lessonId]);

// Submitting an answer
const handleSubmit = async (answer, exerciseId) => {
  try {
    const feedback = await api.exercises.submitAnswer(exerciseId, answer);
    // Handle feedback
  } catch (error) {
    // Handle error
  }
};
```

## Type Compatibility

Since the exercise system has two slightly different Exercise interfaces (one in ExerciseContext and one in ExerciseRenderer), we've implemented type adapters to ensure compatibility. The adapter ensures all required fields are present when passing data between components.

## Future Enhancements

- Add authorization header support for protected endpoints
- Implement request caching for frequently accessed data
- Add request interceptors for global error handling
- Support for real-time data with WebSockets for live exercise feedback 