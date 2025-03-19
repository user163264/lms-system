'use client';

import React, { useState } from 'react';

export interface TrueFalseProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    correct_answer: string[];
    options?: string[];
    max_score?: number;
  };
  onSubmit: (answer: string, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * True/False Exercise Component
 * 
 * This component renders a true/false question where students
 * select either "True" or "False" from a dropdown menu.
 */
const TrueFalse: React.FC<TrueFalseProps> = ({ 
  exercise, 
  onSubmit,
  showFeedback = false 
}) => {
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  
  // Default options if not provided
  const options = exercise.options || ['waar', 'niet waar'];
  
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
      <h3 className="text-lg font-medium mb-2">True or False</h3>
      <p className="text-gray-600 mb-4">Select whether the statement is true or false.</p>
      
      <div className="mb-4">
        <p className="mb-2">{exercise.question}</p>
        <select
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={submitted}
        >
          <option value="">Select an answer</option>
          {options.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
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

export default TrueFalse; 