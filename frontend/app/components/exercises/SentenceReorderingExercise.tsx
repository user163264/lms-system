'use client';

import React, { useState, useEffect } from 'react';
import InteractiveExercise, { InteractiveExerciseProps } from './base/InteractiveExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface SentenceReorderingExerciseProps extends Omit<InteractiveExerciseProps, 'exercise'> {
  exercise: Exercise;
}

// Define the shape of our game state
interface GameState {
  originalSentences: string[];
  shuffledSentences: string[];
  sentenceIds: string[];
  sentenceStatus: Record<string, boolean>;
  arrangement: (string | null)[];
  slotSentenceIds: (string | null)[];
  selectedSentence: string | null;
  isShuffled: boolean;
}

/**
 * Sentence Reordering Exercise Component
 * 
 * Component for exercises where users reorder scrambled sentences to form a coherent paragraph.
 */
const SentenceReorderingExercise: React.FC<SentenceReorderingExerciseProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  
  // Initialize game state
  const [gameState, setGameState] = useState<GameState>(() => {
    // Get original sentences from the exercise
    const originalSentences = exercise.sentences || [];
    
    // Create unique IDs for each sentence
    const sentenceIds = originalSentences.map((sentence, index) => `${index}-${sentence.substring(0, 10)}`);
    
    // Create a map to track which sentences are used
    const sentenceStatus: Record<string, boolean> = {};
    sentenceIds.forEach(id => {
      sentenceStatus[id] = false; // false = not used
    });
    
    return {
      originalSentences,
      shuffledSentences: [...originalSentences], // Will be shuffled after initial render
      sentenceIds,
      sentenceStatus,
      arrangement: Array(originalSentences.length).fill(null),
      slotSentenceIds: Array(originalSentences.length).fill(null),
      selectedSentence: null,
      isShuffled: false
    };
  });
  
  // Shuffle sentences client-side after initial render to avoid hydration mismatches
  useEffect(() => {
    if (!gameState.isShuffled && gameState.originalSentences.length > 0) {
      const shuffledSentences = [...gameState.originalSentences];
      
      // Fisher-Yates shuffle algorithm
      for (let i = shuffledSentences.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledSentences[i], shuffledSentences[j]] = [shuffledSentences[j], shuffledSentences[i]];
      }
      
      setGameState(prev => ({
        ...prev,
        shuffledSentences,
        isShuffled: true
      }));
    }
  }, [gameState.isShuffled, gameState.originalSentences]);
  
  // Update context when arrangement changes
  useEffect(() => {
    // Get the indices of the arranged sentences
    const orderedIndices = gameState.arrangement
      .map((sentenceId, index) => {
        if (sentenceId === null) return -1;
        // Get the original index based on the sentenceId
        const sentenceIndex = gameState.sentenceIds.indexOf(sentenceId);
        return sentenceIndex;
      })
      .filter(index => index !== -1);
    
    // Only update if we have some sentences placed
    if (orderedIndices.length > 0) {
      updateAnswer(orderedIndices);
    }
  }, [gameState.arrangement, gameState.sentenceIds, updateAnswer]);
  
  // Handle sentence selection
  const handleSelectSentence = (sentenceId: string) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    // Toggle selection
    setGameState(prev => ({
      ...prev,
      selectedSentence: prev.selectedSentence === sentenceId ? null : sentenceId
    }));
  };
  
  // Handle placing a sentence in a slot
  const handlePlaceSentence = (slotIndex: number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED || gameState.selectedSentence === null) return;
    
    setGameState(prev => {
      // Create new state objects (don't mutate existing state)
      const newArrangement = [...prev.arrangement];
      const newSlotSentenceIds = [...prev.slotSentenceIds];
      const newSentenceStatus = { ...prev.sentenceStatus };
      
      // If there's already a sentence in this slot, make it available again
      if (newSlotSentenceIds[slotIndex] !== null) {
        const sentenceId = newSlotSentenceIds[slotIndex];
        if (sentenceId !== null) {
          newSentenceStatus[sentenceId] = false;
        }
      }
      
      // Place the selected sentence in the slot
      const selectedSentence = gameState.selectedSentence;
      if (selectedSentence !== null) {
        newArrangement[slotIndex] = selectedSentence;
        newSlotSentenceIds[slotIndex] = selectedSentence;
        newSentenceStatus[selectedSentence] = true;
      }
      
      return {
        ...prev,
        arrangement: newArrangement,
        slotSentenceIds: newSlotSentenceIds,
        sentenceStatus: newSentenceStatus,
        selectedSentence: null // Deselect after placing
      };
    });
  };
  
  // Handle removing a sentence from a slot
  const handleRemoveSentence = (slotIndex: number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    setGameState(prev => {
      // If the slot is empty, do nothing
      if (prev.slotSentenceIds[slotIndex] === null) return prev;
      
      // Create new state objects
      const newArrangement = [...prev.arrangement];
      const newSlotSentenceIds = [...prev.slotSentenceIds];
      const newSentenceStatus = { ...prev.sentenceStatus };
      
      // Mark the sentence as available again
      const sentenceId = prev.slotSentenceIds[slotIndex];
      if (sentenceId !== null) {
        newSentenceStatus[sentenceId] = false;
      }
      
      // Clear the slot
      newArrangement[slotIndex] = null;
      newSlotSentenceIds[slotIndex] = null;
      
      return {
        ...prev,
        arrangement: newArrangement,
        slotSentenceIds: newSlotSentenceIds,
        sentenceStatus: newSentenceStatus
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
      arrangement: Array(prev.originalSentences.length).fill(null),
      slotSentenceIds: Array(prev.originalSentences.length).fill(null),
      sentenceStatus: Object.fromEntries(prev.sentenceIds.map(id => [id, false])),
      selectedSentence: null,
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
    
  // Determine correctness if feedback is available
  const getCorrectOrder = () => {
    if (!state.feedback || !exercise.correct_order) return [];
    
    // Map each slot to whether it contains the correct sentence
    return gameState.arrangement.map((sentenceId, index) => {
      if (sentenceId === null) return false;
      const sentenceIndex = gameState.sentenceIds.indexOf(sentenceId);
      const correctIndex = exercise.correct_order?.[index];
      return sentenceIndex === correctIndex;
    });
  };

  const correctOrder = getCorrectOrder();

  return (
    <InteractiveExercise
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4" suppressHydrationWarning>
        {/* Sentence slots for arranging the paragraph */}
        <div className="space-y-2">
          <h4 className="font-medium">Arrange the sentences in order:</h4>
          {gameState.arrangement.map((sentenceId, slotIndex) => (
            <div 
              key={`slot-${slotIndex}`}
              onClick={() => sentenceId ? handleRemoveSentence(slotIndex) : handlePlaceSentence(slotIndex)}
              className={`
                p-3 rounded border-2 mb-2 transition
                ${sentenceId 
                  ? (state.submissionStatus === SubmissionStatus.SUBMITTED && correctOrder.length > 0
                    ? (correctOrder[slotIndex] ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500')
                    : 'bg-white border-blue-500') 
                  : 'border-dashed border-gray-400 bg-gray-50 hover:bg-gray-100'
                }
                ${gameState.selectedSentence && !sentenceId ? 'bg-blue-50 border-blue-500' : ''}
                ${isDisabled ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'}
              `}
            >
              {sentenceId ? (
                <p className="text-sm">
                  {gameState.originalSentences[gameState.sentenceIds.indexOf(sentenceId)]}
                </p>
              ) : (
                <p className="text-gray-500 text-center py-2">
                  {gameState.selectedSentence ? 'Click to place selected sentence here' : 'Empty slot'}
                </p>
              )}
              {sentenceId && state.submissionStatus === SubmissionStatus.SUBMITTED && correctOrder.length > 0 && (
                <div className={`mt-1 text-xs font-medium ${correctOrder[slotIndex] ? 'text-green-600' : 'text-red-600'}`}>
                  {correctOrder[slotIndex] 
                    ? '✓ Correct position' 
                    : `✗ Should be: "${gameState.originalSentences[exercise.correct_order?.[slotIndex] || 0]}"`
                  }
                </div>
              )}
            </div>
          ))}
        </div>
        
        {/* Sentence bank */}
        <div className="mt-6">
          <h4 className="font-medium mb-2">Available Sentences:</h4>
          <div className="space-y-2">
            {gameState.shuffledSentences.map((sentence, sentenceIndex) => {
              const sentenceId = gameState.sentenceIds[gameState.originalSentences.indexOf(sentence)];
              const isUsed = gameState.sentenceStatus[sentenceId];
              
              return (
                <div
                  key={`sentence-${sentenceId}`}
                  onClick={() => !isUsed && !isDisabled && handleSelectSentence(sentenceId)}
                  className={`
                    p-3 rounded border transition
                    ${isUsed ? 'bg-gray-100 text-gray-500 border-gray-300' : 'bg-white border-gray-300'}
                    ${gameState.selectedSentence === sentenceId ? 'bg-blue-50 border-blue-500' : ''}
                    ${isDisabled || isUsed ? 'opacity-70 cursor-not-allowed' : 'hover:bg-blue-50 hover:border-blue-300 cursor-pointer'}
                  `}
                >
                  <p className="text-sm">{sentence}</p>
                </div>
              );
            })}
          </div>
        </div>
        
        {/* Instructions */}
        <div className="text-sm text-gray-600 mt-4">
          <p>
            <strong>Instructions:</strong> Click on a sentence from the list below, then click on an empty slot to place it. 
            Click on a placed sentence to remove it.
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

export default SentenceReorderingExercise; 