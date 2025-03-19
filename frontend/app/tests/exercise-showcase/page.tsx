'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import ExerciseRenderer from '../components/exercises/ExerciseRenderer';
import { Exercise as RendererExercise } from '../components/exercises/ExerciseRenderer';
import { ExerciseAnswer, Feedback, ExerciseType } from '../context/ExerciseContext';
import api from '../services/api';

// Helper function to send logs to the server
const serverLog = async (message: string, data?: any) => {
  const logData = {
    message,
    data,
    timestamp: new Date().toISOString(),
    page: 'exercise-showcase',
  };
  
  console.log(message, data); // Log to browser console
  
  try {
    // Send log to server
    await fetch('/api/debug-log', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(logData),
    });
  } catch (error) {
    console.error('Error sending log to server:', error);
  }
};

// Track component loading status
const loadStatus = {
  WordScramble: false,
  MultipleChoice: false,
  ShortAnswer: false,
  LongAnswer: false,
  TrueFalse: false,
  FillInBlanks: false,
  MatchingWords: false,
  ImageLabeling: false,
  SentenceReordering: false,
  ClozeTestWithWordBank: false,
};

// Dynamically import components with SSR disabled
const WordScramble = dynamic(() => {
  serverLog('Loading WordScramble component');
  return import('../components/exercises/WordScramble').then(mod => {
    loadStatus.WordScramble = true;
    serverLog('WordScramble component loaded successfully');
    return mod;
  }).catch(err => {
    serverLog('Error loading WordScramble component', err);
    throw err;
  });
}, { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading WordScramble component...</div>
});

const MultipleChoice = dynamic(() => {
  serverLog('Loading MultipleChoice component');
  return import('../components/exercises/MultipleChoice').then(mod => {
    loadStatus.MultipleChoice = true;
    serverLog('MultipleChoice component loaded successfully');
    return mod;
  }).catch(err => {
    serverLog('Error loading MultipleChoice component', err);
    throw err;
  });
}, { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading MultipleChoice component...</div>
});

const ShortAnswer = dynamic(() => {
  serverLog('Loading ShortAnswer component');
  return import('../components/exercises/ShortAnswer').then(mod => {
    loadStatus.ShortAnswer = true;
    serverLog('ShortAnswer component loaded successfully');
    return mod;
  });
}, { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading ShortAnswer component...</div>
});

const LongAnswer = dynamic(() => import('../components/exercises/LongAnswer'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading LongAnswer component...</div>
});

const TrueFalse = dynamic(() => import('../components/exercises/TrueFalse'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading TrueFalse component...</div>
});

const FillInBlanks = dynamic(() => import('../components/exercises/FillInBlanks'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading FillInBlanks component...</div>
});

const MatchingWords = dynamic(() => import('../components/exercises/MatchingWords'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading MatchingWords component...</div>
});

const ImageLabeling = dynamic(() => import('../components/exercises/ImageLabeling'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading ImageLabeling component...</div>
});

const SentenceReordering = dynamic(() => import('../components/exercises/SentenceReordering'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading SentenceReordering component...</div>
});

const ClozeTestWithWordBank = dynamic(() => import('../components/exercises/ClozeTestWithWordBank'), { 
  ssr: false,
  loading: () => <div className="p-4 bg-blue-100 rounded">Loading ClozeTestWithWordBank component...</div>
});

