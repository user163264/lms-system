'use client';

import React, { useEffect, ReactNode, useRef } from 'react';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../../context/ExerciseContext';

export interface BaseExerciseProps {
  exercise: Exercise;
  showFeedback?: boolean;
  className?: string;
  children?: ReactNode;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

/**
 * Base Exercise Component
 * 
 * Provides common layout and functionality for all exercise types.
 */
const BaseExercise: React.FC<BaseExerciseProps> = ({
  exercise,
  showFeedback = false,
  className = '',
  children
}) => {
  const { state, setExercise } = useExercise();
  const initializedRef = useRef(false);
  
  // Set the exercise in context when the component mounts, but only once
  useEffect(() => {
    // Only set the exercise if it's not already set or if it changed
    if (!initializedRef.current) {
      setExercise(exercise);
      initializedRef.current = true;
    }
  }, [exercise, setExercise]);
  
  return (
    <div className={`bg-white rounded-xl shadow-md p-6 mb-4 ${className}`} suppressHydrationWarning>
      {/* Exercise Header */}
      {exercise.exercise_type && (
        <h3 className="text-lg font-medium mb-2 capitalize">
          {exercise.exercise_type.replace('_', ' ')}
        </h3>
      )}
      
      {/* Instructions */}
      {exercise.instructions && (
        <p className="text-gray-600 mb-4">{exercise.instructions}</p>
      )}
      
      {/* Question */}
      <div className="mb-4" suppressHydrationWarning>
        <p className="mb-3 font-medium">{exercise.question}</p>
        
        {/* Exercise Content - Rendered by child components */}
        <div className="exercise-content">
          {children}
        </div>
      </div>
      
      {/* Feedback Display */}
      {showFeedback && state.submissionStatus === SubmissionStatus.SUBMITTED && state.feedback && (
        <div 
          className={`mt-4 p-3 rounded ${
            state.feedback.isCorrect 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}
        >
          <p className="font-medium">
            {state.feedback.isCorrect ? '✓ Correct!' : '✗ Incorrect.'}
          </p>
          <p>{state.feedback.message}</p>
          {state.feedback.score !== undefined && (
            <p className="mt-1">Score: {state.feedback.score}</p>
          )}
        </div>
      )}
      
      {/* Error Display */}
      {state.error && (
        <div className="mt-4 p-3 rounded bg-red-100 text-red-800">
          <p className="font-medium">Error</p>
          <p>{state.error}</p>
        </div>
      )}
    </div>
  );
};

export default BaseExercise; 