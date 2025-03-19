'use client';

import React, { useState, useEffect } from 'react';
import WordScramble from '../../components/exercises/WordScramble';

const sampleExercise = {
  id: 123,
  exercise_type: 'word_scramble',
  question: 'Arrange the words to form a correct sentence:',
  sentence: 'The quick brown fox jumps over the lazy dog',
  correct_answer: ['The quick brown fox jumps over the lazy dog'],
  max_score: 1
};

const duplicateWordsExercise = {
  id: 124,
  exercise_type: 'word_scramble',
  question: 'Arrange the words to form a correct sentence with duplicate words:',
  sentence: 'The dog saw the cat and the cat saw the mouse',
  correct_answer: ['The dog saw the cat and the cat saw the mouse'],
  max_score: 1
};

export default function TestPage() {
  const [submittedAnswer, setSubmittedAnswer] = useState('');
  const [testResults, setTestResults] = useState<string[]>([]);
  
  // Load test script
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const originalConsoleLog = console.log;
      const originalConsoleError = console.error;
      
      console.log = (...args) => {
        originalConsoleLog(...args);
        setTestResults(prev => [...prev, args.join(' ')]);
      };
      
      console.error = (...args) => {
        originalConsoleError(...args);
        setTestResults(prev => [...prev, `ERROR: ${args.join(' ')}`]);
      };
      
      const script = document.createElement('script');
      script.src = '/test/word-scramble/test.js';
      script.async = true;
      document.body.appendChild(script);
      
      return () => {
        console.log = originalConsoleLog;
        console.error = originalConsoleError;
        document.body.removeChild(script);
      };
    }
  }, []);

  // Handler for submission
  const handleSubmit = (answer: string, exerciseId: number) => {
    setSubmittedAnswer(answer);
    console.log(`Exercise ${exerciseId} submitted with answer: ${answer}`);
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-2xl font-bold mb-8">Word Scramble Component Test</h1>
      
      <div className="mb-8 test-case-1">
        <h2 className="text-xl font-semibold mb-4">Test Case 1: Standard Sentence</h2>
        <WordScramble 
          exercise={sampleExercise} 
          onSubmit={handleSubmit} 
          showFeedback={true} 
        />
        {submittedAnswer && (
          <div className="mt-4 p-4 bg-gray-100 rounded">
            <p><strong>Last submitted answer:</strong> {submittedAnswer}</p>
          </div>
        )}
      </div>
      
      <div className="mt-12 test-case-2">
        <h2 className="text-xl font-semibold mb-4">Test Case 2: Sentence with Duplicate Words</h2>
        <WordScramble 
          exercise={duplicateWordsExercise} 
          onSubmit={handleSubmit} 
          showFeedback={true} 
        />
      </div>
      
      <div className="mt-12 p-4 bg-yellow-50 border border-yellow-200 rounded">
        <h3 className="font-medium">Debug Notes:</h3>
        <ul className="list-disc pl-5 mt-2">
          <li>Observe if words jitter/move when selecting and placing them</li>
          <li>Test with duplicate words to ensure word tracking works correctly</li>
          <li>Test removing words from slots and placing them again</li>
        </ul>
      </div>
      
      {/* Test Results Section */}
      <div className="mt-8 p-4 bg-gray-100 rounded">
        <h3 className="font-medium mb-2">Test Results:</h3>
        <div className="bg-black text-green-400 p-4 rounded font-mono text-sm max-h-64 overflow-auto">
          {testResults.length > 0 ? (
            testResults.map((result, index) => (
              <div key={index} className={result.startsWith('ERROR:') ? 'text-red-400' : ''}>
                &gt; {result}
              </div>
            ))
          ) : (
            <div>Waiting for test results...</div>
          )}
        </div>
      </div>
    </div>
  );
} 