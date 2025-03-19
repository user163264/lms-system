'use client';

import React, { ReactNode } from 'react';
import BaseExercise, { BaseExerciseProps } from './BaseExercise';
import { Feedback, ExerciseAnswer } from '../../../context/ExerciseContext';

export interface InteractiveExerciseProps extends Omit<BaseExerciseProps, 'children'> {
  children?: ReactNode;
  loading?: boolean;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

/**
 * Interactive Exercise Component
 * 
 * Base component for interactive exercises that involve complex interactions
 * like matching, reordering, or drag-and-drop.
 */
const InteractiveExercise: React.FC<InteractiveExerciseProps> = ({
  exercise,
  children,
  loading = false,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  return (
    <BaseExercise 
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      {/* Allow child components to provide their own interactive UI */}
      {children}
    </BaseExercise>
  );
};

export default InteractiveExercise; 