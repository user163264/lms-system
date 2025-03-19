'use client';

import React from 'react';
import { ExerciseType, ExerciseAnswer, Feedback, Exercise } from '../context/ExerciseContext';
import { ExerciseFactory } from '../components/exercises';
import { ExerciseProvider } from '../context/ExerciseProvider';

/**
 * Long Answer Test Page
 * 
 * A demo page that showcases the Long Answer exercise component with word counting
 * and keyword requirement features.
 */
export default function LongAnswerTestPage() {
  // Sample exercise data for testing
  const sampleExercise: Exercise = {
    id: 6001,
    exercise_type: ExerciseType.LONG_ANSWER,
    question: "Explain the causes and effects of climate change on global ecosystems.",
    instructions: "Write a comprehensive explanation that addresses both causes and effects. Include specific examples.",
    min_words: 50,
    max_words: 200,
    required_keywords: ["greenhouse gases", "carbon emissions", "sea level", "temperature", "biodiversity"],
    correct_answer: [],
    max_score: 10
  };

  // Handle submitting answers - this would typically be handled by an API
  const handleSubmit = async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log('Submitted answer:', answer);
    
    // Cast answer to string
    const essayAnswer = answer as string;
    let score = 0;
    let feedback = '';
    
    // Word count check
    const wordCount = essayAnswer.trim().split(/\s+/).filter(w => w !== '').length;
    if (wordCount < (sampleExercise.min_words || 0)) {
      feedback += `Your answer is too short (${wordCount} words). `;
    } else if (sampleExercise.max_words && wordCount > sampleExercise.max_words) {
      feedback += `Your answer is too long (${wordCount} words). `;
    } else {
      score += 2; // Award points for meeting word count requirements
      feedback += `Word count requirement satisfied (${wordCount} words). `;
    }
    
    // Keyword check
    if (sampleExercise.required_keywords && Array.isArray(sampleExercise.required_keywords)) {
      const lowerAnswer = essayAnswer.toLowerCase();
      let keywordsFound = 0;
      
      sampleExercise.required_keywords.forEach(keyword => {
        if (lowerAnswer.includes(keyword.toLowerCase())) {
          keywordsFound++;
        }
      });
      
      // Award points based on keywords found (up to 5 points for all keywords)
      const keywordScore = Math.floor((keywordsFound / sampleExercise.required_keywords.length) * 5);
      score += keywordScore;
      
      feedback += `You included ${keywordsFound} out of ${sampleExercise.required_keywords.length} required keywords. `;
    }
    
    // Content quality score (simple algorithm based on length)
    // In a real system, this might use AI or human review
    const qualityScore = Math.min(3, Math.floor(wordCount / 60));
    score += qualityScore;
    
    // Calculate overall score
    const finalScore = Math.min(score, sampleExercise.max_score || 10);
    const isCorrect = finalScore >= (sampleExercise.max_score || 10) * 0.7; // 70% passing threshold
    
    return {
      isCorrect,
      score: finalScore,
      message: feedback + `Overall quality assessment: ${qualityScore} out of 3 points.`
    };
  };

  return (
    <main className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">Long Answer Exercise Test</h1>
      
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
          This page demonstrates the Long Answer exercise component, which allows 
          students to write extended responses or essays. It includes features like:
        </p>
        <ul className="list-disc pl-5 mt-2">
          <li>Word count tracking with minimum and maximum limits</li>
          <li>Required keyword detection that updates in real-time</li>
          <li>Detailed feedback on submission</li>
          <li>Scoring based on multiple criteria</li>
        </ul>
      </div>
    </main>
  );
} 