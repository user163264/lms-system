'use client';

import React, { useState, useEffect } from 'react';
import InteractiveExercise, { InteractiveExerciseProps } from './base/InteractiveExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface MatchingWordsExerciseProps extends Omit<InteractiveExerciseProps, 'exercise'> {
  exercise: Exercise;
}

/**
 * Matching Words Exercise Component
 * 
 * Component for exercises where users match items from one list to items in another list.
 */
const MatchingWordsExercise: React.FC<MatchingWordsExerciseProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  
  // Initialize selections with -1 (no selection) for each item in column A
  const [selections, setSelections] = useState<number[]>(
    Array((exercise.items_a?.length || 0)).fill(-1)
  );
  
  // Track the shuffled order of items in column B
  const [shuffledItemsB, setShuffledItemsB] = useState<string[]>([]);
  const [shuffledIndices, setShuffledIndices] = useState<number[]>([]);

  // Shuffle items B on component mount
  useEffect(() => {
    if (!exercise.items_b || exercise.items_b.length === 0) return;
    
    // Create array of indices for items_b
    const indices = exercise.items_b.map((_, index) => index);
    
    // Fisher-Yates shuffle algorithm
    const shuffled = [...indices];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    
    setShuffledIndices(shuffled);
    setShuffledItemsB(shuffled.map(index => exercise.items_b?.[index] || ''));
    
    // Reset selections when exercise changes
    setSelections(Array((exercise.items_a?.length || 0)).fill(-1));
  }, [exercise]);

  // Update context when selections change
  useEffect(() => {
    updateAnswer(selections);
  }, [selections, updateAnswer]);

  // Handle selecting a match for an item in column A
  const handleSelection = (itemAIndex: number, itemBIndex: number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    const newSelections = [...selections];
    // Store the original index (before shuffling) of the selected item B
    newSelections[itemAIndex] = itemBIndex === -1 ? -1 : shuffledIndices[itemBIndex];
    setSelections(newSelections);
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (selections.includes(-1) || state.submissionStatus === SubmissionStatus.SUBMITTING) return;
    
    await submitAnswer();
  };

  // Handle reset
  const handleReset = () => {
    setSelections(Array((exercise.items_a?.length || 0)).fill(-1));
    resetExercise();
  };

  // Determine if the form is disabled
  const isDisabled = state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = 
    selections.includes(-1) || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;

  // Calculate which matches are correct if feedback is available
  const getCorrectMatches = () => {
    if (!state.feedback || !exercise.correct_matches) return [];
    return selections.map((selection, index) => 
      selection === exercise.correct_matches?.[index]
    );
  };

  const correctMatches = getCorrectMatches();

  return (
    <InteractiveExercise
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4" suppressHydrationWarning>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
          {/* Column A */}
          <div className="space-y-4">
            <h4 className="font-medium border-b pb-2">Column A</h4>
            {exercise.items_a?.map((item, index) => (
              <div 
                key={`a-${index}`} 
                className={`p-3 border rounded ${
                  state.submissionStatus === SubmissionStatus.SUBMITTED ? 
                    (correctMatches[index] ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50') : 
                    'border-gray-300'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span>{item}</span>
                  <div className="ml-4">
                    <select
                      value={selections[index]}
                      onChange={(e) => {
                        const selectedIndex = parseInt(e.target.value);
                        handleSelection(index, selectedIndex);
                      }}
                      disabled={isDisabled}
                      className={`border rounded p-1 ${
                        selections[index] === -1 ? 'text-gray-400' : ''
                      }`}
                      suppressHydrationWarning
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
          
          {/* Column B */}
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
        
        {/* Additional feedback for matching exercises */}
        {showFeedback && state.submissionStatus === SubmissionStatus.SUBMITTED && state.feedback && correctMatches.includes(false) && (
          <div className="mt-4 p-3 rounded border border-blue-200 bg-blue-50">
            <p className="font-medium">Correct matches:</p>
            <ul className="list-disc pl-5 mt-1">
              {exercise.items_a?.map((item, index) => (
                <li key={`correct-${index}`} className={correctMatches[index] ? 'text-green-600' : 'text-red-600'}>
                  {item} → {exercise.items_b?.[exercise.correct_matches?.[index] || 0]}
                </li>
              ))}
            </ul>
          </div>
        )}
      </form>
    </InteractiveExercise>
  );
};

export default MatchingWordsExercise; 