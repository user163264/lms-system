/**
 * API Service for Spotvogel LMS
 * This file centralizes all API calls to maintain consistency across the frontend
 */

import { Exercise, ExerciseAnswer, Feedback } from '../context/ExerciseContext';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * Custom fetch wrapper with error handling and JSON parsing
 */
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, options);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json() as T;
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Exercise API functions
 */
export const exerciseApi = {
  /**
   * Get all exercises for a specific lesson
   */
  getExercisesByLessonId: (lessonId: string | number): Promise<Exercise[]> => {
    return apiFetch<Exercise[]>(`/exercises/?lesson_id=${lessonId}`);
  },

  /**
   * Get a specific exercise by ID
   */
  getExerciseById: (exerciseId: number): Promise<Exercise> => {
    return apiFetch<Exercise>(`/exercises/${exerciseId}`);
  },

  /**
   * Submit an answer for an exercise
   */
  submitAnswer: (exerciseId: number, answer: ExerciseAnswer, userId?: string): Promise<Feedback> => {
    return apiFetch<Feedback>(`/exercises/submit/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        exercise_id: exerciseId,
        answer: answer,
        user_id: userId,
      }),
    });
  },
};

/**
 * Lesson API functions
 */
export const lessonApi = {
  /**
   * Get a specific lesson by ID
   */
  getLessonById: (lessonId: string | number): Promise<any> => {
    return apiFetch<any>(`/lessons/${lessonId}`);
  },
  
  /**
   * Get all lessons
   */
  getAllLessons: (): Promise<any[]> => {
    return apiFetch<any[]>(`/lessons/`);
  },
};

/**
 * Submission API functions
 */
export const submissionApi = {
  /**
   * Get all submissions for a user
   */
  getUserSubmissions: (userId: string): Promise<any[]> => {
    return apiFetch<any[]>(`/submissions/?user_id=${userId}`);
  },
  
  /**
   * Create a new submission record
   */
  createSubmission: (exerciseId: number, answer: ExerciseAnswer, userId?: string): Promise<any> => {
    return apiFetch<any>(`/submissions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        exercise_id: exerciseId,
        answer: answer,
        user_id: userId,
      }),
    });
  },
};

// Export a default API object for convenience
const api = {
  exercises: exerciseApi,
  lessons: lessonApi,
  submissions: submissionApi,
};

export default api; 