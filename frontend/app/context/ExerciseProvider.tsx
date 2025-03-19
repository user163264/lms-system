'use client';

import React, { ReactNode } from 'react';
import { ExerciseProvider as ContextProvider, ExerciseAnswer, Feedback } from './ExerciseContext';

interface ExerciseProviderProps {
  children: ReactNode;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

/**
 * Exercise Provider Component
 * 
 * Wrapper around the ExerciseProvider from ExerciseContext for easier usage
 */
export const ExerciseProvider: React.FC<ExerciseProviderProps> = ({ 
  children,
  onSubmit
}) => {
  return (
    <ContextProvider onSubmit={onSubmit}>
      {children}
    </ContextProvider>
  );
}; 