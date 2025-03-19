"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";

type Lesson = {
  id: string;
  title: string;
  description: string;
};

const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://13.42.249.90/api";

export default function LessonsPage() {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Use useMemo to avoid unnecessary recomputation
  const apiUrl = useMemo(() => `${baseUrl.replace(/\/$/, "")}/lessons`, []);

  useEffect(() => {
    fetch(apiUrl)
      .then((res) => res.json())
      .then((data) => {
        console.log("API Response:", data);
        if (Array.isArray(data)) {
          setLessons(data);
        } else {
          setError("Invalid data format received.");
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching lessons:", err);
        setError("Failed to fetch lessons.");
        setLoading(false);
      });
  }, [apiUrl]); // ESLint will now recognize apiUrl as stable

  if (loading) return <p>Loading lessons...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="min-h-screen p-10 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Available Lessons</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {lessons.map((lesson) => (
          <Link key={lesson.id} href={`/lessons/${lesson.id}`}>
            <div className="p-6 bg-white shadow-lg rounded-xl hover:bg-blue-100 cursor-pointer transition">
              <h2 className="text-xl font-semibold">{lesson.title}</h2>
              <p className="text-gray-600">{lesson.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
