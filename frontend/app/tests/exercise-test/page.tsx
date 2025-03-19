'use client';

import React, { useState, useEffect } from 'react';
import WordScramble from '../components/exercises/WordScramble';
import MultipleChoice from '../components/exercises/MultipleChoice';
import ImageLabeling from '../components/exercises/ImageLabeling';

export default function ExerciseTestPage() {
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    console.log('ExerciseTestPage mounted on client');
    setIsClient(true);
  }, []);

  const handleSubmit = (answer: any, exerciseId: number) => {
    console.log(`Submit for exercise ${exerciseId}:`, answer);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Exercise Test Page</h1>
      
      <div className="p-4 bg-blue-100 rounded mb-4">
        <p><strong>Client Rendering:</strong> {isClient ? "Active" : "Inactive"}</p>
      </div>
      
      {isClient ? (
        <div className="space-y-8">
          <div className="border bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-2xl font-bold mb-4">Word Scramble</h2>
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
          </div>
          
          <div className="border bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-2xl font-bold mb-4">Multiple Choice</h2>
            <MultipleChoice 
              exercise={{
                id: 1002,
                exercise_type: 'multiple_choice',
                question: 'What is the capital of France?',
                options: ['London', 'Berlin', 'Paris', 'Madrid'],
                correct_answer: ['2'] // Paris (index 2)
              }}
              onSubmit={handleSubmit}
              showFeedback={true}
            />
          </div>
          
          <div className="border bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-2xl font-bold mb-4">Image Labeling</h2>
            <ImageLabeling 
              exercise={{
                id: 1003,
                exercise_type: 'image_labeling',
                question: 'Label the parts of a cell:',
                image_url: 'https://placehold.co/600x400/png?text=Cell+Diagram',
                labels: ['Nucleus', 'Cell Membrane', 'Mitochondrion'],
                label_points: [
                  { id: '1', x: 30, y: 30, label: '' },
                  { id: '2', x: 50, y: 60, label: '' },
                  { id: '3', x: 70, y: 40, label: '' }
                ],
                correct_answer: {
                  '1': 'Nucleus',
                  '2': 'Cell Membrane',
                  '3': 'Mitochondrion'
                },
              }}
              onSubmit={handleSubmit}
              showFeedback={true}
            />
          </div>
        </div>
      ) : (
        <div className="my-8 text-center">
          <div className="inline-block p-4 bg-gray-100 rounded-lg">
            <p className="text-lg">Loading exercise components...</p>
            <div className="mt-2 h-2 w-40 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 animate-pulse"></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 