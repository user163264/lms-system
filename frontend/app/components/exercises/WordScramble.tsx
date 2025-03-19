'use client';

import React, { useState, useEffect, useMemo } from 'react';

export interface WordScrambleProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    sentence: string;
    correct_answer: string[];
    max_score?: number;
  };
  onSubmit: (answer: string, exerciseId: number) => void;
  showFeedback?: boolean;
}

// Define the shape of our game state to avoid TypeScript errors
interface GameState {
  initialWords: string[];
  wordIds: string[];
  wordStatus: Record<string, boolean>;
  arrangement: (string | null)[];
  slotWordIds: (string | null)[];
  selectedWord: string | null;
  submitted: boolean;
  isCorrect: boolean;
  showInstructions: boolean;
  isShuffled: boolean; // Track if words have been shuffled
}

/**
 * Word Scramble Exercise Component
 * 
 * This component renders a sentence with scrambled words that students
 * need to rearrange into the correct order.
 */
const WordScramble: React.FC<WordScrambleProps> = ({
  exercise,
  onSubmit,
  showFeedback = false,
}) => {
  // Component state - defined here to avoid recreation in effects
  const [gameState, setGameState] = useState<GameState>(() => {
    // Initialize the game state once - put all initialization logic here
    const originalWords = exercise.sentence.split(/\s+/).filter(word => word.length > 0);
    
    // Create unique IDs for each word - for initial state, use words in original order
    // This ensures server and client render the same initial HTML
    const wordIds = originalWords.map((word, index) => `${word}-${index}`);
    
    // Create a map to track which words are used
    const wordStatus: Record<string, boolean> = {};
    wordIds.forEach(id => {
      wordStatus[id] = false; // false = not used
    });
    
    return {
      initialWords: originalWords, // Store the original words unshuffled
      wordIds,
      wordStatus,
      arrangement: Array(originalWords.length).fill(null),
      slotWordIds: Array(originalWords.length).fill(null),
      selectedWord: null,
      submitted: false,
      isCorrect: false,
      showInstructions: false,
      isShuffled: false // Initially not shuffled
    };
  });
  
  // Shuffle words client-side only after initial render to avoid hydration mismatch
  useEffect(() => {
    if (!gameState.isShuffled) {
      // Get the original words
      const words = [...gameState.initialWords];
      
      // Shuffle the words
      for (let i = words.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [words[i], words[j]] = [words[j], words[i]];
      }
      
      // Make sure the shuffled order is different from the original
      if (words.join(' ') === exercise.sentence) {
        if (words.length >= 2) {
          [words[0], words[1]] = [words[1], words[0]];
        }
      }
      
      // Create unique IDs for each word
      const wordIds = words.map((word, index) => `${word}-${index}`);
      
      // Create a map to track which words are used
      const wordStatus: Record<string, boolean> = {};
      wordIds.forEach(id => {
        wordStatus[id] = false; // false = not used
      });
      
      // Update state with shuffled words
      setGameState(prev => ({
        ...prev,
        initialWords: words,
        wordIds,
        wordStatus,
        isShuffled: true
      }));
    }
  }, [exercise.sentence, gameState.isShuffled]);
  
  // Destructure the game state for easier access
  const {
    initialWords,
    wordIds,
    wordStatus,
    arrangement,
    slotWordIds,
    selectedWord,
    submitted,
    isCorrect,
    showInstructions
  } = gameState;
  
  // Toggle instructions visibility
  const toggleInstructions = () => {
    setGameState(prev => ({
      ...prev,
      showInstructions: !prev.showInstructions
    }));
  };
  
  // All handler functions update the state in a single setGameState call
  // to avoid multiple updates that could cause rerenders
  
  // Select a word from the available words
  const handleSelectWord = (wordId: string) => {
    if (submitted || wordStatus[wordId]) return;
    
    setGameState(prev => ({
      ...prev,
      selectedWord: prev.selectedWord === wordId ? null : wordId
    }));
  };
  
  // Place a word in a slot
  const handlePlaceWord = (slotIndex: number) => {
    if (submitted || !selectedWord || wordStatus[selectedWord]) return;
    
    // Get the actual word from the ID
    const word = selectedWord.split('-')[0];
    
    // Check if the slot already has a word
    const existingWordId = slotWordIds[slotIndex];
    
    // Create new state objects to avoid mutations
    const newArrangement = [...arrangement];
    newArrangement[slotIndex] = word;
    
    const newSlotWordIds = [...slotWordIds];
    newSlotWordIds[slotIndex] = selectedWord;
    
    const newWordStatus = { ...wordStatus };
    newWordStatus[selectedWord] = true; // Mark as used
    
    // If replacing a word in a slot, mark it as unused
    if (existingWordId) {
      newWordStatus[existingWordId] = false;
    }
    
    // Update the entire state at once
    setGameState(prev => ({
      ...prev,
      arrangement: newArrangement,
      slotWordIds: newSlotWordIds,
      wordStatus: newWordStatus,
      selectedWord: null
    }));
  };
  
  // Remove a word from a slot
  const handleRemoveWord = (slotIndex: number) => {
    if (submitted) return;
    
    const wordId = slotWordIds[slotIndex];
    if (!wordId) return;
    
    // Create new state objects to avoid mutations
    const newArrangement = [...arrangement];
    newArrangement[slotIndex] = null;
    
    const newSlotWordIds = [...slotWordIds];
    newSlotWordIds[slotIndex] = null;
    
    const newWordStatus = { ...wordStatus };
    newWordStatus[wordId] = false;
    
    // Update the entire state at once
    setGameState(prev => ({
      ...prev,
      arrangement: newArrangement,
      slotWordIds: newSlotWordIds,
      wordStatus: newWordStatus
    }));
  };
  
  // Submit the answer
  const handleSubmit = () => {
    if (arrangement.includes(null)) return;
    
    const attemptedAnswer = arrangement.join(' ');
    const correctAnswer = exercise.correct_answer[0] || exercise.sentence;
    const isAnswerCorrect = attemptedAnswer.toLowerCase() === correctAnswer.toLowerCase();
    
    setGameState(prev => ({
      ...prev,
      submitted: true,
      isCorrect: isAnswerCorrect
    }));
    
    onSubmit(attemptedAnswer, exercise.id);
  };
  
  // Reset the exercise
  const handleReset = () => {
    if (submitted) return;
    
    const resetStatus: Record<string, boolean> = {};
    wordIds.forEach(id => {
      resetStatus[id] = false;
    });
    
    setGameState(prev => ({
      ...prev,
      arrangement: Array(initialWords.length).fill(null),
      slotWordIds: Array(initialWords.length).fill(null),
      wordStatus: resetStatus,
      selectedWord: null
    }));
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-medium">Word Scramble</h3>
        <button 
          onClick={toggleInstructions}
          className="text-sm text-blue-600 hover:text-blue-800 flex items-center"
        >
          {showInstructions ? 'Hide Instructions' : 'Show Instructions'} 
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="ml-1" viewBox="0 0 16 16">
            <path d={showInstructions 
              ? "M7.646 4.646a.5.5 0 0 1 .708 0L12 8.293l3.646-3.647a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 0-.708z"
              : "M7.646 4.646a.5.5 0 0 1 .708 0l3.646 3.647 3.646-3.647a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 0-.708z"} 
            />
          </svg>
        </button>
      </div>
      
      {showInstructions && (
        <div className="bg-blue-50 p-4 rounded-lg mb-4 text-sm">
          <h4 className="font-medium text-blue-800 mb-2">How to Use</h4>
          <ol className="list-decimal list-inside space-y-2 text-blue-900">
            <li><strong>Select a word</strong> from the word bank below by clicking on it</li>
            <li><strong>Place the word</strong> by clicking on a numbered slot</li>
            <li><strong>Remove a word</strong> by clicking on it in a slot</li>
            <li><strong>Replace a word</strong> by selecting a new word and clicking on a filled slot</li>
            <li><strong>Submit</strong> your answer once all slots are filled</li>
            <li><strong>Reset</strong> if you want to start over</li>
          </ol>
          <p className="mt-2 text-blue-700">The goal is to arrange the words to form a correct, meaningful sentence.</p>
        </div>
      )}
      
      <p className="text-gray-600 mb-4">
        {!gameState.isShuffled ? 'Loading word bank...' : 'Select a word from the list below, then click on a numbered slot to place it in the sentence.'}
      </p>
      
      <div className="mb-4">
        <p className="mb-3 font-medium">{exercise.question}</p>
        
        {/* Word slots - where words will be placed in order */}
        <div className="mb-6 bg-gray-50 border border-gray-300 rounded p-4">
          <div className="flex flex-wrap gap-2">
            {arrangement.map((word, index) => (
              <div 
                key={`slot-${index}`}
                onClick={() => word ? handleRemoveWord(index) : handlePlaceWord(index)}
                className={`
                  relative min-w-[80px] h-10 flex items-center justify-center 
                  px-3 py-1 rounded-lg border-2 
                  ${submitted 
                    ? isCorrect 
                      ? 'bg-green-50 border-green-300' 
                      : 'bg-red-50 border-red-300'
                    : word 
                      ? 'bg-white border-gray-300 cursor-pointer hover:bg-gray-100' 
                      : selectedWord 
                        ? 'bg-blue-50 border-blue-400 cursor-pointer' 
                        : 'bg-gray-100 border-dashed border-gray-400'
                  }
                `}
                data-testid={`word-slot-${index}`}
              >
                {word || (
                  <span className="text-gray-400">
                    {selectedWord ? '+ Place here' : `Slot ${index + 1}`}
                  </span>
                )}
                <div className="absolute -top-3 -left-3 w-6 h-6 flex items-center justify-center bg-gray-200 rounded-full text-xs font-medium">
                  {index + 1}
                </div>
              </div>
            ))}
          </div>
          
          {!submitted && selectedWord && (
            <div className="mt-2 text-sm text-blue-600">
              Click on a slot to place &quot;{selectedWord.split('-')[0]}&quot; or 
              <button 
                onClick={() => setGameState(prev => ({ ...prev, selectedWord: null }))}
                className="underline ml-1 font-medium"
              >
                cancel selection
              </button>
            </div>
          )}
        </div>
        
        {/* Available words - display only after client-side shuffling */}
        {gameState.isShuffled && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Available words:</h4>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
              {wordIds.map((wordId) => {
                const word = wordId.split('-')[0];
                const isUsed = wordStatus[wordId];
                
                return (
                  <div key={wordId} className="min-h-[38px]">
                    {!isUsed && (
                      <button
                        onClick={() => handleSelectWord(wordId)}
                        disabled={submitted || isUsed}
                        className={`
                          w-full py-1 px-3 rounded-lg border 
                          ${submitted 
                            ? 'bg-gray-100 border-gray-300 cursor-not-allowed'
                            : selectedWord === wordId
                              ? 'bg-blue-100 border-blue-500'
                              : 'bg-white border-gray-300 hover:bg-gray-100'
                          }
                        `}
                      >
                        {word}
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
      
      {!submitted ? (
        <div className="flex space-x-3">
          <button
            onClick={handleSubmit}
            disabled={arrangement.includes(null) || !gameState.isShuffled}
            className={`
              bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors
              ${(arrangement.includes(null) || !gameState.isShuffled) ? 'opacity-50 cursor-not-allowed' : ''}
            `}
            data-testid="submit-button"
          >
            Submit
          </button>
          <button
            onClick={handleReset}
            disabled={!gameState.isShuffled}
            className={`
              border border-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-100 transition-colors
              ${!gameState.isShuffled ? 'opacity-50 cursor-not-allowed' : ''}
            `}
            data-testid="reset-button"
          >
            Reset
          </button>
        </div>
      ) : showFeedback ? (
        <div 
          className={`mt-4 p-3 rounded ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}
          data-testid="feedback-panel"
        >
          {isCorrect 
            ? '✓ Correct! You arranged the words in the right order.' 
            : (
              <div>
                <p>✗ Incorrect. The correct sentence is:</p>
                <p className="mt-2 font-medium">{exercise.sentence}</p>
              </div>
            )
          }
        </div>
      ) : null}
    </div>
  );
};

export default WordScramble; 