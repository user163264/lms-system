'use client';

import React from 'react';
import SelectionExercise, { SelectionOption, SelectionExerciseProps } from './base/SelectionExercise';
import { Exercise } from '../../context/ExerciseContext';

export interface MultipleChoiceExerciseProps extends Omit<SelectionExerciseProps, 'options' | 'exercise' | 'allowMultiple'> {
  exercise: Exercise;
}

/**
 * Multiple Choice Exercise Component
 * 
 * Specialized component for multiple choice exercises.
 * Formats the exercise options from the exercise data.
 */
const MultipleChoiceExercise: React.FC<MultipleChoiceExerciseProps> = ({ 
  exercise,
  ...rest
}) => {
  // Transform exercise options into SelectionOptions format
  const options: SelectionOption[] = exercise.options?.map((option, index) => ({
    id: index,
    label: option,
    value: option,
  })) || [];

  // Determine if this is a multiple selection or single selection based on correct_answer
  const allowMultiple = (exercise.correct_answer?.length || 0) > 1;

  return (
    <SelectionExercise
      exercise={exercise}
      options={options}
      allowMultiple={allowMultiple}
      {...rest}
    />
  );
};

export default MultipleChoiceExercise; 