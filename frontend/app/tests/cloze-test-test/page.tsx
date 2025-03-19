'use client';

import React from 'react';
import { ExerciseType, ExerciseAnswer, Feedback, Exercise } from '../context/ExerciseContext';
import { ExerciseFactory } from '../components/exercises';
import { ExerciseProvider } from '../context/ExerciseProvider';

/**
 * Cloze Test Exercise Demo Page
 * 
 * A demo page that showcases the Cloze Test exercise component where
 * users fill in blanks using words from a provided word bank.
 */
export default function ClozeTestPage() {
  // Sample exercise data for testing
  const sampleExercise: Exercise = {
    id: 7001,
    exercise_type: ExerciseType.CLOZE_TEST,
    question: "Fill in the blanks with words from the word bank to complete the passage about renewable energy.",
    instructions: "Select words from the word bank to fill in each blank in the text.",
    sentence: "Renewable energy comes from natural sources that are constantly ____ such as sunlight, wind, and water. Unlike fossil fuels, renewable energy sources don't ____ harmful pollutants and greenhouse gases. Solar panels convert ____ into electricity, while wind turbines use the power of ____ to generate energy. Hydroelectric power relies on moving ____ to create electricity. As technology advances, renewable energy becomes more ____ and widely adopted.",
    word_bank: ["replenished", "emit", "sunlight", "wind", "water", "affordable"],
    correct_answer: ["replenished", "emit", "sunlight", "wind", "water", "affordable"],
    max_score: 6
  };

  // Handle submitting answers
  const handleSubmit = async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log('Submitted answer:', answer);
    
    // Cast answer to string array
    const userAnswers = answer as string[];
    const correctAnswers = sampleExercise.correct_answer || [];
    
    // Calculate how many answers are correct
    let correctCount = 0;
    userAnswers.forEach((word, index) => {
      if (correctAnswers[index] === word) {
        correctCount++;
      }
    });
    
    // Calculate score (1 point per correct answer)
    const score = correctCount;
    const totalBlanks = correctAnswers.length;
    const isAllCorrect = correctCount === totalBlanks;
    
    return {
      isCorrect: isAllCorrect,
      score: score,
      message: `You got ${correctCount} out of ${totalBlanks} blanks correct.`
    };
  };

  return (
    <main className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">Cloze Test Exercise Demo</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md">
        <ExerciseProvider>
          <ExerciseFactory 
            exercise={sampleExercise}
            showFeedback={true}
            onSubmit={handleSubmit}
          />
        </ExerciseProvider>
      </div>
      
      <div className="mt-8 p-4 bg-gray-100 rounded-lg">
        <h2 className="font-semibold mb-2">About This Exercise</h2>
        <p>
          A Cloze Test (also known as a fill-in-the-blank exercise with a word bank) 
          presents text with gaps that students must complete using provided words.
        </p>
        <p className="mt-2">
          This exercise type helps assess vocabulary knowledge, reading comprehension,
          and understanding of context. Students must select the right word for each blank
          based on the surrounding text.
        </p>
        <div className="mt-4">
          <h3 className="font-medium">Features:</h3>
          <ul className="list-disc pl-5 mt-1">
            <li>Interactive word bank with draggable words</li>
            <li>Visual feedback on correct and incorrect answers</li>
            <li>Support for any number of blanks and word bank items</li>
          </ul>
        </div>
      </div>
    </main>
  );
} 