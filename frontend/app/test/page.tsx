export default function TestPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-bold text-blue-800 mb-2">Test Page</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            This is a test page to verify routing functionality.
          </p>
          <a href="/" className="inline-block mt-4 text-blue-600 hover:underline">
            ← Back to home
          </a>
        </header>

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Test Components</h2>
          
          <div className="grid gap-4">
            <div className="border p-4 rounded-lg">
              <h3 className="font-bold text-xl mb-2">Component 1</h3>
              <p className="text-gray-700">This is a test component demonstrating layout.</p>
              <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                Test Button
              </button>
            </div>
            <div className="border p-4 rounded-lg">
              <h3 className="font-bold text-xl mb-2">Component 2</h3>
              <p className="text-gray-700">Another test component showing Tailwind styling.</p>
              <div className="mt-4 flex space-x-2">
                <div className="w-10 h-10 bg-red-500 rounded-full"></div>
                <div className="w-10 h-10 bg-green-500 rounded-full"></div>
                <div className="w-10 h-10 bg-blue-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Exercise Links</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a href="/exercise-gallery" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Exercise Gallery</h3>
              <p className="text-gray-600">View all available exercise types</p>
            </a>
            <a href="/word-scramble-index" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Word Scramble Index</h3>
              <p className="text-gray-600">Index of word scramble exercises</p>
            </a>
            <a href="/scramble" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Scramble Exercises</h3>
              <p className="text-gray-600">Word scramble practice activities</p>
            </a>
            <a href="/lessons" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Lessons</h3>
              <p className="text-gray-600">Browse available lessons</p>
            </a>
            <a href="/exercises/demo" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Exercise Demo</h3>
              <p className="text-gray-600">Demonstration exercises</p>
            </a>
            <a href="/tailwind-test" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Tailwind Test</h3>
              <p className="text-gray-600">Test of Tailwind CSS styling</p>
            </a>
            <a href="/exercises" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">All Exercises</h3>
              <p className="text-gray-600">Main exercises page</p>
            </a>
            <a href="/home" className="block p-4 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Home</h3>
              <p className="text-gray-600">Home page with navigation</p>
            </a>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Test Information</h2>
          <p className="mb-4">
            This page was created to test the Next.js App Router functionality. It demonstrates:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>Page routing with the App Router</li>
            <li>Tailwind CSS styling</li>
            <li>Component organization</li>
            <li>Server-side rendering</li>
          </ul>
          <p className="mt-4 text-sm text-gray-500">
            Created: {new Date().toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
} 