'use client';

import React, { useState, useEffect } from 'react';
import InputExercise, { InputExerciseProps } from './base/InputExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface LongAnswerExerciseProps extends Omit<InputExerciseProps, 'exercise'> {
  exercise: Exercise;
}

/**
 * Long Answer Exercise Component
 * 
 * Component for exercises where users write extended responses or essays.
 * Supports word count tracking, min/max word limits, and required keywords.
 */
const LongAnswerExercise: React.FC<LongAnswerExerciseProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  
  // Local state for the user's answer
  const [answer, setAnswer] = useState('');
  
  // State for word count
  const [wordCount, setWordCount] = useState(0);
  
  // State for tracking keyword requirements
  const [keywordStatus, setKeywordStatus] = useState<Record<string, boolean>>({});
  
  // Initialize keywords status
  useEffect(() => {
    if (exercise.required_keywords && Array.isArray(exercise.required_keywords)) {
      const initialStatus: Record<string, boolean> = {};
      exercise.required_keywords.forEach(keyword => {
        initialStatus[keyword] = false;
      });
      setKeywordStatus(initialStatus);
    }
  }, [exercise.required_keywords]);
  
  // Update word count and keyword status when answer changes
  useEffect(() => {
    // Count words by splitting on whitespace and filtering out empty strings
    const words = answer.trim().split(/\s+/).filter(word => word !== '');
    setWordCount(words.length);
    
    // Check for required keywords
    if (exercise.required_keywords && Array.isArray(exercise.required_keywords)) {
      const lowerAnswer = answer.toLowerCase();
      const newStatus: Record<string, boolean> = {};
      
      exercise.required_keywords.forEach(keyword => {
        // Check if the keyword appears in the answer (case insensitive)
        newStatus[keyword] = lowerAnswer.includes(keyword.toLowerCase());
      });
      
      setKeywordStatus(newStatus);
    }
  }, [answer, exercise.required_keywords]);
  
  // Update context when answer changes
  useEffect(() => {
    if (answer !== '') {
      updateAnswer(answer);
    }
  }, [answer, updateAnswer]);
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (state.submissionStatus === SubmissionStatus.SUBMITTING) {
      return;
    }
    
    await submitAnswer();
  };
  
  // Check if word count is within limits
  const isWithinWordLimits = () => {
    const minWords = exercise.min_words || 0;
    const maxWords = exercise.max_words || Infinity;
    return wordCount >= minWords && wordCount <= maxWords;
  };
  
  // Check if all required keywords are present
  const allKeywordsPresent = () => {
    if (!exercise.required_keywords || !Array.isArray(exercise.required_keywords) || exercise.required_keywords.length === 0) {
      return true;
    }
    
    return Object.values(keywordStatus).every(present => present);
  };
  
  // Determine if submit button should be disabled
  const isSubmitDisabled = 
    !answer.trim() || 
    !isWithinWordLimits() || 
    !allKeywordsPresent() || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Handle answer change
  const handleAnswerChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    setAnswer(e.target.value);
  };
  
  // Handle reset
  const handleReset = () => {
    setAnswer('');
    setWordCount(0);
    resetExercise();
  };
  
  return (
    <InputExercise
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="mb-1">
          <textarea
            value={answer}
            onChange={handleAnswerChange}
            disabled={state.submissionStatus === SubmissionStatus.SUBMITTED}
            className={`w-full p-3 border rounded-md resize-y min-h-[200px] ${
              !isWithinWordLimits() ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Write your answer here..."
          />
        </div>
        
        {/* Word count and limits indicator */}
        <div className="text-sm">
          <span className={!isWithinWordLimits() ? 'text-red-500' : 'text-gray-600'}>
            Word count: {wordCount}
            {exercise.min_words ? ` (minimum: ${exercise.min_words})` : ''}
            {exercise.max_words ? ` (maximum: ${exercise.max_words})` : ''}
          </span>
        </div>
        
        {/* Required keywords indicator */}
        {exercise.required_keywords && Array.isArray(exercise.required_keywords) && exercise.required_keywords.length > 0 && (
          <div className="text-sm mt-2">
            <p className="font-medium mb-1">Required keywords:</p>
            <ul className="list-disc pl-5 space-y-1">
              {exercise.required_keywords.map(keyword => (
                <li key={keyword} className={keywordStatus[keyword] ? 'text-green-600' : 'text-red-500'}>
                  {keyword} {keywordStatus[keyword] ? '✓' : '✗'}
                </li>
              ))}
            </ul>
          </div>
        )}
        
        <div className="flex space-x-4">
          {state.submissionStatus !== SubmissionStatus.SUBMITTED ? (
            <button
              type="submit"
              className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${
                isSubmitDisabled ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={isSubmitDisabled}
            >
              Submit
            </button>
          ) : (
            <button
              type="button"
              onClick={handleReset}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </form>
    </InputExercise>
  );
};

export default LongAnswerExercise; 