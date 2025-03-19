'use client';

import React, { useState } from 'react';

export interface MultipleChoiceProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    options?: string[];
    correct_answer: string[];
    max_score?: number;
  };
  onSubmit: (answer: string, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Multiple Choice Exercise Component
 * 
 * This component renders a multiple choice question where students
 * select one answer from a list of options.
 */
const MultipleChoice: React.FC<MultipleChoiceProps> = ({ 
  exercise, 
  onSubmit,
  showFeedback = false 
}) => {
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  
  // Make sure we have options to display
  if (!exercise.options || exercise.options.length === 0) {
    return <div className="text-red-500">Error: No options provided for multiple choice question.</div>;
  }
  
  const handleSubmit = () => {
    if (!answer) return; // Don't submit empty answers
    
    // Check if the answer is correct
    const correct = exercise.correct_answer.some(
      correctAns => correctAns.toLowerCase() === answer.toLowerCase()
    );
    
    setIsCorrect(correct);
    setSubmitted(true);
    onSubmit(answer, exercise.id);
  };
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <h3 className="text-lg font-medium mb-2">Multiple Choice</h3>
      <p className="text-gray-600 mb-4">Select the correct answer from the options below.</p>
      
      <div className="mb-4">
        <p className="mb-3 font-medium">{exercise.question}</p>
        
        <div className="space-y-2">
          {exercise.options.map((option, index) => (
            <div key={index} className="flex items-center">
              <input
                type="radio"
                id={`option-${exercise.id}-${index}`}
                name={`exercise-${exercise.id}`}
                value={option}
                checked={answer === option}
                onChange={(e) => setAnswer(e.target.value)}
                disabled={submitted}
                className="mr-2 focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300"
              />
              <label 
                htmlFor={`option-${exercise.id}-${index}`}
                className="text-gray-700 cursor-pointer"
              >
                {option}
              </label>
            </div>
          ))}
        </div>
      </div>
      
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${!answer ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={!answer}
        >
          Submit
        </button>
      ) : showFeedback ? (
        <div className={`mt-4 p-3 rounded ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {isCorrect 
            ? '✓ Correct!' 
            : `✗ Incorrect. The correct answer is "${exercise.correct_answer[0]}".`}
        </div>
      ) : null}
    </div>
  );
};

export default MultipleChoice; 