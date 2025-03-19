# Frontend Directory Structure Reorganization Plan

## Current Issues
- Multiple test/example directories that should be consolidated
- Inconsistent component naming conventions
- Lack of clear separation between features, shared components, and layouts
- Duplicated exercise component implementations

## Proposed Structure

```
lms/frontend/
├── app/                          # Next.js app directory
│   ├── components/               # Shared components
│   │   ├── common/               # Truly shared UI components (buttons, inputs, etc.)
│   │   ├── layout/               # Layout components (headers, footers, etc.)
│   │   └── exercises/            # Exercise components (consolidated)
│   │       ├── base/             # Base exercise components
│   │       └── types/            # Exercise type implementations
│   ├── features/                 # Feature-based directories
│   │   ├── auth/                 # Authentication feature
│   │   ├── courses/              # Course management feature
│   │   ├── dashboard/            # Dashboard feature
│   │   ├── exercises/            # Exercise feature pages
│   │   └── lessons/              # Lesson feature pages
│   ├── api/                      # API route handlers
│   ├── context/                  # React context providers
│   ├── services/                 # API service functions
│   ├── utils/                    # Utility functions
│   └── tests/                    # Test pages (consolidated)
├── public/                       # Static assets
├── utils/                        # Utility functions (move to app/utils)
└── src/                          # Source code (migrate to app directory)
```

## Implementation Steps

1. Create the new directory structure
2. Consolidate duplicate exercise components
3. Move test/example pages to a dedicated test directory
4. Standardize component naming conventions
5. Update imports across the codebase

## Component Naming Conventions

- Use PascalCase for all component files
- Use meaningful, descriptive names
- Suffix test components with "Test"
- Avoid duplicative naming (e.g., both "WordScramble.tsx" and "WordScrambleExercise.tsx") 