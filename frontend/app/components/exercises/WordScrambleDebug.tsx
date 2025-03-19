'use client';

import React, { useState, useEffect, useMemo, useRef } from 'react';

// Debug Logger utility
const DebugLogger = {
  enabled: true,
  logStyle: 'background: #f0f0f0; color: #0066cc; padding: 2px 4px; border-radius: 2px;',
  warnStyle: 'background: #fff3cd; color: #856404; padding: 2px 4px; border-radius: 2px;',
  errorStyle: 'background: #f8d7da; color: #721c24; padding: 2px 4px; border-radius: 2px;',
  
  log: (component: string, message: string, data?: any) => {
    if (!DebugLogger.enabled) return;
    console.log(`%c[${component}] ${message}`, DebugLogger.logStyle, data || '');
  },
  
  warn: (component: string, message: string, data?: any) => {
    if (!DebugLogger.enabled) return;
    console.warn(`%c[${component}] ${message}`, DebugLogger.warnStyle, data || '');
  },
  
  error: (component: string, message: string, data?: any) => {
    if (!DebugLogger.enabled) return;
    console.error(`%c[${component}] ${message}`, DebugLogger.errorStyle, data || '');
  },
  
  startTimer: (label: string) => {
    if (!DebugLogger.enabled) return;
    console.time(`⏱️ ${label}`);
  },
  
  endTimer: (label: string) => {
    if (!DebugLogger.enabled) return;
    console.timeEnd(`⏱️ ${label}`);
  }
};

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
  debugMode: boolean;
}

/**
 * Debug Word Scramble Exercise Component
 * 
 * This is an enhanced version of the WordScramble component with extensive
 * debugging capabilities to help identify and fix issues.
 */
