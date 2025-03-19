'use client';

import React, { useState } from 'react';

export interface FillInBlanksProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    correct_answer: string[];
    max_score?: number;
    // Add any additional properties specific to fill-in-the-blanks
  };
  onSubmit: (answer: string, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Fill-in-the-Blanks Exercise Component
 * 
 * This component renders a fill-in-the-blanks exercise where students
 * need to type the missing word(s) in a sentence.
 */
const FillInBlanks: React.FC<FillInBlanksProps> = ({ 
  exercise, 
  onSubmit,
  showFeedback = false 
}) => {
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  
  // Split the question by the blank placeholder (represented by _______)
  const parts = exercise.question.split('_______');
  
  const handleSubmit = () => {
    // Simple case-insensitive check for correct answer
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
      <h3 className="text-lg font-medium mb-2">Fill in the Blank</h3>
      <p className="text-gray-600 mb-4">Fill in the blank with the correct word.</p>
      
      <div className="mb-4" suppressHydrationWarning>
        {parts[0]}
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className="border border-gray-300 rounded px-2 py-1 mx-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your answer"
          disabled={submitted}
          suppressHydrationWarning
        />
        {parts.length > 1 && parts[1]}
      </div>
      
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
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

export default FillInBlanks; 