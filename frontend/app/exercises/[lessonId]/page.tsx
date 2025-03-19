"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ExerciseRenderer from "../../components/exercises/ExerciseRenderer";
import { Exercise as RendererExercise } from "../../components/exercises/ExerciseRenderer";
import api from "../../services/api";
import { Exercise, ExerciseAnswer, Feedback } from "../../context/ExerciseContext";

// Type adapter to convert between API Exercise and Renderer Exercise
const adaptExerciseForRenderer = (exercise: Exercise): RendererExercise => {
  return {
    ...exercise,
    // Ensure correct_answer is always an array, never undefined
    correct_answer: exercise.correct_answer || [],
  } as RendererExercise;
};

export default function ExercisePage() {
  const { lessonId } = useParams();
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submissions, setSubmissions] = useState<Record<number, ExerciseAnswer>>({});

  useEffect(() => {
    setLoading(true);
    
    // Use the API service instead of direct fetch
    api.exercises.getExercisesByLessonId(lessonId as string)
      .then((data) => {
        console.log("Exercises data:", data);
        setExercises(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching exercises:", err);
        setError(err.message);
        setLoading(false);
      });
  }, [lessonId]);

  const handleSubmitAnswer = async (answer: ExerciseAnswer, exerciseId: number): Promise<Feedback> => {
    console.log(`Submitted answer for exercise ${exerciseId}:`, answer);
    
    // Store the submission locally
    setSubmissions(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
    
    try {
      // Use the API service to submit the answer
      const feedback = await api.exercises.submitAnswer(exerciseId, answer);
      return feedback;
    } catch (error) {
      console.error('Error submitting answer:', error);
      return {
        isCorrect: false,
        score: 0,
        message: 'Failed to submit answer. Please try again.'
      };
    }
  };

  // Display submission status (for debugging)
  const submissionCount = Object.keys(submissions).length;

  if (loading) return <p className="p-10">Loading exercises...</p>;
  if (error) return <p className="p-10 text-red-500">Error: {error}</p>;
  if (exercises.length === 0) return <p className="p-10">No exercises found for this lesson.</p>;

  return (
    <div className="min-h-screen p-10 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Exercises</h1>
      
      {submissionCount > 0 && (
        <p className="mb-4 text-green-600">
          You have submitted {submissionCount} out of {exercises.length} exercises.
        </p>
      )}
      
      <div className="space-y-6">
        {exercises.map((exercise) => (
          <ExerciseRenderer
            key={exercise.id}
            exercise={adaptExerciseForRenderer(exercise)}
            onSubmit={handleSubmitAnswer}
            showFeedback={true}
          />
        ))}
      </div>
    </div>
  );
}
