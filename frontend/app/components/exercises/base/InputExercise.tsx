'use client';

import React, { useState } from 'react';
import BaseExercise, { BaseExerciseProps } from './BaseExercise';
import { useExercise, SubmissionStatus, Feedback, ExerciseAnswer } from '../../../context/ExerciseContext';

export interface InputExerciseProps extends Omit<BaseExerciseProps, 'children'> {
  placeholder?: string;
  defaultValue?: string;
  minLength?: number;
  maxLength?: number;
  multiline?: boolean;
  rows?: number;
  loading?: boolean;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

/**
 * Input Exercise Component
 * 
 * Base component for exercises that involve text input from the user.
 * Used for short answers, fill-in-the-blanks, and similar exercise types.
 */
const InputExercise: React.FC<InputExerciseProps> = ({
  exercise,
  placeholder = 'Type your answer here...',
  defaultValue = '',
  minLength = 0,
  maxLength,
  multiline = false,
  rows = 3,
  loading = false,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  const [inputValue, setInputValue] = useState<string>(defaultValue);
  
  // Handler for input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    const newValue = e.target.value;
    setInputValue(newValue);
    updateAnswer(newValue);
  };
  
  // Handler for form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim().length < minLength || state.submissionStatus === SubmissionStatus.SUBMITTING) return;
    
    await submitAnswer();
  };
  
  // Handler for reset
  const handleReset = () => {
    setInputValue(defaultValue);
    resetExercise();
  };
  
  // Determine if the input is disabled
  const isDisabled = state.submissionStatus === SubmissionStatus.SUBMITTED || loading;
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = 
    inputValue.trim().length < minLength || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  return (
    <BaseExercise 
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4" suppressHydrationWarning>
        <div>
          {multiline ? (
            <textarea
              value={inputValue}
              onChange={handleChange}
              placeholder={placeholder}
              disabled={isDisabled}
              rows={rows}
              maxLength={maxLength}
              className={`w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 
                ${isDisabled ? 'bg-gray-100 opacity-70 cursor-not-allowed' : 'border-gray-300'}
              `}
              suppressHydrationWarning
            />
          ) : (
            <input
              type="text"
              value={inputValue}
              onChange={handleChange}
              placeholder={placeholder}
              disabled={isDisabled}
              maxLength={maxLength}
              className={`w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 
                ${isDisabled ? 'bg-gray-100 opacity-70 cursor-not-allowed' : 'border-gray-300'}
              `}
              suppressHydrationWarning
            />
          )}
          
          {maxLength && (
            <div className="text-right text-sm text-gray-500 mt-1">
              {inputValue.length}/{maxLength}
            </div>
          )}
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

export default InputExercise; 