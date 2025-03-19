'use client';

import React, { useState, useEffect } from 'react';

export interface MatchingWordsProps {
  exercise: {
    id: number;
    exercise_type: string;
    items_a: string[];
    items_b: string[];
    correct_matches: number[]; // indices of items_b that match with items_a in order
    max_score?: number;
  };
  onSubmit: (answer: number[], exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Matching Words Exercise Component
 * 
 * This component renders a matching exercise where students
 * match items from column A with their corresponding items in column B.
 */
const MatchingWords: React.FC<MatchingWordsProps> = ({
  exercise,
  onSubmit,
  showFeedback = false,
}) => {
  const [selections, setSelections] = useState<number[]>(
    Array(exercise.items_a.length).fill(-1)
  );
  const [submitted, setSubmitted] = useState(false);
  const [correctMatches, setCorrectMatches] = useState<boolean[]>([]);
  const [shuffledItemsB, setShuffledItemsB] = useState<string[]>([]);
  const [shuffledIndices, setShuffledIndices] = useState<number[]>([]);

  // Shuffle items B on component mount
  useEffect(() => {
    const shuffle = [...exercise.items_b.map((_, index) => index)];
    // Fisher-Yates shuffle algorithm
    for (let i = shuffle.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffle[i], shuffle[j]] = [shuffle[j], shuffle[i]];
    }
    
    setShuffledIndices(shuffle);
    setShuffledItemsB(shuffle.map(index => exercise.items_b[index]));
  }, [exercise.items_b]);

  const handleSelection = (itemAIndex: number, itemBIndex: number) => {
    if (submitted) return;
    
    const newSelections = [...selections];
    newSelections[itemAIndex] = shuffledIndices[itemBIndex];
    setSelections(newSelections);
  };

  const handleSubmit = () => {
    if (selections.includes(-1)) return; // Ensure all have been matched
    
    // Check which matches are correct
    const correctness = selections.map(
      (selection, index) => selection === exercise.correct_matches[index]
    );
    
    setCorrectMatches(correctness);
    setSubmitted(true);
    onSubmit(selections, exercise.id);
  };

  const getScore = () => {
    return correctMatches.filter(match => match).length;
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <h3 className="text-lg font-medium mb-2">Matching Words</h3>
      <p className="text-gray-600 mb-4">Match each word in Column A with its corresponding word in Column B.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
        <div className="space-y-4">
          <h4 className="font-medium border-b pb-2">Column A</h4>
          {exercise.items_a.map((item, index) => (
            <div 
              key={`a-${index}`} 
              className={`p-3 border rounded ${
                submitted ? 
                  (correctMatches[index] ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50') : 
                  'border-gray-300'
              }`}
            >
              <div className="flex justify-between items-center">
                <span>{item}</span>
                <div className="ml-4">
                  <select
                    value={selections[index]}
                    onChange={(e) => handleSelection(index, parseInt(e.target.value))}
                    disabled={submitted}
                    className={`border rounded p-1 ${
                      selections[index] === -1 ? 'text-gray-400' : ''
                    }`}
                  >
                    <option value="-1">Select a match</option>
                    {shuffledItemsB.map((item, bIndex) => (
                      <option key={`option-${bIndex}`} value={bIndex}>
                        {item}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="space-y-4">
          <h4 className="font-medium border-b pb-2">Column B</h4>
          {shuffledItemsB.map((item, index) => (
            <div 
              key={`b-${index}`}
              className="p-3 border border-gray-300 rounded"
            >
              {item}
            </div>
          ))}
        </div>
      </div>
      
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${
            selections.includes(-1) ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          disabled={selections.includes(-1)}
        >
          Submit
        </button>
      ) : showFeedback ? (
        <div className="mt-4 p-3 rounded bg-blue-100 text-blue-800">
          <p>You got {getScore()} out of {exercise.items_a.length} matches correct!</p>
          {correctMatches.includes(false) && (
            <div className="mt-2">
              <p className="font-medium">Correct matches:</p>
              <ul className="list-disc pl-5 mt-1">
                {exercise.items_a.map((item, index) => (
                  <li key={`correct-${index}`}>
                    {item} → {exercise.items_b[exercise.correct_matches[index]]}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
};

export default MatchingWords; 