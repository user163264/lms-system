'use client';

import React from 'react';
import { Exercise, ExerciseType, Feedback, ExerciseAnswer } from '../../context/ExerciseContext';
import MultipleChoiceExercise from './MultipleChoiceExercise';
import TrueFalseExercise from './TrueFalseExercise';
import ShortAnswerExercise from './ShortAnswerExercise';
import FillBlanksExercise from './FillBlanksExercise';
import MatchingWordsExercise from './MatchingWordsExercise';
import WordScrambleExercise from './WordScrambleExercise';
import SentenceReorderingExercise from './SentenceReorderingExercise';
import ImageLabelingExercise from './ImageLabelingExercise';
import LongAnswerExercise from './LongAnswerExercise';
import ClozeTestExercise from './ClozeTestExercise';

// Interface for the factory component props
export interface ExerciseFactoryProps {
  exercise: Exercise;
  showFeedback?: boolean;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
  className?: string;
}

/**
 * Exercise Factory Component
 * 
 * Factory component that renders the appropriate exercise component
 * based on the exercise type. Acts as a single entry point for rendering
 * any exercise type.
 */
const ExerciseFactory: React.FC<ExerciseFactoryProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className
}) => {
  // Select the appropriate component based on exercise type
  switch (exercise.exercise_type) {
    case ExerciseType.MULTIPLE_CHOICE:
      return (
        <MultipleChoiceExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
    
    case ExerciseType.TRUE_FALSE:
      return (
        <TrueFalseExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
    
    case ExerciseType.SHORT_ANSWER:
      return (
        <ShortAnswerExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
    
    case ExerciseType.FILL_BLANK:
      return (
        <FillBlanksExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
    
    case ExerciseType.MATCHING_WORDS:
      return (
        <MatchingWordsExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
      
    case ExerciseType.WORD_SCRAMBLE:
      return (
        <WordScrambleExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
      
    case ExerciseType.SENTENCE_REORDERING:
      return (
        <SentenceReorderingExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
    
    case ExerciseType.IMAGE_LABELING:
      return (
        <ImageLabelingExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
      
    case ExerciseType.LONG_ANSWER:
      return (
        <LongAnswerExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
      
    case ExerciseType.CLOZE_TEST:
      return (
        <ClozeTestExercise
          exercise={exercise}
          showFeedback={showFeedback}
          onSubmit={onSubmit}
          className={className}
        />
      );
    
    // As more exercise types are implemented, add cases here
    
    default:
      // Placeholder for unimplemented exercise types
      return (
        <div className="p-4 border rounded bg-yellow-50 text-yellow-800">
          <h3 className="font-medium">Exercise Type Not Implemented</h3>
          <p>The exercise type &quot;{exercise.exercise_type}&quot; is not yet implemented.</p>
        </div>
      );
  }
};

export default ExerciseFactory; 