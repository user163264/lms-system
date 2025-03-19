'use client';

import React, { useState } from 'react';

export interface ShortAnswerProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    correct_answer: string[];
    max_score?: number;
  };
  onSubmit: (answer: string, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Short Answer Exercise Component
 * 
 * This component renders a short answer question where students
 * need to provide a brief text response.
 */
const ShortAnswer: React.FC<ShortAnswerProps> = ({ 
  exercise, 
  onSubmit,
  showFeedback = false 
}) => {
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  
  const handleSubmit = () => {
    if (!answer.trim()) return; // Don't submit empty answers
    
    // Simple check for exact match (case-insensitive)
    // In a production environment, you might want more sophisticated matching
    const correct = exercise.correct_answer.some(
      correctAns => correctAns.toLowerCase() === answer.toLowerCase()
    );
    
    setIsCorrect(correct);
    setSubmitted(true);
    onSubmit(answer, exercise.id);
  };
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4" suppressHydrationWarning>
      <h3 className="text-lg font-medium mb-2">Short Answer</h3>
      <p className="text-gray-600 mb-4">Answer the question in one or two words.</p>
      
      <div className="mb-4" suppressHydrationWarning>
        <p className="mb-3 font-medium">{exercise.question}</p>
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your answer"
          disabled={submitted}
          suppressHydrationWarning
        />
      </div>
      
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${!answer.trim() ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={!answer.trim()}
          suppressHydrationWarning
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

export default ShortAnswer; 