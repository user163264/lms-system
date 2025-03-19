'use client';

import React from 'react';
import WordScramble from '../components/exercises/WordScramble';

// Sample exercise data - simple sentence with well-known words
const sampleExercise = {
  id: 123,
  exercise_type: 'word_scramble',
  question: 'Arrange the words to form a correct sentence:',
  sentence: 'The quick brown fox jumps over the lazy dog',
  correct_answer: ['The quick brown fox jumps over the lazy dog'],
  max_score: 1
};

export default function ScramblePage() {
  // Simple submission handler
  const handleSubmit = (answer: string, exerciseId: number) => {
    console.log(`Exercise ${exerciseId} submitted with answer: ${answer}`);
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Word Scramble Test</h1>
      <p className="mb-4 text-gray-600">
        This page tests the Word Scramble component with the optimized implementation.
      </p>
      
      <div className="w-full max-w-3xl mx-auto">
        <WordScramble 
          exercise={sampleExercise} 
          onSubmit={handleSubmit} 
          showFeedback={true} 
        />
      </div>

      <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded max-w-3xl mx-auto">
        <h2 className="font-medium mb-2">Test Instructions:</h2>
        <ol className="list-decimal pl-5 space-y-2">
          <li>Try selecting different words and placing them in the slots</li>
          <li>Check if the words remain in fixed positions (no jittering)</li>
          <li>Try removing words from slots and placing them again</li>
          <li>Complete the sentence and submit to verify it works</li>
        </ol>
      </div>
    </div>
  );
} 