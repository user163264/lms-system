'use client';

import React, { useState, useEffect, useMemo } from 'react';
import InteractiveExercise, { InteractiveExerciseProps } from './base/InteractiveExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface WordScrambleExerciseProps extends Omit<InteractiveExerciseProps, 'exercise'> {
  exercise: Exercise;
}

// Define the shape of our game state
interface GameState {
  originalWords: string[];
  shuffledWords: string[];
  wordIds: string[];
  wordStatus: Record<string, boolean>;
  arrangement: (string | null)[];
  slotWordIds: (string | null)[];
  selectedWord: string | null;
  isShuffled: boolean;
}

/**
 * Word Scramble Exercise Component
 * 
 * Component for exercises where users reorder scrambled words to form correct sentences.
 */
const WordScrambleExercise: React.FC<WordScrambleExerciseProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  
  // Initialize game state
  const [gameState, setGameState] = useState<GameState>(() => {
    // Get original words from the sentence
    const originalWords = exercise.sentence?.split(/\s+/).filter(word => word.length > 0) || [];
    
    // Create unique IDs for each word
    const wordIds = originalWords.map((word, index) => `${word}-${index}`);
    
    // Create a map to track which words are used
    const wordStatus: Record<string, boolean> = {};
    wordIds.forEach(id => {
      wordStatus[id] = false; // false = not used
    });
    
    return {
      originalWords,
      shuffledWords: [...originalWords], // Will be shuffled after initial render
      wordIds,
      wordStatus,
      arrangement: Array(originalWords.length).fill(null),
      slotWordIds: Array(originalWords.length).fill(null),
      selectedWord: null,
      isShuffled: false
    };
  });
  
  // Shuffle words client-side after initial render to avoid hydration mismatches
  useEffect(() => {
    if (!gameState.isShuffled && gameState.originalWords.length > 0) {
      const shuffledWords = [...gameState.originalWords];
      
      // Fisher-Yates shuffle algorithm
      for (let i = shuffledWords.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledWords[i], shuffledWords[j]] = [shuffledWords[j], shuffledWords[i]];
      }
      
      setGameState(prev => ({
        ...prev,
        shuffledWords,
        isShuffled: true
      }));
    }
  }, [gameState.isShuffled, gameState.originalWords]);
  
  // Update context when arrangement changes
  useEffect(() => {
    // Get the current arrangement of words
    const currentArrangement = gameState.arrangement
      .map((wordId, index) => {
        if (wordId === null) return null;
        // Extract the word from the ID (remove the index part)
        const wordWithIndex = gameState.wordIds.indexOf(wordId);
        return wordWithIndex >= 0 ? gameState.originalWords[wordWithIndex] : null;
      })
      .filter(Boolean); // Remove nulls
    
    // Only update if we have some words placed
    if (currentArrangement.length > 0) {
      updateAnswer(currentArrangement.join(' '));
    }
  }, [gameState.arrangement, gameState.wordIds, gameState.originalWords, updateAnswer]);
  
  // Handle word selection
  const handleSelectWord = (wordId: string) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    // Toggle selection
    setGameState(prev => ({
      ...prev,
      selectedWord: prev.selectedWord === wordId ? null : wordId
    }));
  };
  
  // Handle placing a word in a slot
  const handlePlaceWord = (slotIndex: number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED || gameState.selectedWord === null) return;
    
    setGameState(prev => {
      // Create new state objects (don't mutate existing state)
      const newArrangement = [...prev.arrangement];
      const newSlotWordIds = [...prev.slotWordIds];
      const newWordStatus = { ...prev.wordStatus };
      
      // If there's already a word in this slot, make it available again
      if (newSlotWordIds[slotIndex] !== null) {
        const wordId = newSlotWordIds[slotIndex];
        if (wordId !== null) {
          newWordStatus[wordId] = false;
        }
      }
      
      // Place the selected word in the slot
      newArrangement[slotIndex] = gameState.selectedWord;
      newSlotWordIds[slotIndex] = gameState.selectedWord;
      newWordStatus[gameState.selectedWord] = true;
      
      return {
        ...prev,
        arrangement: newArrangement,
        slotWordIds: newSlotWordIds,
        wordStatus: newWordStatus,
        selectedWord: null // Deselect after placing
      };
    });
  };
  
  // Handle removing a word from a slot
  const handleRemoveWord = (slotIndex: number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    setGameState(prev => {
      // If the slot is empty, do nothing
      if (prev.slotWordIds[slotIndex] === null) return prev;
      
      // Create new state objects
      const newArrangement = [...prev.arrangement];
      const newSlotWordIds = [...prev.slotWordIds];
      const newWordStatus = { ...prev.wordStatus };
      
      // Mark the word as available again
      const wordId = prev.slotWordIds[slotIndex];
      if (wordId !== null) {
        newWordStatus[wordId] = false;
      }
      
      // Clear the slot
      newArrangement[slotIndex] = null;
      newSlotWordIds[slotIndex] = null;
      
      return {
        ...prev,
        arrangement: newArrangement,
        slotWordIds: newSlotWordIds,
        wordStatus: newWordStatus
      };
    });
  };
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Check if all slots are filled
    if (gameState.arrangement.some(slot => slot === null) || 
        state.submissionStatus === SubmissionStatus.SUBMITTING) {
      return;
    }
    
    await submitAnswer();
  };
  
  // Handle reset
  const handleReset = () => {
    setGameState(prev => ({
      ...prev,
      arrangement: Array(prev.originalWords.length).fill(null),
      slotWordIds: Array(prev.originalWords.length).fill(null),
      wordStatus: Object.fromEntries(prev.wordIds.map(id => [id, false])),
      selectedWord: null,
    }));
    resetExercise();
  };
  
  // Determine if the form is disabled
  const isDisabled = state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = 
    gameState.arrangement.some(slot => slot === null) || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;

  return (
    <InteractiveExercise
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4" suppressHydrationWarning>
        {/* Word slots for arranging the sentence */}
        <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 min-h-24">
          <div className="flex flex-wrap gap-2">
            {gameState.arrangement.map((wordId, slotIndex) => (
              <div 
                key={`slot-${slotIndex}`}
                onClick={() => wordId ? handleRemoveWord(slotIndex) : handlePlaceWord(slotIndex)}
                className={`
                  h-10 min-w-24 flex items-center justify-center border-2 rounded px-3 py-1
                  ${wordId 
                    ? 'bg-white border-blue-500 cursor-pointer' 
                    : 'border-dashed border-gray-400 bg-gray-100 hover:bg-gray-200'
                  }
                  ${gameState.selectedWord && !wordId ? 'bg-blue-100 border-blue-500' : ''}
                  ${isDisabled ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'}
                `}
              >
                {wordId && (
                  <span className="font-medium">
                    {gameState.originalWords[gameState.wordIds.indexOf(wordId)]}
                  </span>
                )}
                {!wordId && (
                  <span className="text-gray-500">
                    {gameState.selectedWord ? 'Place here' : 'Empty'}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
        
        {/* Word bank */}
        <div className="mt-4">
          <h4 className="font-medium mb-2">Available Words:</h4>
          <div className="flex flex-wrap gap-2">
            {gameState.shuffledWords.map((word, wordIndex) => {
              const wordId = gameState.wordIds[gameState.originalWords.indexOf(word)];
              const isUsed = gameState.wordStatus[wordId];
              
              return (
                <button
                  key={`word-${wordId}`}
                  type="button" // Prevent form submission
                  disabled={isUsed || isDisabled}
                  onClick={() => !isUsed && handleSelectWord(wordId)}
                  className={`
                    border rounded px-3 py-1 font-medium transition-colors
                    ${isUsed ? 'bg-gray-200 text-gray-500 border-gray-300' : 'bg-white border-gray-300'}
                    ${gameState.selectedWord === wordId ? 'bg-blue-100 border-blue-500' : ''}
                    ${isDisabled ? 'opacity-70 cursor-not-allowed' : 'hover:bg-blue-50 hover:border-blue-300'}
                  `}
                >
                  {word}
                </button>
              );
            })}
          </div>
        </div>
        
        {/* Instructions */}
        <div className="text-sm text-gray-600 mt-4">
          <p>
            <strong>Instructions:</strong> Click on a word from the word bank, then click on an empty slot to place it. 
            Click on a placed word to remove it.
          </p>
        </div>
        
        {/* Submit and Reset buttons */}
        <div className="flex space-x-2 pt-4">
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
    </InteractiveExercise>
  );
};

export default WordScrambleExercise; 