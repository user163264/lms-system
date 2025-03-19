/**
 * Exercise Types and Interfaces
 * 
 * This file contains type definitions for all exercise components
 */

export enum ExerciseType {
  MULTIPLE_CHOICE = 'multiple_choice',
  TRUE_FALSE = 'true_false',
  SHORT_ANSWER = 'short_answer',
  LONG_ANSWER = 'long_answer',
  FILL_BLANKS = 'fill_blanks',
  CLOZE_TEST = 'cloze_test',
  IMAGE_LABELING = 'image_labeling',
  MATCHING_WORDS = 'matching_words',
  SENTENCE_REORDERING = 'sentence_reordering',
  WORD_SCRAMBLE = 'word_scramble'
}

export interface BaseExerciseProps {
  id: string;
  type: ExerciseType;
  question: string;
  instructions?: string;
  feedback?: string;
  isSubmitted?: boolean;
  isCorrect?: boolean;
  onSubmit?: (answer: any) => void;
  onReset?: () => void;
}

// Multiple Choice Exercise Types
export interface MultipleChoiceExerciseProps extends BaseExerciseProps {
  type: ExerciseType.MULTIPLE_CHOICE;
  options: string[];
  correctAnswer: number | number[];
  allowMultiple?: boolean;
}

// True/False Exercise Types
export interface TrueFalseExerciseProps extends BaseExerciseProps {
  type: ExerciseType.TRUE_FALSE;
  correctAnswer: boolean;
}

// Short Answer Exercise Types
export interface ShortAnswerExerciseProps extends BaseExerciseProps {
  type: ExerciseType.SHORT_ANSWER;
  correctAnswer: string | string[];
  caseSensitive?: boolean;
}

// Long Answer Exercise Types
export interface LongAnswerExerciseProps extends BaseExerciseProps {
  type: ExerciseType.LONG_ANSWER;
  minLength?: number;
  maxLength?: number;
  sampleAnswer?: string;
}

// Fill in the Blanks Exercise Types
export interface FillBlanksExerciseProps extends BaseExerciseProps {
  type: ExerciseType.FILL_BLANKS;
  text: string;
  blanks: { id: string; answer: string }[];
}

// Cloze Test Exercise Types
export interface ClozeTestExerciseProps extends BaseExerciseProps {
  type: ExerciseType.CLOZE_TEST;
  text: string;
  answers: { [key: string]: string };
  wordBank?: string[];
}

// Image Labeling Exercise Types
export interface ImageLabelingExerciseProps extends BaseExerciseProps {
  type: ExerciseType.IMAGE_LABELING;
  imageUrl: string;
  labels: { id: string; x: number; y: number; answer: string }[];
}

// Matching Words Exercise Types
export interface MatchingWordsExerciseProps extends BaseExerciseProps {
  type: ExerciseType.MATCHING_WORDS;
  leftItems: { id: string; text: string }[];
  rightItems: { id: string; text: string }[];
  correctPairs: { left: string; right: string }[];
}

// Sentence Reordering Exercise Types
export interface SentenceReorderingExerciseProps extends BaseExerciseProps {
  type: ExerciseType.SENTENCE_REORDERING;
  sentences: string[];
  correctOrder: number[];
}

// Word Scramble Exercise Types
export interface WordScrambleExerciseProps extends BaseExerciseProps {
  type: ExerciseType.WORD_SCRAMBLE;
  words: string[];
  correctOrder: number[];
}

export type ExerciseProps = 
  | MultipleChoiceExerciseProps
  | TrueFalseExerciseProps
  | ShortAnswerExerciseProps
  | LongAnswerExerciseProps
  | FillBlanksExerciseProps
  | ClozeTestExerciseProps
  | ImageLabelingExerciseProps
  | MatchingWordsExerciseProps
  | SentenceReorderingExerciseProps
  | WordScrambleExerciseProps; 