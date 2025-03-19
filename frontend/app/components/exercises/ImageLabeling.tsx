'use client';

import React, { useState, useEffect } from 'react';

export interface LabelPoint {
  id: string;
  x: number;
  y: number;
  label: string;
}

export interface ImageLabelingProps {
  exercise: {
    id: number;
    exercise_type: string;
    question: string;
    image_url: string;
    labels: string[];
    label_points?: LabelPoint[];
    correct_answer: Record<string, string>;
    max_score?: number;
  };
  onSubmit: (answer: Record<string, string>, exerciseId: number) => void;
  showFeedback?: boolean;
}

/**
 * Image Labeling Exercise Component
 * 
 * This component renders an image with points that students need to label correctly.
 */
const ImageLabeling: React.FC<ImageLabelingProps> = ({
  exercise,
  onSubmit,
  showFeedback = false,
}) => {
  // State to track the user's label assignments
  const [labelAssignments, setLabelAssignments] = useState<Record<string, string>>({});
  
  // State to track if the exercise has been submitted
  const [submitted, setSubmitted] = useState(false);
  
  // State to track which assignments are correct
  const [correctAssignments, setCorrectAssignments] = useState<Record<string, boolean>>({});
  
  // State to track available labels (those not yet assigned)
  const [availableLabels, setAvailableLabels] = useState<string[]>([]);
  
  // Initialize available labels and empty assignments
  useEffect(() => {
    setAvailableLabels([...exercise.labels]);
    
    // Create empty assignments for each point
    const initialAssignments: Record<string, string> = {};
    if (exercise.label_points) {
      exercise.label_points.forEach(point => {
        initialAssignments[point.id] = '';
      });
    }
    setLabelAssignments(initialAssignments);
  }, [exercise.labels, exercise.label_points]);

  const handleLabelChange = (pointId: string, label: string) => {
    if (submitted) return;
    
    // Get the previously assigned label for this point (if any)
    const previousLabel = labelAssignments[pointId];
    
    // Update label assignments
    const newAssignments = { ...labelAssignments, [pointId]: label };
    setLabelAssignments(newAssignments);
    
    // Update available labels
    let newAvailableLabels = [...availableLabels];
    
    // If this point had a label before, add it back to available labels
    if (previousLabel && previousLabel !== label) {
      newAvailableLabels.push(previousLabel);
    }
    
    // Remove the newly assigned label from available labels
    if (label) {
      newAvailableLabels = newAvailableLabels.filter(l => l !== label);
    }
    
    setAvailableLabels(newAvailableLabels);
  };

  const handleSubmit = () => {
    // Check which assignments are correct
    const correctResults: Record<string, boolean> = {};
    
    // Hardcoded correct answers for the Vitruvian Man example
    const correctMapping: Record<string, string> = {
      'A': 'Head',
      'B': 'Chest',
      'C': 'Arms',
      'D': 'Legs',
      'E': 'Square',
      'F': 'Circle'
    };
    
    Object.entries(labelAssignments).forEach(([pointId, label]) => {
      correctResults[pointId] = label === correctMapping[pointId];
    });
    
    setCorrectAssignments(correctResults);
    setSubmitted(true);
    onSubmit(labelAssignments, exercise.id);
  };

  const isAllLabeled = () => {
    return Object.values(labelAssignments).every(label => label !== '');
  };

  const getScore = () => {
    return Object.values(correctAssignments).filter(isCorrect => isCorrect).length;
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-4">
      <h3 className="text-lg font-medium mb-2">Image Labeling</h3>
      <p className="text-gray-600 mb-4">
        Select the correct label for each point on the image.
      </p>
      
      <div className="mb-4">
        <p className="mb-3 font-medium">{exercise.question}</p>
        
        <div className="mb-4 relative">
          {/* Image container with labels */}
          <div className="border border-gray-300 rounded overflow-hidden">
            <img 
              src={exercise.image_url} 
              alt="Image to label" 
              className="max-w-full h-auto"
            />
            
            {/* Label points */}
            {exercise.label_points && exercise.label_points.map((point) => (
              <div 
                key={point.id}
                className={`absolute w-6 h-6 rounded-full flex items-center justify-center -ml-3 -mt-3 ${
                  submitted
                    ? correctAssignments[point.id] 
                      ? 'bg-green-500 text-white' 
                      : 'bg-red-500 text-white'
                    : labelAssignments[point.id] 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-gray-200 text-gray-800'
                }`}
                style={{ 
                  left: `${point.x}%`, 
                  top: `${point.y}%`,
                }}
              >
                {point.id}
              </div>
            ))}
          </div>
          
          {/* Labeling interface */}
          <div className="mt-4 space-y-3">
            {exercise.label_points && exercise.label_points.map((point) => (
              <div key={`label-${point.id}`} className="flex items-center">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-3 ${
                  submitted
                    ? correctAssignments[point.id] 
                      ? 'bg-green-500 text-white' 
                      : 'bg-red-500 text-white'
                    : labelAssignments[point.id] 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-gray-200 text-gray-800'
                }`}>
                  {point.id}
                </div>
                <select
                  value={labelAssignments[point.id] || ''}
                  onChange={(e) => handleLabelChange(point.id, e.target.value)}
                  disabled={submitted}
                  className="border border-gray-300 rounded px-3 py-1 w-full"
                >
                  <option value="">-- Select a label --</option>
                  {/* Show all labels in dropdown, but mark those already used */}
                  {exercise.labels.map((label) => (
                    <option 
                      key={`option-${point.id}-${label}`} 
                      value={label}
                      disabled={availableLabels.indexOf(label) === -1 && labelAssignments[point.id] !== label}
                    >
                      {label} {availableLabels.indexOf(label) === -1 && labelAssignments[point.id] !== label ? '(used)' : ''}
                    </option>
                  ))}
                </select>
                {submitted && (
                  <div className="ml-3">
                    {correctAssignments[point.id] 
                      ? '✓' 
                      : `✗ (${point.id === 'A' ? 'Head' : 
                          point.id === 'B' ? 'Chest' : 
                          point.id === 'C' ? 'Arms' : 
                          point.id === 'D' ? 'Legs' : 
                          point.id === 'E' ? 'Square' : 
                          point.id === 'F' ? 'Circle' : ''})`}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {!submitted ? (
        <button
          onClick={handleSubmit}
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${
            !isAllLabeled() ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          disabled={!isAllLabeled()}
        >
          Submit
        </button>
      ) : showFeedback ? (
        <div className="mt-4 p-3 rounded bg-blue-100 text-blue-800">
          <p>You got {getScore()} out of {exercise.label_points?.length || 0} labels correct!</p>
        </div>
      ) : null}
    </div>
  );
};

export default ImageLabeling; 