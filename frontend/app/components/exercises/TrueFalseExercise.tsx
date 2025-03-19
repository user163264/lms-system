'use client';

import React from 'react';
import SelectionExercise, { SelectionOption, SelectionExerciseProps } from './base/SelectionExercise';
import { Exercise } from '../../context/ExerciseContext';

export interface TrueFalseExerciseProps extends Omit<SelectionExerciseProps, 'options' | 'exercise' | 'allowMultiple'> {
  exercise: Exercise;
}

/**
 * True/False Exercise Component
 * 
 * Specialized component for true/false exercises.
 * Provides standard true and false options.
 */
const TrueFalseExercise: React.FC<TrueFalseExerciseProps> = ({ 
  exercise,
  ...rest
}) => {
  // Standard true/false options
  const options: SelectionOption[] = [
    {
      id: 'true',
      label: 'True',
      value: 'true',
    },
    {
      id: 'false',
      label: 'False',
      value: 'false',
    }
  ];

  return (
    <SelectionExercise
      exercise={exercise}
      options={options}
      allowMultiple={false}
      {...rest}
    />
  );
};

export default TrueFalseExercise; 