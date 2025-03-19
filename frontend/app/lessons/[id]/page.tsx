"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import api from "../../services/api";

type Lesson = {
  id: string;
  title: string;
  content: string;
};

export default function LessonDetail() {
  const { id } = useParams();
  const [lesson, setLesson] = useState<Lesson | null>(null);

  useEffect(() => {
    api.lessons.getLessonById(id as string)
      .then((data) => setLesson(data));
  }, [id]);

  if (!lesson) return <p>Loading...</p>;

  return (
    <div className="min-h-screen p-10 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">{lesson.title}</h1>
      <p className="text-gray-700">{lesson.content}</p>

      <Link href={`/exercises/${lesson.id}`}>
        <button className="mt-6 px-6 py-2 bg-green-500 text-white rounded-lg shadow-md hover:bg-green-600">
          Start Exercises
        </button>
      </Link>
    </div>
  );
}
