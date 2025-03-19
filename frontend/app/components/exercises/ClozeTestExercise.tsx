'use client';

import React, { useState, useEffect } from 'react';
import InteractiveExercise, { InteractiveExerciseProps } from './base/InteractiveExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface ClozeTestExerciseProps extends Omit<InteractiveExerciseProps, 'exercise'> {
  exercise: Exercise;
}

/**
 * Cloze Test Exercise Component
 * 
 * Component for exercises where users fill in blanks in text using 
 * words from a provided word bank.
 */
const ClozeTestExercise: React.FC<ClozeTestExerciseProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  
  // State for the sentence with blanks parsed into segments
  const [segments, setSegments] = useState<Array<{type: 'text' | 'blank', content: string}>>([]);
  
  // State for user answers (maps blank index to selected word)
  const [answers, setAnswers] = useState<Record<number, string>>({});
  
  // State for the word bank (available words to choose from)
  const [wordBank, setWordBank] = useState<Array<{word: string, used: boolean}>>([]);
  
  // State for tracking which blanks are correct (for feedback)
  const [correctAnswers, setCorrectAnswers] = useState<Record<number, boolean>>({});
  
  // Parse the sentence into segments on first render
  useEffect(() => {
    if (exercise.sentence) {
      // Split the sentence by blank markers (___) to get text and blank segments
      const pattern = /____+/g;
      const parts = exercise.sentence.split(pattern);
      const matches = [...exercise.sentence.matchAll(pattern)];
      
      const parsedSegments: Array<{type: 'text' | 'blank', content: string}> = [];
      
      // Interleave text segments and blanks
      parts.forEach((part, index) => {
        // Add text segment
        if (part) {
          parsedSegments.push({ type: 'text', content: part });
        }
        
        // Add blank segment if there's one after this text
        if (index < matches.length) {
          parsedSegments.push({ type: 'blank', content: `blank-${index}` });
        }
      });
      
      setSegments(parsedSegments);
      
      // Initialize word bank from exercise
      if (exercise.word_bank && Array.isArray(exercise.word_bank)) {
        setWordBank(exercise.word_bank.map(word => ({ word, used: false })));
      }
    }
  }, [exercise.sentence, exercise.word_bank]);
  
  // Update the context with answers whenever they change
  useEffect(() => {
    if (Object.keys(answers).length > 0) {
      // Convert answers object to format expected by the API
      // We need to create a format that matches one of the ExerciseAnswer types
      // Using string[] for compatibility with the Exercise interface
      const answerArray = Object.values(answers);
      updateAnswer(answerArray);
    }
  }, [answers, updateAnswer]);

  // Handle selecting a word for a blank
  const handleSelectWord = (blankIndex: number, word: string) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    // If this blank already had a word, make that word available again
    const previousWord = answers[blankIndex];
    if (previousWord) {
      setWordBank(prev => prev.map(item => 
        item.word === previousWord ? { ...item, used: false } : item
      ));
    }
    
    // Update answers
    setAnswers(prev => ({
      ...prev,
      [blankIndex]: word
    }));
    
    // Mark word as used in word bank
    setWordBank(prev => prev.map(item => 
      item.word === word ? { ...item, used: true } : item
    ));
  };
  
  // Handle removing a word from a blank
  const handleRemoveWord = (blankIndex: number) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
    // Get the word that was in the blank
    const word = answers[blankIndex];
    if (!word) return;
    
    // Make the word available again in the word bank
    setWordBank(prev => prev.map(item => 
      item.word === word ? { ...item, used: false } : item
    ));
    
    // Remove the answer
    setAnswers(prev => {
      const newAnswers = { ...prev };
      delete newAnswers[blankIndex];
      return newAnswers;
    });
  };
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (state.submissionStatus === SubmissionStatus.SUBMITTING) {
      return;
    }
    
    // Check which answers are correct
    const correctResults: Record<number, boolean> = {};
    
    if (exercise.correct_answer && Array.isArray(exercise.correct_answer)) {
      const blankCount = segments.filter(segment => segment.type === 'blank').length;
      
      for (let i = 0; i < blankCount; i++) {
        const userAnswer = answers[i];
        const correctAnswer = exercise.correct_answer[i];
        correctResults[i] = userAnswer === correctAnswer;
      }
    }
    
    setCorrectAnswers(correctResults);
    await submitAnswer();
  };
  
  // Handle reset
  const handleReset = () => {
    setAnswers({});
    setCorrectAnswers({});
    // Reset word bank to all words available
    if (exercise.word_bank && Array.isArray(exercise.word_bank)) {
      setWordBank(exercise.word_bank.map(word => ({ word, used: false })));
    }
    resetExercise();
  };
  
  // Check if all blanks are filled
  const allBlanksFilled = () => {
    const blankCount = segments.filter(segment => segment.type === 'blank').length;
    return Object.keys(answers).length === blankCount;
  };
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = 
    !allBlanksFilled() || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  return (
    <InteractiveExercise
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Cloze Text with Blanks */}
        <div className="text-lg leading-relaxed">
          {segments.map((segment, index) => {
            if (segment.type === 'text') {
              // Text segment
              return <span key={`text-${index}`}>{segment.content}</span>;
            } else {
              // Blank segment
              const blankIndex = parseInt(segment.content.split('-')[1]);
              const userAnswer = answers[blankIndex];
              const isCorrect = state.submissionStatus === SubmissionStatus.SUBMITTED && correctAnswers[blankIndex];
              const isIncorrect = state.submissionStatus === SubmissionStatus.SUBMITTED && !correctAnswers[blankIndex];
              
              return (
                <span
                  key={`blank-${index}`}
                  onClick={() => userAnswer && handleRemoveWord(blankIndex)}
                  className={`inline-block min-w-32 mx-1 px-2 py-1 border-b-2 text-center ${
                    userAnswer 
                      ? 'bg-blue-50 border-blue-500 cursor-pointer'
                      : 'border-gray-300'
                  } ${
                    isCorrect ? 'bg-green-100 border-green-500' :
                    isIncorrect ? 'bg-red-100 border-red-500' : ''
                  }`}
                >
                  {userAnswer || '\u00A0'}
                  {state.submissionStatus === SubmissionStatus.SUBMITTED && isIncorrect && (
                    <span className="block text-xs text-red-600 mt-1">
                      {exercise.correct_answer && Array.isArray(exercise.correct_answer) 
                        ? `(${exercise.correct_answer[blankIndex]})` 
                        : ''}
                    </span>
                  )}
                </span>
              );
            }
          })}
        </div>
        
        {/* Word Bank */}
        <div className="mt-6">
          <h3 className="text-sm font-medium mb-2">Word Bank:</h3>
          <div className="flex flex-wrap gap-2">
            {wordBank.map((item, index) => (
              <button
                key={`word-${index}`}
                type="button"
                disabled={item.used || state.submissionStatus === SubmissionStatus.SUBMITTED}
                onClick={() => {
                  if (!item.used) {
                    // Find the first empty blank
                    const blankSegments = segments.filter(s => s.type === 'blank');
                    for (let i = 0; i < blankSegments.length; i++) {
                      if (!answers[i]) {
                        handleSelectWord(i, item.word);
                        break;
                      }
                    }
                  }
                }}
                className={`px-3 py-1 rounded border ${
                  item.used 
                    ? 'bg-gray-100 text-gray-400 border-gray-300' 
                    : 'bg-white border-blue-500 text-blue-700 hover:bg-blue-50'
                }`}
              >
                {item.word}
              </button>
            ))}
          </div>
        </div>
        
        <div className="flex space-x-4 mt-4">
          {state.submissionStatus !== SubmissionStatus.SUBMITTED ? (
            <button
              type="submit"
              className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${
                isSubmitDisabled ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={isSubmitDisabled}
            >
              Submit
            </button>
          ) : (
            <button
              type="button"
              onClick={handleReset}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </form>
    </InteractiveExercise>
  );
};

export default ClozeTestExercise; 