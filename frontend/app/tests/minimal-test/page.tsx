'use client';

import React, { useState, useEffect } from 'react';

export default function MinimalTestPage() {
  const [isClient, setIsClient] = useState(false);
  const [counter, setCounter] = useState(0);
  
  useEffect(() => {
    console.log('MinimalTestPage mounted on client');
    setIsClient(true);
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Minimal Test Page</h1>
      
      <div className="p-4 bg-blue-100 rounded mb-4">
        <p><strong>Client Rendering:</strong> {isClient ? "Active" : "Inactive"}</p>
      </div>
      
      <div className="border bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-4">Counter Test</h2>
        <p className="mb-4">Current count: {counter}</p>
        <button 
          onClick={() => setCounter(prev => prev + 1)}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mr-2"
        >
          Increment
        </button>
        <button 
          onClick={() => setCounter(0)}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Reset
        </button>
      </div>
    </div>
  );
} 