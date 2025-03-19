'use client';

import React, { useState, useEffect } from 'react';

export interface SentenceReorderingProps {
  exercise: {
    id: number;
    exercise_type: string;
    sentences: string[];
    correct_order: number[]; // Indices of the correct order
    max_score?: number;
  };
  onSubmit: (answer: number[], exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Sentence Reordering Exercise Component
 * 
 * This component renders a sentence reordering exercise where students
 * drag and drop sentences to arrange them in the correct order.
 */
const SentenceReordering: React.FC<SentenceReorderingProps> = ({
  exercise,
  onSubmit,
  showFeedback = false,
}) => {
  const [sentences, setSentences] = useState<{text: string, originalIndex: number}[]>([]);
  const [currentOrder, setCurrentOrder] = useState<number[]>([]);
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [draggingIndex, setDraggingIndex] = useState<number | null>(null);

  // Initialize with shuffled sentences
  useEffect(() => {
    // Create an array of sentence objects with their original indices
    const sentenceObjects = exercise.sentences.map((text, index) => ({
      text,
      originalIndex: index,
    }));

    // Shuffle the sentence objects
    const shuffled = [...sentenceObjects];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }

    setSentences(shuffled);
    setCurrentOrder(shuffled.map(s => s.originalIndex));
  }, [exercise.sentences]);

  const handleDragStart = (index: number) => {
    if (submitted) return;
    setDraggingIndex(index);
  };

  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    if (draggingIndex === null || draggingIndex === index || submitted) return;

    // Reorder the sentences
    const newSentences = [...sentences];
    const draggedSentence = newSentences[draggingIndex];
    newSentences.splice(draggingIndex, 1);
    newSentences.splice(index, 0, draggedSentence);

    setSentences(newSentences);
    setCurrentOrder(newSentences.map(s => s.originalIndex));
    setDraggingIndex(index);
  };

  const handleDragEnd = () => {
    setDraggingIndex(null);
  };

  const handleSubmit = () => {
    // Check if the current order matches the correct order
    const correct = JSON.stringify(currentOrder) === JSON.stringify(exercise.correct_order);
    setIsCorrect(correct);
    setSubmitted(true);
    onSubmit(currentOrder, exercise.id);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <h3 className="text-lg font-medium mb-2">Sentence Reordering</h3>
      <p className="text-gray-600 mb-4">Drag and drop the sentences to arrange them in the correct order.</p>
      
      <div className="mb-4 space-y-2">
        {sentences.map((sentence, index) => (
          <div
            key={`sentence-${sentence.originalIndex}`}
            draggable={!submitted}
            onDragStart={() => handleDragStart(index)}
            onDragOver={(e) => handleDragOver(e, index)}
            onDragEnd={handleDragEnd}
            className={`p-3 border rounded cursor-grab ${
              submitted 
                ? currentOrder[index] === exercise.correct_order[index]
                  ? 'border-green-500 bg-green-50'
                  : 'border-red-500 bg-red-50'
                : draggingIndex === index
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-blue-300'
            }`}
          >
            <div className="flex items-center">
              <span className="mr-3 w-6 h-6 flex items-center justify-center bg-gray-200 rounded-full text-sm">
                {index + 1}
              </span>
              <span>{sentence.text}</span>
            </div>
          </div>
        ))}
      </div>
      
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          Submit
        </button>
      ) : showFeedback ? (
        <div className={`mt-4 p-3 rounded ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {isCorrect 
            ? '✓ Correct! The sentences are in the right order.' 
            : (
              <div>
                <p>✗ Incorrect. The correct order is:</p>
                <ol className="list-decimal pl-5 mt-2">
                  {exercise.correct_order.map((index) => (
                    <li key={`correct-${index}`}>
                      {exercise.sentences[index]}
                    </li>
                  ))}
                </ol>
              </div>
            )
          }
        </div>
      ) : null}
    </div>
  );
};

export default SentenceReordering; 