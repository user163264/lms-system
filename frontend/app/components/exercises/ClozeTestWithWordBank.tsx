'use client';

import React, { useState } from 'react';

export interface ClozeTestWithWordBankProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    word_bank?: string[];
    correct_answer: string[];
    max_score?: number;
  };
  onSubmit: (answer: string[], exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Cloze Test with Word Bank Exercise Component
 * 
 * This component renders a fill-in-the-blanks exercise where students
 * need to fill in multiple blanks from a provided word bank.
 */
const ClozeTestWithWordBank: React.FC<ClozeTestWithWordBankProps> = ({ 
  exercise, 
  onSubmit,
  showFeedback = false 
}) => {
  // Question with blanks (e.g., "Mona Lisa hangs in the _______ in _______")
  const parts = exercise.question.split('_______');
  const blankCount = parts.length - 1;
  
  // Initialize state for answers to each blank
  const [answers, setAnswers] = useState<string[]>(Array(blankCount).fill(''));
  const [submitted, setSubmitted] = useState(false);
  const [correctAnswers, setCorrectAnswers] = useState<boolean[]>(Array(blankCount).fill(false));
  
  // Ensure word bank exists
  const wordBank = exercise.word_bank || [];
  
  // Check if all blanks have been filled
  const allAnswered = answers.every(answer => answer !== '');
  
  const handleSelectAnswer = (blank: number, word: string) => {
    if (submitted) return;
    
    const newAnswers = [...answers];
    newAnswers[blank] = word;
    setAnswers(newAnswers);
  };
  
  const handleSubmit = () => {
    if (!allAnswered) return;
    
    // Check each answer against the corresponding correct answer
    const results = answers.map((answer, index) => {
      // Ensure we have a corresponding correct answer
      if (index < exercise.correct_answer.length) {
        return answer.toLowerCase() === exercise.correct_answer[index].toLowerCase();
      }
      return false;
    });
    
    setCorrectAnswers(results);
    setSubmitted(true);
    onSubmit(answers, exercise.id);
  };
  
  const renderQuestion = () => {
    return (
      <div className="mb-4">
        {parts.map((part, index) => (
          <React.Fragment key={index}>
            <span>{part}</span>
            {index < parts.length - 1 && (
              <span className="relative inline-block mx-1">
                <input
                  type="text"
                  value={answers[index]}
                  readOnly
                  className={`border ${
                    submitted 
                      ? correctAnswers[index] 
                        ? 'border-green-500 bg-green-50' 
                        : 'border-red-500 bg-red-50'
                      : 'border-gray-300'
                  } rounded px-2 py-1 w-24 text-center`}
                  placeholder="______"
                />
                {submitted && showFeedback && !correctAnswers[index] && (
                  <span className="absolute -bottom-6 left-0 text-xs text-red-600">
                    {exercise.correct_answer[index]}
                  </span>
                )}
              </span>
            )}
          </React.Fragment>
        ))}
      </div>
    );
  };
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <h3 className="text-lg font-medium mb-2">Fill in the Blanks with Word Bank</h3>
      <p className="text-gray-600 mb-4">
        Fill in the blanks using words from the word bank below.
      </p>
      
      {/* The question with blanks */}
      {renderQuestion()}
      
      {/* Word bank */}
      <div className="mt-6 mb-4">
        <h4 className="text-md font-medium mb-2">Word Bank:</h4>
        <div className="flex flex-wrap gap-2">
          {wordBank.map((word, index) => (
            <button
              key={index}
              onClick={() => {
                // Find the first empty blank and fill it with this word
                const emptyIndex = answers.findIndex(a => a === '');
                if (emptyIndex >= 0) {
                  handleSelectAnswer(emptyIndex, word);
                }
              }}
              disabled={submitted || answers.includes(word)}
              className={`px-3 py-1 rounded border ${
                answers.includes(word)
                  ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
              }`}
            >
              {word}
            </button>
          ))}
        </div>
      </div>
      
      {/* Submit button or feedback */}
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${!allAnswered ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={!allAnswered}
        >
          Submit
        </button>
      ) : showFeedback ? (
        <div className={`mt-4 p-3 rounded ${
          correctAnswers.every(c => c) 
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}>
          {correctAnswers.every(c => c)
            ? '✓ All correct!' 
            : `✗ Some answers are incorrect. Please check the highlighted fields.`}
        </div>
      ) : null}
    </div>
  );
};

export default ClozeTestWithWordBank; 