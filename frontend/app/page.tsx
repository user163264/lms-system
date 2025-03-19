import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">LMS Dashboard</h1>
      <div className="grid grid-cols-1 gap-6">
        <Link href="/home" className="px-6 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 text-center">
          Go to Home
        </Link>
      </div>
    </div>
  );
}
