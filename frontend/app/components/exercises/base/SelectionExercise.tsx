'use client';

import React, { useState } from 'react';
import BaseExercise, { BaseExerciseProps } from './BaseExercise';
import { useExercise, SubmissionStatus, Feedback, ExerciseAnswer } from '../../../context/ExerciseContext';

export interface SelectionOption {
  id: string | number;
  label: string;
  value: string | number | boolean;
}

export interface SelectionExerciseProps extends Omit<BaseExerciseProps, 'children'> {
  options: SelectionOption[];
  allowMultiple?: boolean;
  defaultSelected?: (string | number)[];
  loading?: boolean;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

/**
 * Selection Exercise Component
 * 
 * Base component for exercises that involve selecting from a list of options.
 * Used for multiple choice, true/false, and similar exercise types.
 */
const SelectionExercise: React.FC<SelectionExerciseProps> = ({
  exercise,
  options,
  allowMultiple = false,
  defaultSelected = [],
  loading = false,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  const [selected, setSelected] = useState<(string | number)[]>(defaultSelected);
  
  // Handler for option selection
  const handleSelect = (optionId: string | number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    let newSelected: (string | number)[];
    
    if (allowMultiple) {
      // For multiple selection, toggle the selected option
      newSelected = selected.includes(optionId)
        ? selected.filter(id => id !== optionId)
        : [...selected, optionId];
    } else {
      // For single selection, replace the selection
      newSelected = [optionId];
    }
    
    setSelected(newSelected);
    
    // Update answer in context
    const selectedValues = newSelected.map(id => {
      const option = options.find(opt => opt.id === id);
      return option ? option.value : null;
    }).filter(Boolean);
    
    const answer = allowMultiple 
      ? selectedValues as string[] | number[] 
      : (typeof selectedValues[0] === 'string' ? selectedValues[0] : String(selectedValues[0])) || '';
    updateAnswer(answer);
  };
  
  // Handler for form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selected.length === 0 || state.submissionStatus === SubmissionStatus.SUBMITTING) return;
    
    await submitAnswer();
  };
  
  // Handler for reset
  const handleReset = () => {
    setSelected([]);
    resetExercise();
  };
  
  // Determine if an option is disabled
  const isDisabled = state.submissionStatus === SubmissionStatus.SUBMITTED || loading;
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = selected.length === 0 || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  return (
    <BaseExercise 
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          {options.map((option) => (
            <div 
              key={option.id}
              className={`
                flex items-center p-3 rounded border cursor-pointer transition
                ${selected.includes(option.id) 
                  ? 'bg-blue-50 border-blue-300' 
                  : 'border-gray-200 hover:bg-gray-50'}
                ${isDisabled ? 'opacity-70 cursor-not-allowed' : ''}
              `}
              onClick={() => !isDisabled && handleSelect(option.id)}
            >
              <input
                type={allowMultiple ? 'checkbox' : 'radio'}
                id={`option-${exercise.id}-${option.id}`}
                name={`exercise-${exercise.id}`}
                checked={selected.includes(option.id)}
                onChange={() => {}} // Controlled by div click handler
                disabled={isDisabled}
                className={`mr-3 h-4 w-4 ${allowMultiple ? 'rounded' : 'rounded-full'} text-blue-600 focus:ring-blue-500`}
              />
              <label 
                htmlFor={`option-${exercise.id}-${option.id}`}
                className="flex-grow cursor-pointer"
              >
                {option.label}
              </label>
            </div>
          ))}
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

export default SelectionExercise; 