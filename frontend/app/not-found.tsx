"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

export default function NotFoundPage() {
  const router = useRouter();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Image
        src="/404-image.png" // Image must be in public folder
        alt="404 Not Found"
        width={500}
        height={350}
        priority
      />
      <h1 className="text-4xl font-bold text-gray-800 mt-4">Oops! Page Not Found</h1>
      <p className="text-gray-600 mt-2">The page you are looking for doesn’t exist.</p>
      <button
        className="mt-6 px-6 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600"
        onClick={() => router.push("/")}
      >
        Go Back Home
      </button>
    </div>
  );
}
