'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function TestsIndex() {
  const [filter, setFilter] = useState('');
  
  const testPages = [
    { path: '/tests/cloze-test-test', name: 'Cloze Test', description: 'Test for cloze text exercises' },
    { path: '/tests/exercise-test', name: 'Exercise Test', description: 'General exercise testing' },
    { path: '/tests/image-labeling-test', name: 'Image Labeling', description: 'Test for image labeling exercises' },
    { path: '/tests/input-exercise-test', name: 'Input Exercise', description: 'Test for input-based exercises' },
    { path: '/tests/interactive-exercise-test', name: 'Interactive Exercise', description: 'Test for interactive exercises' },
    { path: '/tests/long-answer-test', name: 'Long Answer', description: 'Test for long answer exercises' },
    { path: '/tests/minimal-test', name: 'Minimal Test', description: 'Minimal test case' },
    { path: '/tests/word-scramble-test', name: 'Word Scramble', description: 'Test for word scramble exercises' },
    { path: '/tests/direct-showcase', name: 'Direct Showcase', description: 'Direct component showcases' },
    { path: '/tests/exercise-showcase', name: 'Exercise Showcase', description: 'Exercise component showcases' },
    { path: '/tests/simplified-showcase', name: 'Simplified Showcase', description: 'Simplified component showcases' },
    { path: '/tests/word-scramble-debug', name: 'Word Scramble Debug', description: 'Debug page for word scramble' },
  ];
  
  const filteredPages = testPages.filter(page => 
    page.name.toLowerCase().includes(filter.toLowerCase()) || 
    page.description.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Test Pages Index</h1>
      
      <div className="mb-6">
        <input
          type="text"
          placeholder="Filter test pages..."
          className="w-full p-2 border rounded"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredPages.map((page) => (
          <Link href={page.path} key={page.path}>
            <div className="border rounded p-4 hover:bg-gray-50 cursor-pointer h-full">
              <h2 className="font-bold text-lg">{page.name}</h2>
              <p className="text-sm text-gray-600">{page.description}</p>
            </div>
          </Link>
        ))}
      </div>
      
      {filteredPages.length === 0 && (
        <p className="text-center text-gray-500 mt-8">No test pages match your filter.</p>
      )}
    </div>
  );
} 