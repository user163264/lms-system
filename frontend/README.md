# LMS Frontend

This directory contains the frontend code for the Learning Management System (LMS), built with Next.js.

## Project Structure

```
lms/frontend/
│
├── app/                      # Next.js App Router
│   ├── api/                  # API endpoints for frontend
│   ├── components/           # Reusable components
│   │   ├── common/           # Common UI components
│   │   ├── layout/           # Layout components (headers, footers, etc.)
│   │   └── exercises/        # Exercise components
│   │       ├── base/         # Base exercise components
│   │       └── types/        # Exercise type implementations
│   ├── features/             # Feature-based directories
│   │   ├── auth/             # Authentication feature
│   │   ├── courses/          # Course management feature
│   │   ├── dashboard/        # Dashboard feature
│   │   ├── exercises/        # Exercise feature pages
│   │   └── lessons/          # Lesson feature pages
│   ├── context/              # React context providers
│   ├── services/             # API service functions
│   ├── utils/                # Utility functions
│   ├── tests/                # Test pages (consolidated)
│   └── page.tsx              # Homepage
│
├── public/                   # Static assets
│   ├── images/               # Image assets
│   └── icons/                # Icon assets 
│
├── .next/                    # Next.js build output (gitignored)
├── node_modules/             # Node.js dependencies (gitignored)
├── .env.local                # Environment variables (gitignored)
├── next.config.js            # Next.js configuration
├── package.json              # Project dependencies and scripts
├── postcss.config.js         # PostCSS configuration
├── tailwind.config.js        # Tailwind CSS configuration
└── tsconfig.json             # TypeScript configuration
```

## Features

- **User Authentication** - JWT-based authentication with login/logout
- **Course Management** - Browse and enroll in courses
- **Exercise System** - Interactive exercises with automatic grading
- **Dashboard** - Student and teacher dashboards showing progress
- **Responsive Design** - Mobile-friendly interface with Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18.0.0 or later
- npm or yarn or pnpm

### Installation

1. Install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Create a `.env.local` file in the root directory with the following:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Development

### Key Technologies

- **Next.js** - React framework for frontend
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **React Context** - State management
- **Fetch API** - Data fetching

### Development Best Practices

1. Follow consistent naming conventions (PascalCase for components)
2. Use TypeScript for all components and utilities
3. Create modular, reusable components
4. Write responsive designs using Tailwind CSS
5. Use the App Router pattern for routing
6. Follow error handling best practices
7. Place components in appropriate feature directories

### Adding a New Page

1. Determine if the page belongs to a specific feature
2. Create a new directory in the appropriate section of the `app/features` directory
3. Create a `page.tsx` file in the new directory
4. Add any necessary components to the appropriate components directory
5. Update navigation components as needed

### Adding a New Component

1. Determine if the component is feature-specific or shared
2. For shared components:
   - Add to `app/components/common` or `app/components/layout`
3. For feature-specific components:
   - Add to the corresponding feature directory
4. Use TypeScript props interface
5. Follow the established component patterns
6. Test the component thoroughly

## Building for Production

To build the application for production:

```bash
npm run build
# or
yarn build
# or
pnpm build
```

## Deployment

The production environment is hosted on AWS. Contact the systems administrator for deployment credentials and procedures.

## Documentation

For more detailed documentation, refer to:

- [Frontend Architecture](../documentation/architecture/frontend_architecture.md)
- [Frontend Structure](../documentation/cleanup/frontend_structure.md)
- [Exercise Types](../documentation/development/exercise_types.md)
- [API Integration](../documentation/api/api_overview.md)
- [Troubleshooting](../documentation/troubleshooting/frontend_issues.md)
