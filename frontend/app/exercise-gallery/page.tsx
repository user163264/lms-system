export default function ExerciseGalleryPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-bold text-blue-800 mb-2">Exercise Gallery</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Explore the various types of interactive exercises available in our Learning Management System.
          </p>
          <a href="/" className="inline-block mt-4 text-blue-600 hover:underline">
            ← Back to home
          </a>
        </header>

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Available Exercise Types</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {exerciseTypes.map((type) => (
              <a 
                key={type.id} 
                href={`/exercises/${type.id}`} 
                className="border-2 border-blue-500 rounded-lg overflow-hidden hover:shadow-lg hover:bg-blue-50 transition-all cursor-pointer"
              >
                <div className="bg-blue-50 p-4 border-b border-blue-300">
                  <h3 className="font-semibold text-blue-800">{type.name}</h3>
                </div>
                <div className="p-4">
                  <p className="text-gray-700 mb-4">{type.description}</p>
                  <div className="text-sm text-gray-500">ID: {type.id}</div>
                  <div className="mt-3 text-blue-600 font-medium">Try this exercise →</div>
                </div>
              </a>
            ))}
          </div>
        </div>
        
        {/* Information section */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">About Our Exercise System</h2>
          <p className="mb-4">
            Our Learning Management System supports a wide variety of exercise types to enhance the learning experience.
            These exercises are designed to test different cognitive skills and knowledge areas.
          </p>
          <p className="mb-4">
            Instructors can create custom exercises for their courses, and students can track their progress through 
            comprehensive analytics.
          </p>
          <h3 className="text-xl font-semibold mt-6 mb-3">Features:</h3>
          <ul className="list-disc pl-6 space-y-2">
            <li>Interactive exercise components with real-time feedback</li>
            <li>Support for various media types including text, images, and audio</li>
            <li>Accessibility-focused design for all learners</li>
            <li>Progress tracking and performance analytics</li>
            <li>Customizable difficulty levels and time limits</li>
          </ul>
        </div>
        
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Quick Navigation</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <a href="/word-scramble-index" className="block p-3 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Word Scramble Index</h3>
              <p className="text-gray-600">Practice word scramble exercises</p>
            </a>
            <a href="/scramble" className="block p-3 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Scramble Exercises</h3>
              <p className="text-gray-600">Word scramble practice activities</p>
            </a>
            <a href="/lessons" className="block p-3 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Lessons</h3>
              <p className="text-gray-600">Browse available lessons</p>
            </a>
            <a href="/exercises/demo" className="block p-3 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
              <h3 className="font-bold text-blue-700">Exercise Demo</h3>
              <p className="text-gray-600">Try exercise demonstrations</p>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

// Exercise type data
const exerciseTypes = [
  {
    id: 'multiple_choice',
    name: 'Multiple Choice',
    description: 'Students select one or more correct options from a list of choices. Good for testing recognition and recall.'
  },
  {
    id: 'true_false',
    name: 'True/False',
    description: 'Students determine whether a statement is true or false. Effective for quick knowledge checks.'
  },
  {
    id: 'short_answer',
    name: 'Short Answer',
    description: 'Students provide a brief text response, typically a few words or a single sentence.'
  },
  {
    id: 'long_answer',
    name: 'Long Answer',
    description: 'Students write extended responses, essays, or paragraphs to demonstrate deeper understanding.'
  },
  {
    id: 'fill_blank',
    name: 'Fill in the Blanks',
    description: 'Students complete sentences by filling in missing words, testing vocabulary and comprehension.'
  },
  {
    id: 'cloze_test',
    name: 'Cloze Test',
    description: 'Students fill in blanks in a text using words from a provided word bank.'
  },
  {
    id: 'image_labeling',
    name: 'Image Labeling',
    description: 'Students identify and label specific parts of an image, useful for visual subjects.'
  },
  {
    id: 'matching_words',
    name: 'Matching Words',
    description: 'Students match items from two columns, such as terms with definitions or causes with effects.'
  },
  {
    id: 'sentence_reordering',
    name: 'Sentence Reordering',
    description: 'Students arrange sentences in the correct logical or chronological order.'
  },
  {
    id: 'word_scramble',
    name: 'Word Scramble',
    description: 'Students rearrange words to form a complete, meaningful sentence.'
  }
]; 