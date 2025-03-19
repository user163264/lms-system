'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export default function WordScrambleIndexPage() {
  const [publicIP, setPublicIP] = useState<string>('');
  
  useEffect(() => {
    // Get the current hostname
    const hostname = window.location.hostname;
    const port = window.location.port;
    
    // Set public IP for accessing the pages
    setPublicIP(port ? `${hostname}:${port}` : hostname);
  }, []);

  return (
    <div className="container mx-auto py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-4">Word Scramble Test Suite</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            A collection of test pages and debugging tools for the Word Scramble component
          </p>
        </header>
        
        <div className="mb-8 bg-blue-50 p-4 rounded-lg">
          <h2 className="font-medium text-lg text-blue-800 mb-2">Public Access URLs</h2>
          <p className="text-blue-700 mb-3">
            These URLs can be used to access the test pages from any device on the network:
          </p>
          <div className="space-y-2">
            {publicIP && (
              <>
                <div className="p-2 bg-white rounded-md border border-blue-200 flex justify-between items-center">
                  <span className="font-mono text-blue-900">http://{publicIP}/word-scramble-debug</span>
                  <a 
                    href={`http://${publicIP}/word-scramble-debug`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-blue-500 text-white text-sm rounded-md"
                  >
                    Open
                  </a>
                </div>
                <div className="p-2 bg-white rounded-md border border-blue-200 flex justify-between items-center">
                  <span className="font-mono text-blue-900">http://{publicIP}/word-scramble-test</span>
                  <a 
                    href={`http://${publicIP}/word-scramble-test`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-blue-500 text-white text-sm rounded-md"
                  >
                    Open
                  </a>
                </div>
                <div className="p-2 bg-white rounded-md border border-blue-200 flex justify-between items-center">
                  <span className="font-mono text-blue-900">http://{publicIP}/test/word-scramble</span>
                  <a 
                    href={`http://${publicIP}/test/word-scramble`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-blue-500 text-white text-sm rounded-md"
                  >
                    Open
                  </a>
                </div>
              </>
            )}
          </div>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <h2 className="text-xl font-semibold mb-3">Debug Version</h2>
            <p className="text-gray-600 mb-4">
              Enhanced version with debug overlay, state monitoring, and performance tracking
            </p>
            <ul className="mb-4 space-y-2 text-sm">
              <li className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Console logging of all interactions
              </li>
              <li className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Performance metrics
              </li>
              <li className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                State visualization
              </li>
            </ul>
            <Link 
              href="/word-scramble-debug" 
              className="block w-full text-center bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Open Debug Version
            </Link>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <h2 className="text-xl font-semibold mb-3">Test Version</h2>
            <p className="text-gray-600 mb-4">
              Multiple test cases with different sentence structures and complexities
            </p>
            <ul className="mb-4 space-y-2 text-sm">
              <li className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Multiple test scenarios
              </li>
              <li className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Submission history
              </li>
              <li className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Automated test script
              </li>
            </ul>
            <Link 
              href="/word-scramble-test" 
              className="block w-full text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Open Test Version
            </Link>
          </div>
        </div>
        
        <div className="mt-8 p-4 bg-gray-100 rounded-lg">
          <h2 className="font-medium text-lg mb-3">Documentation</h2>
          <div className="prose max-w-none">
            <p>
              The Word Scramble component has been extensively optimized to prevent UI jitter using:
            </p>
            <ul>
              <li>Stable word management with unique IDs for duplicate words</li>
              <li>Fixed positioning layout for the word bank</li>
              <li>Single state updates to minimize re-renders</li>
              <li>Instructions toggle for improved UX</li>
            </ul>
            <p>
              The debug version includes additional instrumentation to monitor performance
              and component behavior. It tracks render counts, state changes, and interaction timings.
            </p>
          </div>
          
          <div className="mt-4 text-right">
            <Link href="/" className="text-blue-600 hover:text-blue-800">
              Return to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
} 