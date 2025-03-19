'use client';

import React, { useCallback } from 'react';
import { ExerciseFactory } from '../components/exercises';
import { ExerciseProvider, Exercise, ExerciseType, Feedback, ExerciseAnswer } from '../context/ExerciseContext';

const InteractiveExerciseTestPage = () => {
  // Mock function to simulate API submission
  const handleSubmit = useCallback(async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log(`Exercise ID ${exerciseId} submitted with answer:`, answer);
    
    // Simple validation - for demo purposes
    let isCorrect = false;
    let message = "Incorrect answer. Try again.";
    let score = 0;
    
    // Check the answer against the exercise's expected correct answer
    const exercise = sampleExercises.find(ex => ex.id === exerciseId);
    
    if (exercise) {
      if (exercise.exercise_type === ExerciseType.MATCHING_WORDS) {
        if (Array.isArray(answer)) {
          // For matching exercises, compare the selected indices with correct_matches
          isCorrect = JSON.stringify(answer) === JSON.stringify(exercise.correct_matches);
          
          // Calculate partial score
          if (!isCorrect && Array.isArray(exercise.correct_matches)) {
            const correctCount = answer.filter((selected, index) => 
              selected === exercise.correct_matches?.[index]
            ).length;
            score = correctCount / exercise.correct_matches.length;
            message = `You got ${correctCount} out of ${exercise.correct_matches.length} matches correct.`;
          }
        }
      } else if (exercise.exercise_type === ExerciseType.WORD_SCRAMBLE) {
        if (typeof answer === 'string' && typeof exercise.sentence === 'string') {
          // For word scramble, compare with original sentence (ignoring case, extra spaces)
          const normalizedAnswer = answer.toLowerCase().trim().replace(/\s+/g, ' ');
          const normalizedCorrect = exercise.sentence.toLowerCase().trim().replace(/\s+/g, ' ');
          isCorrect = normalizedAnswer === normalizedCorrect;
          
          if (!isCorrect) {
            // Check if words are correct but order is wrong
            const answerWords = normalizedAnswer.split(' ');
            const correctWords = normalizedCorrect.split(' ');
            
            if (answerWords.length === correctWords.length) {
              const correctWordsCount = answerWords.filter(word => correctWords.includes(word)).length;
              score = correctWordsCount / correctWords.length * 0.5; // Partial credit
              message = `You've used the right words but the order isn't correct.`;
            }
          }
        }
      } else if (exercise.exercise_type === ExerciseType.SENTENCE_REORDERING) {
        if (Array.isArray(answer) && Array.isArray(exercise.correct_order)) {
          // For sentence reordering, compare the order of sentences
          isCorrect = JSON.stringify(answer) === JSON.stringify(exercise.correct_order);
          
          // Calculate partial score for sentences in correct positions
          if (!isCorrect) {
            const correctPositions = answer.filter((idx, position) => 
              idx === exercise.correct_order?.[position]
            ).length;
            score = correctPositions / exercise.correct_order.length;
            message = `You got ${correctPositions} out of ${exercise.correct_order.length} sentences in the correct position.`;
          }
        }
      }
      
      if (isCorrect) {
        message = "Great job! That's correct.";
        score = exercise?.max_score || 1;
      }
    }
    
    // Create feedback object
    const feedback: Feedback = {
      isCorrect,
      message,
      score
    };
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return feedback;
  }, []);

  return (
    <div className="container mx-auto p-6 max-w-4xl" suppressHydrationWarning>
      <h1 className="text-3xl font-bold mb-8">Interactive Exercise Test</h1>
      
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
    exercise_type: ExerciseType.MATCHING_WORDS,
    question: "Match each country with its capital city.",
    instructions: "Select the capital city for each country in the list.",
    items_a: ["France", "Japan", "Brazil", "Egypt", "Canada"],
    items_b: ["Paris", "Tokyo", "Brasília", "Cairo", "Ottawa"],
    correct_matches: [0, 1, 2, 3, 4], // Each index corresponds to the correct match in items_b
    max_score: 5
  },
  {
    id: 2,
    exercise_type: ExerciseType.MATCHING_WORDS,
    question: "Match each term with its definition.",
    instructions: "Pair each programming term with its correct definition.",
    items_a: ["Variable", "Function", "Array", "Loop", "Conditional"],
    items_b: [
      "A container for storing data values", 
      "A block of code designed to perform a particular task", 
      "A data structure used to store multiple values", 
      "A control structure that repeats a block of code", 
      "A statement that performs different actions based on whether a condition is true or false"
    ],
    correct_matches: [0, 1, 2, 3, 4],
    max_score: 5
  },
  {
    id: 3,
    exercise_type: ExerciseType.WORD_SCRAMBLE,
    question: "Rearrange the words to form a proper sentence.",
    instructions: "Put the words in the correct order to create a meaningful sentence.",
    sentence: "The quick brown fox jumps over the lazy dog",
    max_score: 2
  },
  {
    id: 4,
    exercise_type: ExerciseType.WORD_SCRAMBLE,
    question: "Arrange these words into a programming statement.",
    instructions: "Form a valid JavaScript conditional statement.",
    sentence: "if condition is true then execute this code",
    max_score: 2
  },
  {
    id: 5,
    exercise_type: ExerciseType.SENTENCE_REORDERING,
    question: "Arrange these sentences to form a coherent paragraph.",
    instructions: "Put the sentences in a logical order to form a paragraph about climate change.",
    sentences: [
      "Climate change is the long-term alteration of temperature and typical weather patterns.",
      "Human activities, particularly the burning of fossil fuels, are the primary cause of climate change.",
      "The effects of climate change include rising sea levels, extreme weather events, and disruptions to ecosystems.",
      "To address climate change, countries around the world are working to reduce greenhouse gas emissions.",
      "Individual actions, such as reducing energy consumption and supporting renewable energy, also play an important role."
    ],
    correct_order: [0, 1, 2, 3, 4],
    max_score: 5
  },
  {
    id: 6,
    exercise_type: ExerciseType.SENTENCE_REORDERING,
    question: "Arrange these sentences to form a coherent set of instructions.",
    instructions: "Put the sentences in the correct order to explain how to make a sandwich.",
    sentences: [
      "First, gather two slices of bread, your choice of filling, and condiments.",
      "Next, spread butter or mayonnaise on one side of each bread slice.",
      "Then, add your fillings such as cheese, meat, or vegetables.",
      "After that, place the second slice of bread on top with the buttered side facing in.",
      "Finally, cut the sandwich in half and serve on a plate."
    ],
    correct_order: [0, 1, 2, 3, 4],
    max_score: 5
  }
];

export default InteractiveExerciseTestPage; 