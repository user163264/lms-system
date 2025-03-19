'use client';

import React, { createContext, useContext, useReducer, ReactNode, useCallback, useRef } from 'react';
import api from '../services/api';

// Exercise types matching the backend
export enum ExerciseType {
  MULTIPLE_CHOICE = 'multiple_choice',
  TRUE_FALSE = 'true_false',
  FILL_BLANK = 'fill_blank',
  SHORT_ANSWER = 'short_answer',
  MATCHING_WORDS = 'matching_words',
  WORD_SCRAMBLE = 'word_scramble',
  SENTENCE_REORDERING = 'sentence_reordering',
  IMAGE_LABELING = 'image_labeling',
  LONG_ANSWER = 'long_answer',
  CLOZE_TEST = 'cloze_test'
}

// Submission status
export enum SubmissionStatus {
  IDLE = 'idle',
  SUBMITTING = 'submitting',
  SUBMITTED = 'submitted',
  ERROR = 'error'
}

// Exercise data interface
export interface Exercise {
  id: number;
  exercise_type: ExerciseType;
  question: string;
  instructions?: string;
  options?: string[];
  correct_answer?: string[];
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
  template_id?: number;
  [key: string]: unknown;
}

// User response types
export type ExerciseAnswer = 
  | string 
  | string[] 
  | number[] 
  | Record<string, string> 
  | Record<string, unknown>;

// Feedback type
export interface Feedback {
  isCorrect: boolean;
  score: number;
  message: string;
  detailedResults?: Record<string, unknown>;
}

// Exercise state interface
export interface ExerciseState {
  exercise: Exercise | null;
  userAnswer: ExerciseAnswer | null;
  submissionStatus: SubmissionStatus;
  feedback: Feedback | null;
  loading: boolean;
  error: string | null;
}

// Action types
export enum ActionType {
  SET_EXERCISE = 'SET_EXERCISE',
  UPDATE_ANSWER = 'UPDATE_ANSWER',
  SUBMIT_ANSWER = 'SUBMIT_ANSWER',
  SUBMIT_ANSWER_SUCCESS = 'SUBMIT_ANSWER_SUCCESS',
  SUBMIT_ANSWER_ERROR = 'SUBMIT_ANSWER_ERROR',
  RESET_EXERCISE = 'RESET_EXERCISE',
  SET_LOADING = 'SET_LOADING',
  SET_ERROR = 'SET_ERROR'
}

// Action interface
interface ExerciseAction {
  type: ActionType;
  payload?: any;
}

// Initial state
const initialState: ExerciseState = {
  exercise: null,
  userAnswer: null,
  submissionStatus: SubmissionStatus.IDLE,
  feedback: null,
  loading: false,
  error: null
};

// Reducer function
function exerciseReducer(state: ExerciseState, action: ExerciseAction): ExerciseState {
  switch (action.type) {
    case ActionType.SET_EXERCISE:
      return {
        ...state,
        exercise: action.payload,
        userAnswer: null,
        submissionStatus: SubmissionStatus.IDLE,
        feedback: null,
        error: null
      };
    
    case ActionType.UPDATE_ANSWER:
      return {
        ...state,
        userAnswer: action.payload
      };
    
    case ActionType.SUBMIT_ANSWER:
      return {
        ...state,
        submissionStatus: SubmissionStatus.SUBMITTING
      };
    
    case ActionType.SUBMIT_ANSWER_SUCCESS:
      return {
        ...state,
        submissionStatus: SubmissionStatus.SUBMITTED,
        feedback: action.payload
      };
    
    case ActionType.SUBMIT_ANSWER_ERROR:
      return {
        ...state,
        submissionStatus: SubmissionStatus.ERROR,
        error: action.payload
      };
    
    case ActionType.RESET_EXERCISE:
      return {
        ...state,
        userAnswer: null,
        submissionStatus: SubmissionStatus.IDLE,
        feedback: null,
        error: null
      };
    
    case ActionType.SET_LOADING:
      return {
        ...state,
        loading: action.payload
      };
    
    case ActionType.SET_ERROR:
      return {
        ...state,
        error: action.payload
      };
    
    default:
      return state;
  }
}

// Create context
interface ExerciseContextType {
  state: ExerciseState;
  setExercise: (exercise: Exercise) => void;
  updateAnswer: (answer: ExerciseAnswer) => void;
  submitAnswer: () => Promise<void>;
  resetExercise: () => void;
}

const ExerciseContext = createContext<ExerciseContextType | undefined>(undefined);

// Provider props
interface ExerciseProviderProps {
  children: ReactNode;
  onSubmit?: (answer: ExerciseAnswer, exerciseId: number) => Promise<Feedback>;
}

// Provider component
export function ExerciseProvider({ 
  children, 
  onSubmit 
}: ExerciseProviderProps) {
  const [state, dispatch] = useReducer(exerciseReducer, initialState);
  const isSubmittingRef = useRef(false);

  const setExercise = useCallback((exercise: Exercise) => {
    dispatch({ type: ActionType.SET_EXERCISE, payload: exercise });
  }, []);

  const updateAnswer = useCallback((answer: ExerciseAnswer) => {
    dispatch({ type: ActionType.UPDATE_ANSWER, payload: answer });
  }, []);

  const submitAnswer = useCallback(async () => {
    if (!state.exercise || !state.userAnswer) return;
    if (state.submissionStatus === SubmissionStatus.SUBMITTING || isSubmittingRef.current) return;
    
    isSubmittingRef.current = true;
    dispatch({ type: ActionType.SUBMIT_ANSWER });
    
    try {
      // If custom submission handler is provided, use it
      if (onSubmit) {
        const feedback = await onSubmit(state.userAnswer, state.exercise.id);
        dispatch({ type: ActionType.SUBMIT_ANSWER_SUCCESS, payload: feedback });
      } else {
        // Use the centralized API service to submit the answer
        const feedback = await api.exercises.submitAnswer(state.exercise.id, state.userAnswer);
        dispatch({ type: ActionType.SUBMIT_ANSWER_SUCCESS, payload: feedback });
      }
    } catch (error) {
      dispatch({ 
        type: ActionType.SUBMIT_ANSWER_ERROR, 
        payload: 'Failed to submit answer. Please try again.' 
      });
    } finally {
      isSubmittingRef.current = false;
    }
  }, [state.exercise, state.userAnswer, onSubmit, state.submissionStatus]);

  const resetExercise = useCallback(() => {
    dispatch({ type: ActionType.RESET_EXERCISE });
  }, []);

  const value = {
    state,
    setExercise,
    updateAnswer,
    submitAnswer,
    resetExercise
  };

  return (
    <ExerciseContext.Provider value={value}>
      {children}
    </ExerciseContext.Provider>
  );
}

// Custom hook to use the context
export function useExercise() {
  const context = useContext(ExerciseContext);
  
  if (context === undefined) {
    throw new Error('useExercise must be used within an ExerciseProvider');
  }
  
  return context;
}

export default ExerciseContext; 