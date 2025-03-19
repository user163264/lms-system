'use client';

import React, { useState } from 'react';
import { 
  ExerciseProvider, 
  Exercise, 
  ExerciseType, 
  ExerciseAnswer, 
  Feedback 
} from '../../context/ExerciseContext';
import { ExerciseFactory } from '../../components/exercises';

// Sample exercises for demonstration with explicit correct_answer fields
const sampleExercises: Exercise[] = [
  {
    id: 1,
    exercise_type: ExerciseType.MULTIPLE_CHOICE,
    question: 'What is the capital of France?',
    options: ['London', 'Berlin', 'Paris', 'Madrid'],
    correct_answer: ['Paris'],
  },
  {
    id: 2,
    exercise_type: ExerciseType.MULTIPLE_CHOICE,
    question: 'Which of the following are primary colors?',
    options: ['Red', 'Green', 'Blue', 'Orange'],
    correct_answer: ['Red', 'Blue'],
  },
  {
    id: 3,
    exercise_type: ExerciseType.TRUE_FALSE,
    question: 'The Earth is the third planet from the Sun.',
    correct_answer: ['true'],
  },
  {
    id: 4,
    exercise_type: ExerciseType.TRUE_FALSE,
    question: 'The Great Wall of China is visible from space with the naked eye.',
    correct_answer: ['false'],
  }
];

/**
 * Demo page for the Exercise components
 */
export default function ExerciseDemoPage() {
  const [selectedExercise, setSelectedExercise] = useState<Exercise>(sampleExercises[0]);
  
  // Simple mock submission handler with improved type safety
  const handleSubmit = async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    // Find the exercise
    const exercise = sampleExercises.find(ex => ex.id === exerciseId);
    
    if (!exercise || !exercise.correct_answer) {
      return {
        isCorrect: false,
        score: 0,
        message: 'Exercise not found or missing correct answer'
      };
    }
    
    // Compare the answer to the correct answer
    let isCorrect = false;
    
    if (Array.isArray(answer) && Array.isArray(exercise.correct_answer)) {
      // For multiple selection exercises
      const sortedAnswer = [...answer].sort();
      const sortedCorrect = [...exercise.correct_answer].sort();
      isCorrect = sortedAnswer.length === sortedCorrect.length && 
        sortedAnswer.every((val, idx) => val === sortedCorrect[idx]);
    } else if (!Array.isArray(answer) && Array.isArray(exercise.correct_answer) && exercise.correct_answer.length === 1) {
      // For single selection where correct_answer is an array with one item
      isCorrect = answer === exercise.correct_answer[0];
    }
    
    // Create feedback
    return {
      isCorrect,
      score: isCorrect ? 1 : 0,
      message: isCorrect 
        ? 'Correct! Well done.' 
        : 'Incorrect. Please try again.'
    };
  };
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Exercise Component Demo</h1>
      
      {/* Exercise selector */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-3">Select an Exercise</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sampleExercises.map((exercise) => (
            <button
              key={exercise.id}
              onClick={() => setSelectedExercise(exercise)}
              className={`p-4 border rounded-lg text-left hover:bg-blue-50 transition-colors
                ${selectedExercise.id === exercise.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}
              `}
            >
              <div className="text-sm text-gray-500 mb-1">
                {exercise.exercise_type.replace('_', ' ').toUpperCase()}
              </div>
              <div className="font-medium">{exercise.question}</div>
            </button>
          ))}
        </div>
      </div>
      
      {/* Selected exercise */}
      <div className="border rounded-lg p-6 bg-white shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Exercise</h2>
        <ExerciseProvider onSubmit={handleSubmit}>
          <ExerciseFactory 
            exercise={selectedExercise}
            showFeedback={true}
          />
        </ExerciseProvider>
      </div>
    </div>
  );
} 