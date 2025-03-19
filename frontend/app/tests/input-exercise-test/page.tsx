'use client';

import React, { useState, useCallback } from 'react';
import { ExerciseFactory } from '../components/exercises';
import { ExerciseProvider, Exercise, ExerciseType, Feedback, ExerciseAnswer } from '../context/ExerciseContext';

const InputExerciseTestPage = () => {
  const [feedbackState, setFeedbackState] = useState<{ [key: number]: Feedback }>({});
  
  // Mock function to simulate API submission
  const handleSubmit = useCallback(async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log(`Exercise ID ${exerciseId} submitted with answer:`, answer);
    
    // Simple validation - for demo purposes
    let isCorrect = false;
    let message = "Incorrect answer. Try again.";
    let score = 0;
    
    // Check the answer against the exercise's correct answer
    const exercise = sampleExercises.find(ex => ex.id === exerciseId);
    if (exercise && exercise.correct_answer) {
      if (typeof answer === 'string') {
        // Case-insensitive check for string answers
        isCorrect = exercise.correct_answer.some(
          correct => correct.toLowerCase() === answer.toLowerCase()
        );
      }
      
      if (isCorrect) {
        message = "Great job! That's correct.";
        score = exercise.max_score || 1;
      }
    }
    
    // Create feedback object
    const feedback: Feedback = {
      isCorrect,
      message,
      score
    };
    
    // Update state
    setFeedbackState(prev => ({
      ...prev,
      [exerciseId]: feedback
    }));
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return feedback;
  }, []);

  return (
    <div className="container mx-auto p-6 max-w-4xl" suppressHydrationWarning>
      <h1 className="text-3xl font-bold mb-8">Input Exercise Test</h1>
      
      {/* Render each sample exercise */}
      <div className="space-y-8">
        {sampleExercises.map(exercise => (
          <div key={exercise.id} className="bg-white rounded-lg shadow-md p-1" suppressHydrationWarning>
            <ExerciseProvider onSubmit={handleSubmit}>
              <ExerciseFactory 
                exercise={exercise}
                showFeedback={true}
              />
            </ExerciseProvider>
          </div>
        ))}
      </div>
    </div>
  );
};

// Sample exercises for testing
const sampleExercises: Exercise[] = [
  {
    id: 1,
    exercise_type: ExerciseType.SHORT_ANSWER,
    question: "What is the capital of France?",
    instructions: "Provide a short answer to the question.",
    correct_answer: ["Paris", "paris"],
    max_score: 1
  },
  {
    id: 2,
    exercise_type: ExerciseType.FILL_BLANK,
    question: "The largest planet in our solar system is _______.",
    instructions: "Fill in the blank with the correct word.",
    correct_answer: ["Jupiter", "jupiter"],
    max_score: 1
  },
  {
    id: 3,
    exercise_type: ExerciseType.SHORT_ANSWER,
    question: "What is the chemical symbol for gold?",
    instructions: "Enter the chemical symbol (abbreviation).",
    correct_answer: ["Au", "au"],
    max_words: 1,
    max_score: 1
  },
  {
    id: 4,
    exercise_type: ExerciseType.FILL_BLANK,
    question: "In programming, a _______ is a sequence of instructions.",
    instructions: "Complete the sentence with the appropriate term.",
    correct_answer: ["function", "program", "algorithm", "routine", "procedure", "method"],
    max_score: 1
  }
];

export default InputExerciseTestPage; 