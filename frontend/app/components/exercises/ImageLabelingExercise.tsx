'use client';

import React, { useState, useEffect } from 'react';
import InteractiveExercise, { InteractiveExerciseProps } from './base/InteractiveExercise';
import { Exercise, ExerciseAnswer, Feedback, SubmissionStatus, useExercise } from '../../context/ExerciseContext';

export interface LabelPoint {
  id: string;
  x: number;
  y: number;
  label?: string;
}

export interface ImageLabelingExerciseProps extends Omit<InteractiveExerciseProps, 'exercise'> {
  exercise: Exercise;
}

/**
 * Image Labeling Exercise Component
 * 
 * This component renders an image with points that students need to label correctly.
 * Users select labels from a dropdown for each point on the image.
 */
const ImageLabelingExercise: React.FC<ImageLabelingExerciseProps> = ({
  exercise,
  showFeedback = false,
  onSubmit,
  className = ''
}) => {
  const { state, updateAnswer, submitAnswer, resetExercise } = useExercise();
  
  // State to track the user's label assignments
  const [labelAssignments, setLabelAssignments] = useState<Record<string, string>>({});
  
  // State to track which assignments are correct (for feedback)
  const [correctAssignments, setCorrectAssignments] = useState<Record<string, boolean>>({});
  
  // State to track available labels (those not yet assigned)
  const [availableLabels, setAvailableLabels] = useState<string[]>([]);
  
  // Initialize available labels and empty assignments
  useEffect(() => {
    if (exercise.labels) {
      setAvailableLabels([...exercise.labels]);
    }
    
    // Create empty assignments for each point
    const initialAssignments: Record<string, string> = {};
    if (exercise.label_points) {
      exercise.label_points.forEach(point => {
        initialAssignments[point.id] = '';
      });
    }
    setLabelAssignments(initialAssignments);
  }, [exercise.labels, exercise.label_points]);
  
  // Update the context when label assignments change
  useEffect(() => {
    if (Object.keys(labelAssignments).length > 0) {
      updateAnswer(labelAssignments);
    }
  }, [labelAssignments, updateAnswer]);
  
  // Handle label change for a point
  const handleLabelChange = (pointId: string, label: string) => {
    if (state.submissionStatus === SubmissionStatus.SUBMITTED) return;
    
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
  
  // Check if all points have been labeled
  const isAllLabeled = () => {
    return Object.values(labelAssignments).every(label => label !== '');
  };
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isAllLabeled() || state.submissionStatus === SubmissionStatus.SUBMITTING) {
      return;
    }
    
    // Check which assignments are correct
    const correctResults: Record<string, boolean> = {};
    
    // Check if we have a correct_label_mapping, otherwise use correct_answer
    const correctMapping = 
      (exercise as any).correct_label_mapping || 
      (exercise.correct_answer && typeof exercise.correct_answer === 'object' ? exercise.correct_answer : {});
    
    Object.entries(labelAssignments).forEach(([pointId, label]) => {
      correctResults[pointId] = label === correctMapping[pointId];
    });
    
    setCorrectAssignments(correctResults);
    await submitAnswer();
  };
  
  // Handle reset
  const handleReset = () => {
    // Reset label assignments
    const initialAssignments: Record<string, string> = {};
    if (exercise.label_points) {
      exercise.label_points.forEach(point => {
        initialAssignments[point.id] = '';
      });
    }
    
    setLabelAssignments(initialAssignments);
    if (exercise.labels) {
      setAvailableLabels([...exercise.labels]);
    }
    setCorrectAssignments({});
    resetExercise();
  };
  
  // Determine if the form is disabled
  const isDisabled = state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Determine if the submit button should be disabled
  const isSubmitDisabled = 
    !isAllLabeled() || 
    state.submissionStatus === SubmissionStatus.SUBMITTING || 
    state.submissionStatus === SubmissionStatus.SUBMITTED;
  
  // Get score for feedback
  const getScore = () => {
    if (!state.feedback) return 0;
    return Object.values(correctAssignments).filter(isCorrect => isCorrect).length;
  };
  
  return (
    <InteractiveExercise
      exercise={exercise}
      showFeedback={showFeedback}
      onSubmit={onSubmit}
      className={className}
    >
      <form onSubmit={handleSubmit} className="space-y-4" suppressHydrationWarning>
        <div className="mb-4 relative">
          {/* Image container with label points */}
          <div className="border border-gray-300 rounded overflow-hidden">
            {exercise.image_url && (
              <img 
                src={exercise.image_url} 
                alt="Image to label" 
                className="max-w-full h-auto"
              />
            )}
            
            {/* Label points overlaid on the image */}
            {exercise.label_points && exercise.label_points.map((point) => (
              <div 
                key={point.id}
                className={`absolute w-6 h-6 rounded-full flex items-center justify-center -ml-3 -mt-3 ${
                  state.submissionStatus === SubmissionStatus.SUBMITTED && Object.keys(correctAssignments).length > 0
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
                  state.submissionStatus === SubmissionStatus.SUBMITTED && Object.keys(correctAssignments).length > 0
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
                  disabled={isDisabled}
                  className="border border-gray-300 rounded px-3 py-1 w-full"
                >
                  <option value="">-- Select a label --</option>
                  {/* Show all labels in dropdown, but mark those already used */}
                  {exercise.labels && exercise.labels.map((label) => (
                    <option 
                      key={`option-${point.id}-${label}`} 
                      value={label}
                      disabled={availableLabels.indexOf(label) === -1 && labelAssignments[point.id] !== label}
                    >
                      {label} {availableLabels.indexOf(label) === -1 && labelAssignments[point.id] !== label ? '(used)' : ''}
                    </option>
                  ))}
                </select>
                {state.submissionStatus === SubmissionStatus.SUBMITTED && state.feedback && (
                  <div className="ml-3">
                    {correctAssignments[point.id] 
                      ? '✓' 
                      : `✗ (${
                        ((exercise as any).correct_label_mapping && (exercise as any).correct_label_mapping[point.id]) || 
                        (exercise.correct_answer && typeof exercise.correct_answer === 'object' ? 
                          (exercise.correct_answer as any)[point.id] : '')
                      })`}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
        
        <div className="flex space-x-4">
          {state.submissionStatus !== SubmissionStatus.SUBMITTED ? (
            <button
              type="submit"
              className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${
                isSubmitDisabled ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={isSubmitDisabled}
            >
              Submit
            </button>
          ) : (
            <button
              type="button"
              onClick={handleReset}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </form>
    </InteractiveExercise>
  );
};

export default ImageLabelingExercise; 