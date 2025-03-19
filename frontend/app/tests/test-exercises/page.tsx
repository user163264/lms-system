'use client';

import React, { useState } from 'react';
import ExerciseRenderer, { Exercise, ExerciseAnswer } from '../components/exercises/ExerciseRenderer';

export default function TestExercisesPage() {
  const [submissions, setSubmissions] = useState<Record<number, ExerciseAnswer>>({});

  // Sample exercises for testing
  const sampleExercises: Exercise[] = [
    // Fill in the blanks example
    {
      id: 1,
      exercise_type: 'fill_blank',
      question: 'De glimlach van de _______ is wereldberoemd en blijft een mysterie.',
      correct_answer: ['Mona Lisa'],
      max_score: 1
    },
    
    // True/False example
    {
      id: 2,
      exercise_type: 'true_false',
      question: 'Mona Lisa werd geschilderd door Vincent van Gogh.',
      options: ['waar', 'niet waar'],
      correct_answer: ['niet waar'],
      max_score: 1
    },
    
    // Multiple choice example
    {
      id: 3,
      exercise_type: 'multiple_choice',
      question: 'Welk museum herbergt de Mona Lisa?',
      options: ['Prado', 'Louvre', 'Rijksmuseum'],
      correct_answer: ['Louvre'],
      max_score: 1
    },
    
    // Cloze test with word bank example
    {
      id: 4,
      exercise_type: 'cloze_test',
      question: 'Mona Lisa hangs in the _______ in _______.',
      word_bank: ['Louvre', 'Paris', 'Prado', 'Madrid', 'Rijksmuseum', 'Amsterdam'],
      correct_answer: ['Louvre', 'Paris'],
      max_score: 2
    },

    // Short answer example
    {
      id: 5,
      exercise_type: 'short_answer',
      question: 'Who painted the Mona Lisa?',
      correct_answer: ['Leonardo da Vinci', 'Da Vinci'],
      max_score: 1
    },

    // Matching words example
    {
      id: 6,
      exercise_type: 'matching_words',
      question: 'Match each painting with its artist:',
      correct_answer: ['0', '1', '2', '3'], // String representation of indices for compatibility
      items_a: ['Mona Lisa', 'Starry Night', 'The Scream', 'Girl with a Pearl Earring'],
      items_b: ['Leonardo da Vinci', 'Vincent van Gogh', 'Edvard Munch', 'Johannes Vermeer'],
      correct_matches: [0, 1, 2, 3], // indices matching items_a to items_b
      max_score: 4
    },

    // Sentence reordering example
    {
      id: 7,
      exercise_type: 'sentence_reordering',
      question: 'Arrange the following sentences in the correct chronological order:',
      correct_answer: ['0', '1', '3', '2'], // String representation of indices for compatibility
      sentences: [
        'Leonardo da Vinci began painting the Mona Lisa in 1503.',
        'It is thought to be a portrait of Lisa Gherardini.',
        'The painting is now displayed at the Louvre Museum in Paris.',
        'The Mona Lisa is one of the most valuable paintings in the world.'
      ],
      correct_order: [0, 1, 3, 2], // The correct order of sentences
      max_score: 4
    },

    // Long answer example
    {
      id: 8,
      exercise_type: 'long_answer',
      question: 'Explain the significance of the Mona Lisa in art history and why it has become such an iconic painting.',
      correct_answer: [
        'The subject\'s enigmatic expression',
        'Leonardo\'s innovative techniques',
        'Its influence on portrait painting',
        'Its cultural impact beyond the art world'
      ],
      required_keywords: ['sfumato', 'composition', 'Renaissance'],
      min_words: 30,
      max_words: 300,
      max_score: 5
    },

    // Word scramble example
    {
      id: 9,
      exercise_type: 'word_scramble',
      question: 'Rearrange the words to form a correct sentence about the Mona Lisa:',
      sentence: 'The Mona Lisa was painted by Leonardo da Vinci in the early sixteenth century.',
      correct_answer: ['The Mona Lisa was painted by Leonardo da Vinci in the early sixteenth century.'],
      max_score: 1
    },

    // Image labeling example
    {
      id: 10,
      exercise_type: 'image_labeling',
      question: 'Label the following anatomical features in Leonardo da Vinci\'s Vitruvian Man:',
      image_url: 'https://upload.wikimedia.org/wikipedia/commons/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg',
      labels: ['Head', 'Chest', 'Arms', 'Legs', 'Circle', 'Square'],
      label_points: [
        { id: 'A', x: 50, y: 20, label: '' },
        { id: 'B', x: 50, y: 40, label: '' },
        { id: 'C', x: 30, y: 45, label: '' },
        { id: 'D', x: 50, y: 70, label: '' },
        { id: 'E', x: 70, y: 45, label: '' },
        { id: 'F', x: 20, y: 50, label: '' }
      ],
      // Using a dummy array for type compatibility, the component will use it as a Record
      correct_answer: ['dummy'],
      max_score: 6
    }
  ];

  const handleSubmitAnswer = (answer: ExerciseAnswer, exerciseId: number) => {
    console.log(`Submitted answer for exercise ${exerciseId}:`, answer);
    
    // Store the submission locally
    setSubmissions(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
  };

  // Display submission status
  const submissionCount = Object.keys(submissions).length;

  return (
    <div className="min-h-screen p-10 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Exercise Component Tests</h1>
      <p className="mb-4 text-gray-600">
        This page demonstrates the different exercise types implemented in the LMS.
      </p>
      
      {submissionCount > 0 && (
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Your Submissions</h2>
          <p>You have submitted {submissionCount} out of {sampleExercises.length} exercises.</p>
          <pre className="mt-2 p-3 bg-gray-100 rounded text-sm overflow-auto max-h-40">
            {JSON.stringify(submissions, null, 2)}
          </pre>
        </div>
      )}
      
      <div className="space-y-8 mb-10">
        <h2 className="text-2xl font-semibold">Fill in the Blanks</h2>
        <ExerciseRenderer
          exercise={sampleExercises[0]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />
        
        <h2 className="text-2xl font-semibold mt-8">True/False</h2>
        <ExerciseRenderer
          exercise={sampleExercises[1]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />
        
        <h2 className="text-2xl font-semibold mt-8">Multiple Choice</h2>
        <ExerciseRenderer
          exercise={sampleExercises[2]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />
        
        <h2 className="text-2xl font-semibold mt-8">Cloze Test with Word Bank</h2>
        <ExerciseRenderer
          exercise={sampleExercises[3]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />

        <h2 className="text-2xl font-semibold mt-8">Short Answer</h2>
        <ExerciseRenderer
          exercise={sampleExercises[4]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />

        <h2 className="text-2xl font-semibold mt-8">Matching Words</h2>
        <ExerciseRenderer
          exercise={sampleExercises[5]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />

        <h2 className="text-2xl font-semibold mt-8">Sentence Reordering</h2>
        <ExerciseRenderer
          exercise={sampleExercises[6]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />

        <h2 className="text-2xl font-semibold mt-8">Long Answer / Essay</h2>
        <ExerciseRenderer
          exercise={sampleExercises[7]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />

        <h2 className="text-2xl font-semibold mt-8">Word Scramble</h2>
        <ExerciseRenderer
          exercise={sampleExercises[8]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />

        <h2 className="text-2xl font-semibold mt-8">Image Labeling</h2>
        <ExerciseRenderer
          exercise={sampleExercises[9]}
          onSubmit={handleSubmitAnswer}
          showFeedback={true}
        />
      </div>
    </div>
  );
} 