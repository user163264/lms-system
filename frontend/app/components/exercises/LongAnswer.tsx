'use client';

import React, { useState } from 'react';

export interface LongAnswerProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    min_words?: number;
    max_words?: number;
    required_keywords?: string[];
    correct_answer?: string[]; // Sample answer or key points
    max_score?: number;
  };
  onSubmit: (answer: string, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Long Answer Exercise Component
 * 
 * This component renders an essay-type question where students
 * can provide a longer text response that may be assessed for keywords,
 * length, and other parameters.
 */
const LongAnswer: React.FC<LongAnswerProps> = ({
  exercise,
  onSubmit,
  showFeedback = false,
}) => {
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [feedback, setFeedback] = useState<{
    wordCount: number;
    meetsMinWords: boolean;
    meetsMaxWords: boolean;
    keywordsFound: string[];
    keywordsMissing: string[];
  } | null>(null);

  const minWords = exercise.min_words || 50;
  const maxWords = exercise.max_words || 500;
  const requiredKeywords = exercise.required_keywords || [];

  const countWords = (text: string): number => {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
  };

  const checkKeywords = (text: string): { found: string[]; missing: string[] } => {
    const textLower = text.toLowerCase();
    const found: string[] = [];
    const missing: string[] = [];

    requiredKeywords.forEach(keyword => {
      if (textLower.includes(keyword.toLowerCase())) {
        found.push(keyword);
      } else {
        missing.push(keyword);
      }
    });

    return { found, missing };
  };

  const handleSubmit = () => {
    if (!answer.trim() || countWords(answer) < minWords) return;

    const wordCount = countWords(answer);
    const { found: keywordsFound, missing: keywordsMissing } = checkKeywords(answer);

    const feedbackData = {
      wordCount,
      meetsMinWords: wordCount >= minWords,
      meetsMaxWords: wordCount <= maxWords,
      keywordsFound,
      keywordsMissing,
    };

    setFeedback(feedbackData);
    setSubmitted(true);
    onSubmit(answer, exercise.id);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <h3 className="text-lg font-medium mb-2">Essay / Long Answer</h3>
      <p className="text-gray-600 mb-4">
        Write a response addressing all parts of the question. 
        {minWords > 0 && ` Minimum ${minWords} words.`}
        {maxWords > 0 && ` Maximum ${maxWords} words.`}
      </p>

      <div className="mb-4">
        <p className="mb-3 font-medium">{exercise.question}</p>
        
        {requiredKeywords.length > 0 && (
          <div className="mb-3 p-3 bg-blue-50 rounded">
            <p className="text-sm font-medium text-blue-800">Required elements to address:</p>
            <ul className="list-disc pl-5 mt-1 text-sm text-blue-800">
              {requiredKeywords.map((keyword, index) => (
                <li key={`keyword-${index}`}>{keyword}</li>
              ))}
            </ul>
          </div>
        )}
        
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          disabled={submitted}
          className="w-full p-3 border border-gray-300 rounded min-h-[200px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type your answer here..."
        />
        
        <div className="mt-2 text-sm text-gray-500 flex justify-between">
          <span>Word count: {countWords(answer)}</span>
          <span>
            {countWords(answer) < minWords 
              ? `Need ${minWords - countWords(answer)} more words`
              : countWords(answer) > maxWords
                ? `${countWords(answer) - maxWords} words over limit`
                : 'Word count acceptable'}
          </span>
        </div>
      </div>

      {!submitted ? (
        <button
          onClick={handleSubmit}
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${
            !answer.trim() || countWords(answer) < minWords 
              ? 'opacity-50 cursor-not-allowed' 
              : ''
          }`}
          disabled={!answer.trim() || countWords(answer) < minWords}
        >
          Submit
        </button>
      ) : showFeedback && feedback ? (
        <div className="mt-4 p-3 rounded bg-blue-100">
          <h4 className="font-medium text-blue-800 mb-2">Feedback</h4>
          
          <div className="space-y-2">
            <p className={feedback.meetsMinWords ? 'text-green-600' : 'text-red-600'}>
              {feedback.meetsMinWords 
                ? '✓ Meets minimum word count' 
                : `✗ Below minimum word count (${minWords})`}
            </p>
            
            <p className={feedback.meetsMaxWords ? 'text-green-600' : 'text-red-600'}>
              {feedback.meetsMaxWords 
                ? '✓ Within maximum word limit' 
                : `✗ Exceeds maximum word count (${maxWords})`}
            </p>
            
            {requiredKeywords.length > 0 && (
              <div>
                <p className="font-medium mt-2">Required elements:</p>
                <ul className="list-disc pl-5">
                  {feedback.keywordsFound.map((keyword, index) => (
                    <li key={`found-${index}`} className="text-green-600">
                      ✓ {keyword}
                    </li>
                  ))}
                  {feedback.keywordsMissing.map((keyword, index) => (
                    <li key={`missing-${index}`} className="text-red-600">
                      ✗ {keyword} (not addressed)
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {exercise.correct_answer && exercise.correct_answer.length > 0 && (
              <div className="mt-3 pt-3 border-t border-blue-200">
                <p className="font-medium">Sample answer elements:</p>
                <ul className="list-disc pl-5 mt-1">
                  {exercise.correct_answer.map((point, index) => (
                    <li key={`point-${index}`}>{point}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default LongAnswer; 