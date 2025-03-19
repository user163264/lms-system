'use client';

import React, { useState, useEffect } from 'react';
import WordScrambleDebug from '../components/exercises/WordScrambleDebug';

// Sample exercises for debug testing
const exercises = [
  {
    id: 1,
    title: "Simple Sentence",
    exercise: {
      id: 101,
      exercise_type: 'word_scramble',
      question: 'Arrange the words to form a correct sentence:',
      sentence: 'The quick brown fox jumps over the lazy dog',
      correct_answer: ['The quick brown fox jumps over the lazy dog'],
      max_score: 1
    }
  },
  {
    id: 2,
    title: "Duplicate Words",
    exercise: {
      id: 102,
      exercise_type: 'word_scramble',
      question: 'Create a sentence with repeated words:',
      sentence: 'The dog saw the cat and the cat saw the mouse',
      correct_answer: ['The dog saw the cat and the cat saw the mouse'],
      max_score: 1
    }
  },
  {
    id: 3,
    title: "Short Technical Phrase",
    exercise: {
      id: 103,
      exercise_type: 'word_scramble',
      question: 'Arrange these technical words:',
      sentence: 'React components should avoid unnecessary renders',
      correct_answer: ['React components should avoid unnecessary renders'],
      max_score: 1
    }
  }
];

// Safe browser check to avoid SSR issues
const isBrowser = typeof window !== 'undefined';

