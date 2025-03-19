import Link from 'next/link'

const NavBar = () => {
  return (
    <div className="hidden sm:flex space-x-8 items-center">
      <Link href="/" className="hover:text-gray-600">Home</Link>
      <Link href="/courses" className="hover:text-gray-600">Courses</Link>
      <Link href="/exercises" className="hover:text-gray-600">Exercises</Link>
      <Link href="/exercise-showcase" className="hover:text-gray-600">Exercise Showcase</Link>
      <Link href="/word-scramble-index" className="hover:text-gray-600">Word Scramble</Link>
      <Link href="/about" className="hover:text-gray-600">About</Link>
    </div>
  )
}

export default NavBar 