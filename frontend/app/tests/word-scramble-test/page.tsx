'use client';

import React, { useState, useEffect } from 'react';
import WordScramble from '../components/exercises/WordScramble';

// Sample exercises for thorough testing
const exercises = [
  {
    id: 1,
    title: "Basic Sentence",
    exercise: {
      id: 101,
      exercise_type: 'word_scramble',
      question: 'Arrange the words to form a correct sentence:',
      sentence: 'The quick brown fox jumps over the lazy dog',
      correct_answer: ['The quick brown fox jumps over the lazy dog'],
      max_score: 1
    }
  },
  {
    id: 2,
    title: "Sentence with Duplicate Words",
    exercise: {
      id: 102,
      exercise_type: 'word_scramble',
      question: 'Arrange the words to create a sentence with repeated words:',
      sentence: 'The dog saw the cat and the cat saw the mouse',
      correct_answer: ['The dog saw the cat and the cat saw the mouse'],
      max_score: 1
    }
  },
  {
    id: 3,
    title: "Short Sentence",
    exercise: {
      id: 103,
      exercise_type: 'word_scramble',
      question: 'Form a simple short sentence:',
      sentence: 'I love learning languages',
      correct_answer: ['I love learning languages'],
      max_score: 1
    }
  },
  {
    id: 4,
    title: "Longer Complex Sentence",
    exercise: {
      id: 104,
      exercise_type: 'word_scramble',
      question: 'Arrange these words into a more complex sentence:',
      sentence: 'While studying for the test, she realized that practice makes perfect',
      correct_answer: ['While studying for the test, she realized that practice makes perfect'],
      max_score: 1
    }
  },
  {
    id: 5, 
    title: "Question Format",
    exercise: {
      id: 105,
      exercise_type: 'word_scramble',
      question: 'Form a question from these words:',
      sentence: 'What time does the museum open tomorrow',
      correct_answer: ['What time does the museum open tomorrow'],
      max_score: 1
    }
  }
];

export default function WordScrambleTestPage() {
  const [selectedExercise, setSelectedExercise] = useState(exercises[0]);
  const [results, setResults] = useState<{id: number, answer: string}[]>([]);
  
  useEffect(() => {
    // Load test script
    const script = document.createElement('script');
    script.src = '/test/word-scramble-test.js';
    script.async = true;
    document.body.appendChild(script);
    
    return () => {
      // Clean up
      document.body.removeChild(script);
    };
  }, []);
  
  // Handler for submission
  const handleSubmit = (answer: string, exerciseId: number) => {
    console.log(`Exercise ${exerciseId} submitted with answer: ${answer}`);
    setResults(prev => [...prev, {id: exerciseId, answer}]);
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-2xl font-bold mb-4">Word Scramble Component Test</h1>
      <p className="text-gray-600 mb-6">This page allows you to test different variations of the Word Scramble exercise.</p>
      
      {/* Exercise selector */}
      <div className="mb-8 bg-gray-50 p-4 rounded-lg border border-gray-200">
        <h2 className="text-lg font-medium mb-3">Select an Exercise:</h2>
        <div className="flex flex-wrap gap-2">
          {exercises.map(ex => (
            <button
              key={ex.id}
              onClick={() => setSelectedExercise(ex)}
              className={`px-3 py-2 rounded text-sm ${
                selectedExercise.id === ex.id 
                  ? 'bg-blue-100 border-blue-500 border-2' 
                  : 'bg-white border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {ex.title}
            </button>
          ))}
        </div>
      </div>
      
      {/* Current exercise */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">{selectedExercise.title}</h2>
        <WordScramble 
          exercise={selectedExercise.exercise} 
          onSubmit={handleSubmit} 
          showFeedback={true} 
        />
      </div>
      
      {/* Results section */}
      {results.length > 0 && (
        <div className="mt-8 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-medium mb-2">Submission History:</h3>
          <ul className="space-y-2">
            {results.map((result, index) => {
              const exerciseInfo = exercises.find(ex => ex.exercise.id === result.id);
              return (
                <li key={index} className="bg-white p-3 rounded border border-gray-200">
                  <span className="font-medium">{exerciseInfo?.title || `Exercise ${result.id}`}:</span> {result.answer}
                </li>
              );
            })}
          </ul>
        </div>
      )}
      
      {/* Debug info */}
      <div className="mt-12 p-4 bg-yellow-50 border border-yellow-200 rounded">
        <h3 className="font-medium">Testing Notes:</h3>
        <ul className="list-disc pl-5 mt-2">
          <li>The instructions are now integrated as a collapsible section</li>
          <li>Try all different exercise types to verify the component handles them well</li>
          <li>Test word selection, placement, and removal functionality</li>
          <li>Check for any jittering in the word bank when interacting with words</li>
        </ul>
      </div>
    </div>
  );
} 