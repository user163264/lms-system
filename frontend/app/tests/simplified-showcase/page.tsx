'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import just one component for testing
const WordScramble = dynamic(
  () => import('../components/exercises/WordScramble'),
  { 
    ssr: false,
    loading: () => <div className="p-4 bg-gray-100 rounded">Loading WordScramble component...</div>
  }
);

export default function SimplifiedShowcasePage() {
  const [isClient, setIsClient] = useState(false);
  const [componentLoaded, setComponentLoaded] = useState(false);
  
  useEffect(() => {
    console.log('SimplifiedShowcasePage mounted on client');
    setIsClient(true);
    
    // Pre-load the component
    import('../components/exercises/WordScramble')
      .then(() => {
        console.log('WordScramble pre-loaded successfully');
        setComponentLoaded(true);
      })
      .catch(err => {
        console.error('Error pre-loading WordScramble', err);
      });
  }, []);

  const handleSubmit = (answer: string, exerciseId: number) => {
    console.log(`Submit for exercise ${exerciseId}:`, answer);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Simplified Showcase</h1>
      
      <div className="p-4 bg-blue-100 rounded mb-4">
        <p><strong>Client Rendering:</strong> {isClient ? "Active" : "Inactive"}</p>
        <p><strong>Component Pre-loaded:</strong> {componentLoaded ? "Yes" : "No"}</p>
      </div>
      
      <div className="border bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-4">Word Scramble (Dynamic Import)</h2>
        {isClient && (
          <WordScramble 
            exercise={{
              id: 1001,
              exercise_type: 'word_scramble',
              question: 'Arrange the words to form a complete sentence:',
              sentence: 'The quick brown fox jumps over the lazy dog',
              correct_answer: ['The quick brown fox jumps over the lazy dog']
            }}
            onSubmit={handleSubmit}
            showFeedback={true}
          />
        )}
      </div>
    </div>
  );
} 