const WordScrambleDebug: React.FC<WordScrambleProps> = ({
  exercise,
  onSubmit,
  showFeedback = false,
}) => {
  // Render counter for debugging
  const renderCount = useRef(0);
  
  // Debug view state
  const [debugView, setDebugView] = useState({
    showStatePanel: false,
    showTimingInfo: false,
    showEventLog: false,
    logEntries: [] as {time: string, message: string, type: 'log' | 'event' | 'warning' | 'error'}[]
  });
  
  // Add to debug log
  const addLogEntry = (message: string, type: 'log' | 'event' | 'warning' | 'error' = 'log') => {
    if (!debugView.showEventLog) return;
    
    const time = new Date().toLocaleTimeString();
    setDebugView(prev => ({
      ...prev,
      logEntries: [...prev.logEntries, {time, message, type}].slice(-50) // Keep last 50 entries
    }));
  };
  
  // Component state - defined here to avoid recreation in effects
  const [gameState, setGameState] = useState<GameState>(() => {
    DebugLogger.log('WordScramble', 'Initializing game state');
    DebugLogger.startTimer('Initial State Creation');
    
    // Initialize the game state once - put all initialization logic here
    const originalWords = exercise.sentence.split(/\s+/).filter(word => word.length > 0);
    
    DebugLogger.log('WordScramble', `Original sentence parsed into ${originalWords.length} words:`, originalWords);
    
    // Create a copy of the original words
    const words = [...originalWords];
    
    // Shuffle the words
    for (let i = words.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [words[i], words[j]] = [words[j], words[i]];
    }
    
    DebugLogger.log('WordScramble', 'Words after shuffling:', words);
    
    // Make sure the shuffled order is different from the original
    if (words.join(' ') === exercise.sentence) {
      DebugLogger.warn('WordScramble', 'Shuffle resulted in same order as original, attempting fix');
      if (words.length >= 2) {
        [words[0], words[1]] = [words[1], words[0]];
        DebugLogger.log('WordScramble', 'Fixed by swapping first two words:', words);
      }
    }
    
    // Create unique IDs for each word
    const wordIds = words.map((word, index) => `${word}-${index}`);
    DebugLogger.log('WordScramble', 'Created word IDs:', wordIds);
    
    // Create a map to track which words are used
    const wordStatus: Record<string, boolean> = {};
    wordIds.forEach(id => {
      wordStatus[id] = false; // false = not used
    });
    
    DebugLogger.log('WordScramble', 'Initial word status map created:', wordStatus);
    DebugLogger.endTimer('Initial State Creation');
    
    return {
      initialWords: words,
      wordIds,
      wordStatus,
      arrangement: Array(words.length).fill(null),
      slotWordIds: Array(words.length).fill(null),
      selectedWord: null,
      submitted: false,
      isCorrect: false,
      showInstructions: false,
      debugMode: true
    };
  });
  
  // Track render count
  useEffect(() => {
    renderCount.current++;
    DebugLogger.log('WordScramble', `Component rendered (${renderCount.current} times)`);
    
    // Return cleanup function
    return () => {
      DebugLogger.log('WordScramble', 'Component unmounting');
    };
  });
  
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
    showInstructions,
    debugMode
  } = gameState;
  
  // Debug state snapshot - create a memoized snapshot of current state for debugging
  const stateSnapshot = useMemo(() => {
    return {
      initialWords,
      wordIds: wordIds.length > 10 ? [...wordIds.slice(0, 5), '...', ...wordIds.slice(-5)] : wordIds,
      wordStatus,
      arrangement,
      slotWordIds,
      selectedWord,
      submitted,
      isCorrect,
      showInstructions,
      debugMode,
      renderCount: renderCount.current
    };
  }, [
    initialWords, wordIds, wordStatus, 
    arrangement, slotWordIds, selectedWord, 
    submitted, isCorrect, showInstructions, debugMode
  ]);
  
  // Toggle instructions visibility
  const toggleInstructions = () => {
    DebugLogger.log('WordScramble', `Toggling instructions visibility from ${showInstructions} to ${!showInstructions}`);
    addLogEntry(`Instructions ${showInstructions ? 'hidden' : 'shown'}`, 'event');
    
    setGameState(prev => ({
      ...prev,
      showInstructions: !prev.showInstructions
    }));
  };
  
  // Toggle debug mode
  const toggleDebugMode = () => {
    DebugLogger.log('WordScramble', `Toggling debug mode`);
    
    setGameState(prev => ({
      ...prev,
      debugMode: !prev.debugMode
    }));
  };
  
  // Toggle debug panels
  const toggleDebugPanel = (panel: 'state' | 'timing' | 'log') => {
    DebugLogger.log('WordScramble', `Toggling debug panel: ${panel}`);
    
    setDebugView(prev => {
      if (panel === 'state') {
        return { ...prev, showStatePanel: !prev.showStatePanel };
      } else if (panel === 'timing') {
        return { ...prev, showTimingInfo: !prev.showTimingInfo };
      } else {
        return { ...prev, showEventLog: !prev.showEventLog };
      }
    });
  };
  
  // All handler functions update the state in a single setGameState call
  // to avoid multiple updates that could cause rerenders
  
  // Select a word from the available words
  const handleSelectWord = (wordId: string) => {
    DebugLogger.startTimer('handleSelectWord');
    
    if (submitted || wordStatus[wordId]) {
      DebugLogger.warn('WordScramble', `Word selection blocked for "${wordId}" - submitted: ${submitted}, isUsed: ${wordStatus[wordId]}`);
      DebugLogger.endTimer('handleSelectWord');
      return;
    }
    
    const word = wordId.split('-')[0];
    DebugLogger.log('WordScramble', `Word "${word}" (ID: ${wordId}) selected/deselected`);
    addLogEntry(`Word "${word}" ${selectedWord === wordId ? 'deselected' : 'selected'}`, 'event');
    
    setGameState(prev => ({
      ...prev,
      selectedWord: prev.selectedWord === wordId ? null : wordId
    }));
    
    DebugLogger.endTimer('handleSelectWord');
  };
  
  // Place a word in a slot
  const handlePlaceWord = (slotIndex: number) => {
    DebugLogger.startTimer('handlePlaceWord');
    
    if (submitted) {
      DebugLogger.warn('WordScramble', `Word placement blocked - exercise already submitted`);
      DebugLogger.endTimer('handlePlaceWord');
      return;
    }
    
    if (!selectedWord) {
      DebugLogger.warn('WordScramble', `Word placement blocked - no word selected`);
      DebugLogger.endTimer('handlePlaceWord');
      return;
    }
    
    if (wordStatus[selectedWord]) {
      DebugLogger.warn('WordScramble', `Word placement blocked - selected word "${selectedWord}" is already used`);
      DebugLogger.endTimer('handlePlaceWord');
      return;
    }
    
    // Get the actual word from the ID
    const word = selectedWord.split('-')[0];
    
    // Check if the slot already has a word
    const existingWordId = slotWordIds[slotIndex];
    
    DebugLogger.log('WordScramble', `Placing word "${word}" (ID: ${selectedWord}) in slot ${slotIndex + 1}${
      existingWordId ? ` (replacing "${existingWordId.split('-')[0]}")` : ''
    }`);
    
    addLogEntry(`Word "${word}" placed in slot ${slotIndex + 1}${
      existingWordId ? ` (replacing "${existingWordId.split('-')[0]}")` : ''
    }`, 'event');
    
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
      DebugLogger.log('WordScramble', `Word "${existingWordId.split('-')[0]}" (ID: ${existingWordId}) marked as unused`);
    }
    
    // Update the entire state at once
    setGameState(prev => ({
      ...prev,
      arrangement: newArrangement,
      slotWordIds: newSlotWordIds,
      wordStatus: newWordStatus,
      selectedWord: null
    }));
    
    DebugLogger.endTimer('handlePlaceWord');
  };
  
  // Remove a word from a slot
  const handleRemoveWord = (slotIndex: number) => {
    DebugLogger.startTimer('handleRemoveWord');
    
    if (submitted) {
      DebugLogger.warn('WordScramble', `Word removal blocked - exercise already submitted`);
      DebugLogger.endTimer('handleRemoveWord');
      return;
    }
    
    const wordId = slotWordIds[slotIndex];
    if (!wordId) {
      DebugLogger.warn('WordScramble', `Word removal blocked - no word in slot ${slotIndex + 1}`);
      DebugLogger.endTimer('handleRemoveWord');
      return;
    }
    
    const word = wordId.split('-')[0];
    DebugLogger.log('WordScramble', `Removing word "${word}" (ID: ${wordId}) from slot ${slotIndex + 1}`);
    addLogEntry(`Word "${word}" removed from slot ${slotIndex + 1}`, 'event');
    
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
    
    DebugLogger.endTimer('handleRemoveWord');
  };
  
  // Submit the answer
  const handleSubmit = () => {
    DebugLogger.startTimer('handleSubmit');
    
    if (arrangement.includes(null)) {
      DebugLogger.warn('WordScramble', `Submission blocked - not all slots are filled`);
      DebugLogger.endTimer('handleSubmit');
      return;
    }
    
    const attemptedAnswer = arrangement.join(' ');
    const correctAnswer = exercise.correct_answer[0] || exercise.sentence;
    const isAnswerCorrect = attemptedAnswer.toLowerCase() === correctAnswer.toLowerCase();
    
    DebugLogger.log('WordScramble', `Submitting answer: "${attemptedAnswer}"`);
    DebugLogger.log('WordScramble', `Correct answer: "${correctAnswer}"`);
    DebugLogger.log('WordScramble', `Is answer correct: ${isAnswerCorrect}`);
    
    addLogEntry(`Answer submitted: "${attemptedAnswer}"`, 'event');
    addLogEntry(`Answer is ${isAnswerCorrect ? 'correct! ✅' : 'incorrect ❌'}`, isAnswerCorrect ? 'log' : 'warning');
    
    setGameState(prev => ({
      ...prev,
      submitted: true,
      isCorrect: isAnswerCorrect
    }));
    
    onSubmit(attemptedAnswer, exercise.id);
    DebugLogger.endTimer('handleSubmit');
  };
  
  // Reset the exercise
  const handleReset = () => {
    DebugLogger.startTimer('handleReset');
    
    if (submitted) {
      DebugLogger.warn('WordScramble', `Reset blocked - exercise already submitted`);
      DebugLogger.endTimer('handleReset');
      return;
    }
    
    DebugLogger.log('WordScramble', 'Resetting exercise');
    addLogEntry('Exercise reset', 'event');
    
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
    
    DebugLogger.endTimer('handleReset');
  };
  
  // Count filled slots for debugging
  const filledSlots = arrangement.filter(Boolean).length;
  const emptySlots = arrangement.length - filledSlots;
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      {/* Debug Controls */}
      {debugMode && (
        <div className="bg-gray-800 text-white p-3 rounded-lg mb-4 text-xs">
          <div className="flex justify-between items-center mb-2">
            <h4 className="font-medium">Debug Controls</h4>
            <div className="space-x-2">
              <button
                onClick={() => toggleDebugPanel('state')}
                className={`px-2 py-1 rounded text-xs ${debugView.showStatePanel ? 'bg-blue-600' : 'bg-gray-600'}`}
              >
                State
              </button>
              <button
                onClick={() => toggleDebugPanel('timing')}
                className={`px-2 py-1 rounded text-xs ${debugView.showTimingInfo ? 'bg-blue-600' : 'bg-gray-600'}`}
              >
                Timing
              </button>
              <button
                onClick={() => toggleDebugPanel('log')}
                className={`px-2 py-1 rounded text-xs ${debugView.showEventLog ? 'bg-blue-600' : 'bg-gray-600'}`}
              >
                Event Log
              </button>
              <button
                onClick={toggleDebugMode}
                className="px-2 py-1 rounded text-xs bg-red-600"
              >
                Close Debug
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-4 gap-2 text-gray-300 mb-2">
            <div>Renders: <span className="text-white">{renderCount.current}</span></div>
            <div>Words: <span className="text-white">{initialWords.length}</span></div>
            <div>Filled: <span className="text-white">{filledSlots}/{arrangement.length}</span></div>
            <div>Selected: <span className="text-white">{selectedWord ? selectedWord.split('-')[0] : 'none'}</span></div>
          </div>
          
          {debugView.showStatePanel && (
            <div className="bg-gray-700 p-2 rounded mb-2 overflow-auto max-h-40">
              <pre className="text-xs text-gray-300">
                {JSON.stringify(stateSnapshot, null, 2)}
              </pre>
            </div>
          )}
          
          {debugView.showEventLog && (
            <div className="bg-gray-700 p-2 rounded mb-2 overflow-auto max-h-40">
              {debugView.logEntries.length === 0 ? (
                <p className="text-gray-400 text-xs">No events logged yet</p>
              ) : (
                <ul className="space-y-1 text-xs">
                  {debugView.logEntries.map((entry, i) => (
                    <li key={i} className={`
                      ${entry.type === 'error' ? 'text-red-300' : 
                        entry.type === 'warning' ? 'text-yellow-300' : 
                        entry.type === 'event' ? 'text-blue-300' : 'text-gray-300'}
                    `}>
                      <span className="text-gray-400">{entry.time}</span> {entry.message}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      )}
      
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center">
          <h3 className="text-lg font-medium">Word Scramble</h3>
          {!debugMode && (
            <button
              onClick={toggleDebugMode}
              className="ml-3 text-xs bg-gray-100 hover:bg-gray-200 text-gray-800 px-2 py-1 rounded-full"
            >
              Debug
            </button>
          )}
        </div>
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
        Select a word from the list below, then click on a numbered slot to place it in the sentence.
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
                data-debug-has-word={word ? "true" : "false"}
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
        
        {/* Available words - with fixed positions using absolute positioning */}
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-700 mb-2">
            Available words: <span className="text-blue-600">{Object.values(wordStatus).filter(status => !status).length} remaining</span>
          </p>
          <div 
            className="relative available-words" 
            style={{ 
              height: `${Math.ceil(wordIds.length / 4) * 46}px`,
              minHeight: '46px'
            }}
            data-testid="word-bank"
            data-debug-word-count={wordIds.length}
          >
            {wordIds.map((wordId, index) => {
              const word = wordId.split('-')[0];
              const isUsed = wordStatus[wordId];
              
              // Calculate position based on index
              const col = index % 4;
              const row = Math.floor(index / 4);
              
              return (
                <div 
                  key={wordId} 
                  className="absolute word-item"
                  style={{
                    top: `${row * 46}px`,
                    left: `${col * 25}%`,
                    width: '24%',
                    height: '38px',
                    opacity: isUsed ? 0 : 1,
                    visibility: isUsed ? 'hidden' : 'visible',
                    pointerEvents: isUsed ? 'none' : 'auto'
                  }}
                  data-testid={`word-item-${index}`}
                  data-debug-word={word}
                  data-debug-used={isUsed ? "true" : "false"}
                >
                  <button
                    onClick={() => handleSelectWord(wordId)}
                    disabled={submitted || isUsed}
                    className={`
                      w-full h-full py-1 px-3 rounded-lg border 
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
                </div>
              );
            })}
          </div>
        </div>
      </div>
      
      {!submitted ? (
        <div className="flex space-x-3">
          <button
            onClick={handleSubmit}
            disabled={arrangement.includes(null)}
            className={`
              bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors
              ${arrangement.includes(null) ? 'opacity-50 cursor-not-allowed' : ''}
            `}
            data-testid="submit-button"
          >
            Submit
          </button>
          <button
            onClick={handleReset}
            className="border border-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-100 transition-colors"
            data-testid="reset-button"
          >
            Reset
          </button>
        </div>
      ) : showFeedback ? (
        <div 
          className={`mt-4 p-3 rounded ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}
          data-testid="feedback-panel"
          data-debug-is-correct={isCorrect ? "true" : "false"}
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

export default WordScrambleDebug; 