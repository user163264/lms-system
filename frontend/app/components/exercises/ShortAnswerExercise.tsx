'use client';

import React from 'react';
import InputExercise, { InputExerciseProps } from './base/InputExercise';
import { Exercise } from '../../context/ExerciseContext';

export interface ShortAnswerExerciseProps extends Omit<InputExerciseProps, 'exercise' | 'multiline' | 'rows'> {
  exercise: Exercise;
}

/**
 * Short Answer Exercise Component
 * 
 * Specialized component for short answer exercises.
 * Single-line text input with character limits based on exercise configuration.
 */
const ShortAnswerExercise: React.FC<ShortAnswerExerciseProps> = ({ 
  exercise,
  ...rest
}) => {
  // Get min/max word requirements from exercise data if available
  const minLength = exercise.min_words ? 1 : 0; // Minimum 1 character if min_words is specified
  const maxLength = exercise.max_words ? exercise.max_words * 10 : undefined; // Rough estimate: 10 chars per word
  
  return (
    <InputExercise
      exercise={exercise}
      placeholder="Enter your answer..."
      minLength={minLength}
      maxLength={maxLength}
      multiline={false}
      {...rest}
    />
  );
};

export default ShortAnswerExercise; 