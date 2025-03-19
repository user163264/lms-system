# Type Management Best Practices

## Current Implementation

The Spotvogel LMS currently has multiple definitions of the `Exercise` type:

1. In `/frontend/app/context/ExerciseContext.tsx` - Used for API interactions and state management
2. In `/frontend/app/components/exercises/ExerciseRenderer.tsx` - Used for rendering exercises

This duplication creates type incompatibility issues requiring adapter functions to bridge the differences:

```typescript
const adaptExerciseForRenderer = (exercise: Exercise): RendererExercise => {
  return {
    ...exercise,
    // Ensure correct_answer is always an array, never undefined
    correct_answer: exercise.correct_answer || [],
  } as RendererExercise;
};
```

## Recommended Improvement

### Single Source of Truth for Types

The best practice is to maintain a single source of truth for all shared types, especially core entities like `Exercise`:

1. Create a dedicated types directory:
   ```
   /frontend/app/types/
   ```

2. Define shared types in appropriate files:
   ```
   /frontend/app/types/exercise.ts
   ```

3. Export and import types from this central location:
   ```typescript
   // In types/exercise.ts
   export interface Exercise {
     // Unified definition with clear documentation on requirements
   }
   
   // In components and services
   import { Exercise } from '../../types/exercise';
   ```

### Implementation Effort

**Work required:**
- Medium effort (approximately 1-2 hours)
- Changes to 3-5 files
- Updates to import statements where Exercise is used

**Impact on API calls:**
- No change to the actual API calling implementation
- The centralized API service pattern remains unchanged
- Only type definitions would be consolidated

**Safety considerations:**
- TypeScript compilation will catch most incompatibilities
- Requires careful testing to ensure all components receive the necessary fields
- Could be implemented as a separate refactoring task
- Consider adding documentation comments to the type definition to clarify requirements

## Phased Approach

1. **Short-term:** Continue with the current adapter approach for immediate stability
2. **Medium-term:** Create the consolidated type definitions
3. **Long-term:** Remove adapters and update all components to use the shared types

## Benefits

- Reduces maintenance complexity
- Ensures consistency across the application
- Makes future changes to the Exercise structure more manageable
- Improves developer experience with clearer type expectations
- Eliminates the need for type conversion logic 