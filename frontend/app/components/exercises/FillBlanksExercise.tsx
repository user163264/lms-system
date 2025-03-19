'use client';

import React, { useState } from 'react';
import BaseExercise from './base/BaseExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface FillBlanksExerciseProps {
  exercise: Exercise;
  showFeedback?: boolean;
  className?: string;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

/**
 * Fill in the Blanks Exercise Component
 * 
 * Specialized component for fill-in-the-blanks exercises.
 * Renders a sentence with a blank space for user input.
 */
const FillBlanksExercise: React.FC<FillBlanksExerciseProps> = ({ 
  exercise,
  showFeedback = false,
  className = '',
  onSubmit,
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  const [inputValue, setInputValue] = useState<string>('');
  
  // Split the question by the blank placeholder (represented by _______)
  const parts = exercise.question.split('_______');
  
  // Create a placeholder based on available info
  let placeholder = "Fill in the blank";
  if (exercise.max_words === 1) {
    placeholder = "Enter a word";
  } else if (exercise.max_words && exercise.max_words > 1) {
    placeholder = `Enter up to ${exercise.max_words} words`;
  }
  
  // Handler for input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    const newValue = e.target.value;
    setInputValue(newValue);
    updateAnswer(newValue);
  };
  
  // Handler for form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim().length === 0 || state.submissionStatus === SubmissionStatus.SUBMITTING) return;
    
    await submitAnswer();
  };
  
  // Handler for reset
  const handleReset = () => {
    setInputValue('');
    resetExercise();
  };
  
  // Determine if the input is disabled
  const isDisabled = state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = 
    inputValue.trim().length === 0 || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Generate a title/instruction if not provided
  const instructions = exercise.instructions || "Fill in the missing word or phrase in the sentence below.";
  
  // Create a modified exercise object with cleaned/enhanced information
  const modifiedExercise = {
    ...exercise,
    instructions: instructions,
    question: "" // We'll handle the question rendering in the children content
  };

  return (
    <BaseExercise 
      exercise={modifiedExercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4" suppressHydrationWarning>
        <div className="mb-4">
          <p className="mb-3 font-medium">
            {parts[0]}
            <span className="inline-block mx-1 border-b-2 border-gray-400 min-w-[100px]">
              <input
                type="text"
                value={inputValue}
                onChange={handleChange}
                placeholder={placeholder}
                disabled={isDisabled}
                maxLength={exercise.max_words ? exercise.max_words * 10 : 50}
                className="w-full border-none focus:outline-none focus:ring-0 bg-transparent px-1"
                suppressHydrationWarning
              />
            </span>
            {parts.length > 1 && parts[1]}
          </p>
        </div>
        
        <div className="flex space-x-2 pt-2">
          <button
            type="submit"
            disabled={isSubmitDisabled}
            className={`px-4 py-2 rounded text-white bg-blue-500 hover:bg-blue-600 transition-colors
              ${isSubmitDisabled ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            {state.submissionStatus === SubmissionStatus.SUBMITTING ? 'Submitting...' : 'Submit'}
          </button>
          
          {state.submissionStatus !== SubmissionStatus.IDLE && (
            <button
              type="button"
              onClick={handleReset}
              className="px-4 py-2 rounded text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </form>
    </BaseExercise>
  );
};

export default FillBlanksExercise; 