export default function ExerciseShowcase() {
  const router = useRouter();
  const [results, setResults] = useState<Record<number, any>>({});
  const [isClient, setIsClient] = useState(false);
  const [loadingState, setLoadingState] = useState<string>("initializing");
  const [feedback, setFeedback] = useState<Record<number, Feedback>>({});
  
  // Set isClient to true when component mounts on client
  useEffect(() => {
    serverLog('ExerciseShowcasePage mounted on client');
    setIsClient(true);
    setLoadingState("client-ready");
  }, []);

  // Debug log when isClient changes
  useEffect(() => {
    serverLog('isClient state changed', { isClient });
  }, [isClient]);
  
  // Generic submit handlers for different component types
  const handleStringSubmit = (answer: string, exerciseId: number) => {
    serverLog(`String submit for exercise ${exerciseId}`, { answer });
    setResults(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
  };
  
  const handleNumberArraySubmit = (answer: number[], exerciseId: number) => {
    serverLog(`Number array submit for exercise ${exerciseId}`, { answer });
    setResults(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
  };
  
  const handleRecordSubmit = (answer: Record<string, string>, exerciseId: number) => {
    serverLog(`Record submit for exercise ${exerciseId}`, { answer });
    setResults(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
  };
  
  const handleStringArraySubmit = (answer: string[], exerciseId: number) => {
    serverLog(`String array submit for exercise ${exerciseId}`, { answer });
    setResults(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
  };

  // Safer error boundary approach
  const renderExercise = (Component: any, props: any) => {
    try {
      return <Component {...props} />;
    } catch (error) {
      serverLog('Error rendering exercise component', { error, props });
      return (
        <div className="p-4 bg-red-100 rounded">
          <p className="text-red-700">Error rendering component. See console for details.</p>
        </div>
      );
    }
  };

  // Demo exercises representing all 10 types
  const demoExercises: RendererExercise[] = [
    {
      id: 1,
      exercise_type: ExerciseType.MULTIPLE_CHOICE,
      question: "Which of the following is a JavaScript framework?",
      options: ["React", "Python", "HTML", "SQL"],
      correct_answer: ["React"]
    },
    {
      id: 2,
      exercise_type: ExerciseType.TRUE_FALSE,
      question: "HTML is a programming language.",
      correct_answer: ["false"]
    },
    {
      id: 3,
      exercise_type: ExerciseType.FILL_BLANK,
      question: "Complete the sentence: JavaScript is a _____ language.",
      correct_answer: ["programming", "scripting"]
    },
    {
      id: 4,
      exercise_type: ExerciseType.SHORT_ANSWER,
      question: "What does CSS stand for?",
      correct_answer: ["Cascading Style Sheets"],
      min_words: 1,
      max_words: 5
    },
    {
      id: 5,
      exercise_type: ExerciseType.MATCHING_WORDS,
      question: "Match the languages with their use cases",
      items_a: ["JavaScript", "SQL", "Python", "HTML"],
      items_b: ["Web Interactivity", "Database Queries", "Data Science", "Web Structure"],
      correct_matches: [0, 1, 2, 3],
      correct_answer: ["0,1,2,3"]
    },
    {
      id: 6,
      exercise_type: ExerciseType.WORD_SCRAMBLE,
      question: "Unscramble the words to form a sentence",
      sentence: "React makes building user interfaces easy",
      correct_answer: ["React makes building user interfaces easy"]
    },
    {
      id: 7,
      exercise_type: ExerciseType.SENTENCE_REORDERING,
      question: "Place these steps in the correct order to create a React component",
      sentences: [
        "Import React", 
        "Define the component function", 
        "Return JSX", 
        "Export the component"
      ],
      correct_order: [0, 1, 2, 3],
      correct_answer: ["0,1,2,3"]
    },
    {
      id: 8,
      exercise_type: ExerciseType.IMAGE_LABELING,
      question: "Label the parts of the HTML document",
      image_url: "https://i.imgur.com/RVEMt4E.png",
      labels: ["HTML", "Head", "Body", "Title"],
      label_points: [
        {id: "1", x: 10, y: 10, label: "HTML"},
        {id: "2", x: 30, y: 30, label: "Head"},
        {id: "3", x: 50, y: 50, label: "Body"},
        {id: "4", x: 70, y: 30, label: "Title"}
      ],
      correct_answer: ["HTML", "Head", "Body", "Title"]
    },
    {
      id: 9,
      exercise_type: ExerciseType.LONG_ANSWER,
      question: "Explain the difference between var, let, and const in JavaScript.",
      min_words: 20,
      max_words: 100,
      required_keywords: ["scope", "hoisting", "reassign"],
      correct_answer: [""]
    },
    {
      id: 10,
      exercise_type: ExerciseType.CLOZE_TEST,
      question: "Fill in the blanks with the correct words",
      sentence: "React is a JavaScript __1__ for building user __2__. It was developed by __3__.",
      word_bank: ["library", "framework", "interfaces", "applications", "Google", "Facebook", "Amazon"],
      correct_answer: ["library", "interfaces", "Facebook"]
    }
  ];

  const handleSubmitAnswer = async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log(`Submitted answer for exercise ${exerciseId}:`, answer);
    
    // Evaluate the answer locally for demo purposes
    let isCorrect = false;
    let score = 0;
    let message = "Incorrect. Try again!";
    
    const exercise = demoExercises.find(ex => ex.id === exerciseId);
    
    if (exercise) {
      // Simple evaluation logic (just for demo)
      if (exercise.exercise_type === ExerciseType.MULTIPLE_CHOICE || 
          exercise.exercise_type === ExerciseType.TRUE_FALSE) {
        isCorrect = JSON.stringify(answer) === JSON.stringify(exercise.correct_answer);
      } else {
        // For other types, always say it's correct in this demo
        isCorrect = true;
      }
      
      score = isCorrect ? 1 : 0;
      message = isCorrect ? "Correct! Great job!" : "Incorrect. Try again!";
    }
    
    const feedback: Feedback = { isCorrect, score, message };
    
    // Store feedback
    setFeedback(prev => ({
      ...prev,
      [exerciseId]: feedback
    }));
    
    return feedback;
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-10 text-blue-800">
          Spotvogel LMS - Exercise Type Showcase
        </h1>
        
        <p className="text-center mb-8 text-gray-600">
          This page demonstrates all 10 exercise types available in the Spotvogel Learning Management System.
        </p>
        
        <div className="space-y-10">
          {demoExercises.map((exercise) => (
            <div key={exercise.id} className="bg-white rounded-xl shadow-md overflow-hidden">
              <div className="px-4 py-3 bg-blue-50 border-b border-blue-100">
                <h3 className="text-lg font-medium text-blue-800">
                  Type: {exercise.exercise_type.replace(/_/g, ' ').toUpperCase()}
                </h3>
              </div>
              
              <div className="p-6">
                <ExerciseRenderer
                  key={exercise.id}
                  exercise={exercise}
                  onSubmit={handleSubmitAnswer}
                  showFeedback={true}
                />
              </div>
              
              {feedback[exercise.id] && (
                <div className={`px-6 py-3 ${feedback[exercise.id].isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
                  <p className={`text-sm ${feedback[exercise.id].isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                    {feedback[exercise.id].message}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
        
        <div className="mt-10 text-center text-sm text-gray-500">
          <p>© {new Date().getFullYear()} Spotvogel LMS. All exercises are for demonstration purposes.</p>
        </div>
      </div>
    </div>
  );
} 