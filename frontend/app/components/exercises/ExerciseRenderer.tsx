'use client';

import React from 'react';
import FillInBlanks from './FillInBlanks';
import TrueFalse from './TrueFalse';
import MultipleChoice from './MultipleChoice';
import ClozeTestWithWordBank from './ClozeTestWithWordBank';
import ShortAnswer from './ShortAnswer';
import MatchingWords from './MatchingWords';
import SentenceReordering from './SentenceReordering';
import LongAnswer from './LongAnswer';
import WordScramble from './WordScramble';
import ImageLabeling from './ImageLabeling';
import HydrationSuppressor from './utils/HydrationSuppressor';

export type ExerciseAnswer = string | string[] | number[] | Record<string, unknown>;

export interface Exercise {
  id: number;
  exercise_type: string;
  question: string;
  options?: string[];
  correct_answer: string[];
  word_bank?: string[];
  items_a?: string[];
  items_b?: string[];
  correct_matches?: number[];
  sentences?: string[];
  correct_order?: number[];
  min_words?: number;
  max_words?: number;
  required_keywords?: string[];
  sentence?: string;
  image_url?: string;
  labels?: string[];
  label_points?: Array<{id: string; x: number; y: number; label: string}>;
  max_score?: number;
  [key: string]: unknown; // For any additional fields
}

interface ExerciseRendererProps {
  exercise: Exercise;
  onSubmit: (answer: ExerciseAnswer, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Exercise Renderer Component
 * 
 * This component renders the appropriate exercise component based on the exercise type.
 * It acts as a central dispatcher for all exercise types.
 */
const ExerciseRenderer: React.FC<ExerciseRendererProps> = ({
  exercise,
  onSubmit,
  showFeedback = false
}) => {
  // Render the appropriate exercise component based on type
  switch (exercise.exercise_type) {
    case 'fill_blank':
      return (
        <HydrationSuppressor>
          <FillInBlanks 
            exercise={exercise} 
            onSubmit={(answer, id) => onSubmit(answer, id)} 
            showFeedback={showFeedback} 
          />
        </HydrationSuppressor>
      );
      
    case 'true_false':
      return (
        <HydrationSuppressor>
          <TrueFalse 
            exercise={exercise} 
            onSubmit={(answer, id) => onSubmit(answer, id)} 
            showFeedback={showFeedback} 
          />
        </HydrationSuppressor>
      );
      
    case 'multiple_choice':
      return (
        <HydrationSuppressor>
          <MultipleChoice 
            exercise={exercise} 
            onSubmit={(answer, id) => onSubmit(answer, id)} 
            showFeedback={showFeedback} 
          />
        </HydrationSuppressor>
      );
      
    case 'cloze_test':
      return (
        <HydrationSuppressor>
          <ClozeTestWithWordBank 
            exercise={exercise} 
            onSubmit={(answers, id) => onSubmit(answers, id)} 
            showFeedback={showFeedback} 
          />
        </HydrationSuppressor>
      );
      
    case 'short_answer':
      return (
        <HydrationSuppressor>
          <ShortAnswer
            exercise={exercise}
            onSubmit={(answer, id) => onSubmit(answer, id)}
            showFeedback={showFeedback}
          />
        </HydrationSuppressor>
      );
      
    case 'matching_words':
      return (
        <HydrationSuppressor>
          <MatchingWords
            exercise={exercise as Exercise & { items_a: string[], items_b: string[], correct_matches: number[] }}
            onSubmit={(answers, id) => onSubmit(answers, id)}
            showFeedback={showFeedback}
          />
        </HydrationSuppressor>
      );
      
    case 'sentence_reordering':
      return (
        <HydrationSuppressor>
          <SentenceReordering
            exercise={exercise as Exercise & { sentences: string[], correct_order: number[] }}
            onSubmit={(order, id) => onSubmit(order, id)}
            showFeedback={showFeedback}
          />
        </HydrationSuppressor>
      );
      
    case 'long_answer':
      return (
        <HydrationSuppressor>
          <LongAnswer
            exercise={exercise}
            onSubmit={(answer, id) => onSubmit(answer, id)}
            showFeedback={showFeedback}
          />
        </HydrationSuppressor>
      );
      
    case 'word_scramble':
      return (
        <HydrationSuppressor>
          <WordScramble
            exercise={exercise as Exercise & { sentence: string }}
            onSubmit={(answer, id) => onSubmit(answer, id)}
            showFeedback={showFeedback}
          />
        </HydrationSuppressor>
      );
      
    case 'image_labeling':
      return (
        <HydrationSuppressor>
          <ImageLabeling
            exercise={exercise as Exercise & { 
              image_url: string, 
              labels: string[], 
              label_points: Array<{id: string; x: number; y: number; label: string}>,
              correct_answer: Record<string, string>
            }}
            onSubmit={(answer, id) => onSubmit(answer, id)}
            showFeedback={showFeedback}
          />
        </HydrationSuppressor>
      );
      
    default:
      // Fallback for unsupported exercise types
      return (
        <div className="bg-white rounded-xl shadow-md p-6 mb-4">
          <h3 className="text-lg font-medium text-red-500">
            Unsupported Exercise Type: {exercise.exercise_type}
          </h3>
          <p className="text-gray-600">
            This exercise type is not currently supported. Please contact your instructor.
          </p>
          <pre className="mt-4 p-3 bg-gray-100 rounded overflow-auto text-sm">
            {JSON.stringify(exercise, null, 2)}
          </pre>
        </div>
      );
  }
};

export default ExerciseRenderer; 