export default function WordScrambleDebugPage() {
  const [selectedExercise, setSelectedExercise] = useState(exercises[0]);
  const [results, setResults] = useState<{id: number, answer: string, timestamp: string}[]>([]);
  const [perfStats, setPerfStats] = useState<{
    renderTime: number[],
    interactionTime: number[]
  }>({
    renderTime: [],
    interactionTime: []
  });
  
  // Environment info state
  const [envInfo, setEnvInfo] = useState({
    userAgent: 'Loading...',
    platform: 'Loading...',
    screen: 'Loading...',
    viewport: 'Loading...',
    online: false
  });
  
  // Update environment info after mounting
  useEffect(() => {
    setEnvInfo({
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      screen: `${window.screen.width}×${window.screen.height}`,
      viewport: `${window.innerWidth}×${window.innerHeight}`,
      online: navigator.onLine
    });
  }, []);
  
  // Track performance stats
  useEffect(() => {
    if (!isBrowser) return;
    
    const now = performance.now();
    const initialRenderTime = now;
    
    console.log('[DEBUG] Initial page render at:', initialRenderTime);
    
    // Record first interaction timing
    const recordFirstInteraction = () => {
      const interactionTime = performance.now();
      console.log('[DEBUG] First interaction at:', interactionTime, 'Time since load:', interactionTime - initialRenderTime);
      
      setPerfStats(prev => ({
        ...prev,
        interactionTime: [...prev.interactionTime, interactionTime - initialRenderTime]
      }));
      
      // Remove listener after first interaction
      document.removeEventListener('click', recordFirstInteraction);
    };
    
    document.addEventListener('click', recordFirstInteraction);
    
    return () => {
      document.removeEventListener('click', recordFirstInteraction);
    };
  }, []);
  
  // Handler for submission
  const handleSubmit = (answer: string, exerciseId: number) => {
    console.log(`Exercise ${exerciseId} submitted with answer: ${answer}`);
    const timestamp = new Date().toISOString();
    setResults(prev => [...prev, {id: exerciseId, answer, timestamp}]);
  };
  
  // Share debug data (could send to backend or analytics)
  const shareDebugData = () => {
    if (!isBrowser) return;
    
    const debugData = {
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      renderStats: perfStats,
      exercises: exercises.map(ex => ex.id),
      results,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      }
    };
    
    console.log('[DEBUG] Collected data:', debugData);
    alert('Debug data logged to console. In a real app, this would be sent to a server.');
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <div className="bg-gray-800 text-white p-4 rounded-lg mb-6">
        <h1 className="text-2xl font-bold">Word Scramble Debug Mode</h1>
        <p className="text-gray-300 mt-2">
          This page contains a debug-enhanced version of the Word Scramble component with extensive logging and state tracking.
          Open your browser console to see detailed debug information.
        </p>
        <div className="mt-4 flex gap-4">
          <button 
            onClick={() => isBrowser && console.clear()} 
            className="px-3 py-1 bg-gray-600 hover:bg-gray-700 rounded"
          >
            Clear Console
          </button>
          <button 
            onClick={shareDebugData} 
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded"
          >
            Share Debug Data
          </button>
          <button 
            onClick={() => {isBrowser && localStorage.clear(); isBrowser && window.location.reload()}}
            className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded"
          >
            Reset Storage & Reload
          </button>
        </div>
      </div>
      
      {/* Exercise selector */}
      <div className="mb-8 bg-gray-50 p-4 rounded-lg border border-gray-200">
        <h2 className="text-lg font-medium mb-3">Select Test Case:</h2>
        <div className="flex flex-wrap gap-2">
          {exercises.map(ex => (
            <button
              key={ex.id}
              onClick={() => setSelectedExercise(ex)}
              className={`px-3 py-2 rounded text-sm ${
                selectedExercise.id === ex.id 
                  ? 'bg-blue-100 border-blue-500 border-2' 
                  : 'bg-white border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {ex.title}
            </button>
          ))}
        </div>
      </div>
      
      {/* Debug info */}
      <div className="mb-6 bg-gray-50 p-3 rounded border border-gray-200 text-sm">
        <div className="flex justify-between">
          <div>
            <span className="font-medium">Exercise ID:</span> {selectedExercise.exercise.id}
          </div>
          <div>
            <span className="font-medium">Word count:</span> {selectedExercise.exercise.sentence.split(' ').length}
          </div>
          <div>
            <span className="font-medium">Character count:</span> {selectedExercise.exercise.sentence.length}
          </div>
        </div>
      </div>
      
      {/* Component under test */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">{selectedExercise.title}</h2>
        <WordScrambleDebug
          exercise={selectedExercise.exercise} 
          onSubmit={handleSubmit} 
          showFeedback={true} 
        />
      </div>
      
      {/* Network status - only render on client */}
      {isBrowser && (
        <div className="mb-6 bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <h3 className="font-medium text-yellow-800 mb-2">Network Status</h3>
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div>
              <span className="font-medium">Online:</span> {envInfo.online ? 'Yes ✓' : 'No ✗'}
            </div>
            <div>
              <span className="font-medium">Connection:</span> <span id="connection-type">Checking...</span>
            </div>
            <div>
              <span className="font-medium">Latency:</span> <span id="latency">Checking...</span>
            </div>
          </div>
          <script dangerouslySetInnerHTML={{ __html: `
            // Check connection type
            if ('connection' in navigator) {
              const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
              if (connection) {
                document.getElementById('connection-type').textContent = connection.effectiveType || 'Unknown';
              }
            } else {
              document.getElementById('connection-type').textContent = 'API not available';
            }
            
            // Check latency
            const startTime = performance.now();
            fetch('/api/ping', { cache: 'no-store' })
              .then(response => response.json())
              .then(data => {
                const latency = Math.round(performance.now() - startTime);
                document.getElementById('latency').textContent = latency + 'ms';
              })
              .catch(err => {
                document.getElementById('latency').textContent = 'Error';
                console.error('Latency check failed:', err);
              });
          ` }}></script>
        </div>
      )}
      
      {/* Results section */}
      {results.length > 0 && (
        <div className="mt-8 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-medium mb-2">Submission History:</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-200">
                  <th className="p-2 text-left">Time</th>
                  <th className="p-2 text-left">Exercise</th>
                  <th className="p-2 text-left">Answer</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result, index) => {
                  const exerciseInfo = exercises.find(ex => ex.exercise.id === result.id);
                  return (
                    <tr key={index} className="border-b border-gray-300">
                      <td className="p-2 text-gray-600">{new Date(result.timestamp).toLocaleTimeString()}</td>
                      <td className="p-2">{exerciseInfo?.title || `Exercise ${result.id}`}</td>
                      <td className="p-2 font-mono">{result.answer}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {/* Browser info */}
      <div className="mt-8 p-4 bg-gray-800 text-gray-300 rounded-lg text-xs">
        <h3 className="font-medium text-white mb-2">Debug Environment:</h3>
        <div className="grid grid-cols-2 gap-2">
          <div><span className="text-gray-400">User Agent:</span> {envInfo.userAgent}</div>
          <div><span className="text-gray-400">Platform:</span> {envInfo.platform}</div>
          <div><span className="text-gray-400">Screen:</span> {envInfo.screen}</div>
          <div><span className="text-gray-400">Viewport:</span> {envInfo.viewport}</div>
          <div><span className="text-gray-400">Next.js:</span> 15.2.1</div>
          <div><span className="text-gray-400">React:</span> 18.x</div>
        </div>
      </div>
    </div>
  );
} 