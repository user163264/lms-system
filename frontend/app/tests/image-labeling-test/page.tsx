'use client';

import React from 'react';
import { ExerciseType, ExerciseAnswer, Feedback, Exercise } from '../context/ExerciseContext';
import { ExerciseFactory } from '../components/exercises';
import { ExerciseProvider } from '../context/ExerciseProvider';

/**
 * Image Labeling Test Page
 * 
 * A demo page that showcases the Image Labeling exercise component.
 */
export default function ImageLabelingTestPage() {
  // Sample exercise data for testing
  const sampleExercise: Exercise = {
    id: 5001,
    exercise_type: ExerciseType.IMAGE_LABELING,
    question: "Label the parts of the human body in this diagram",
    instructions: "Select the correct label for each marked point on the image",
    image_url: "https://upload.wikimedia.org/wikipedia/commons/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg",
    labels: ["Head", "Chest", "Arms", "Legs", "Square", "Circle"],
    label_points: [
      { id: "A", x: 50, y: 15, label: "" },
      { id: "B", x: 50, y: 37, label: "" },
      { id: "C", x: 75, y: 40, label: "" },
      { id: "D", x: 50, y: 70, label: "" },
      { id: "E", x: 20, y: 50, label: "" },
      { id: "F", x: 80, y: 50, label: "" }
    ],
    // We need to store the correct label mapping in a custom property for ImageLabeling
    // but keep correct_answer as a string[] to satisfy the Exercise interface
    correct_answer: [], // This will be empty but meets the interface requirement
    correct_label_mapping: {
      "A": "Head",
      "B": "Chest",
      "C": "Arms",
      "D": "Legs",
      "E": "Square",
      "F": "Circle"
    },
    max_score: 6
  };

  // Handle submitting answers
  const handleSubmit = async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log('Submitted answer:', answer);
    
    // Calculate score
    let score = 0;
    let correct = false;
    
    // Cast answer to the expected format
    const labelAnswers = answer as Record<string, string>;
    const correctAnswers = sampleExercise.correct_label_mapping as Record<string, string>;
    
    // Check each label against the correct answer
    Object.entries(labelAnswers).forEach(([pointId, label]) => {
      if (correctAnswers[pointId] === label) {
        score++;
      }
    });
    
    correct = score === Object.keys(correctAnswers).length;
    
    return {
      isCorrect: correct,
      score: score,
      message: correct ? "All labels are correct!" : `You labeled ${score} out of ${Object.keys(correctAnswers).length} points correctly.`
    };
  };

  return (
    <main className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">Image Labeling Exercise Test</h1>
      
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
        <h2 className="font-semibold mb-2">About This Example</h2>
        <p>
          This page demonstrates the Image Labeling exercise component, which allows 
          students to identify and label parts of an image. In this example, students 
          label parts of Leonardo da Vinci's Vitruvian Man.
        </p>
      </div>
    </main>
  );
} 