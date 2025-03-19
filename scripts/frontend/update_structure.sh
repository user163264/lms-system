#!/bin/bash

# Frontend Structure Update Script
# This script helps update the frontend to follow the new directory structure

FRONTEND_DIR="$(pwd)/lms/frontend"

# Check if we're in the right directory
if [ ! -d "$FRONTEND_DIR" ]; then
  echo "Error: Cannot find frontend directory at $FRONTEND_DIR"
  echo "Please run this script from the root of the LMS project"
  exit 1
fi

echo "=== Frontend Structure Update Script ==="
echo "This script will reorganize the frontend directory structure according to the cleanup plan."
echo ""
echo "The following changes will be made:"
echo "1. Create new directory structure"
echo "2. Move components to appropriate locations"
echo "3. Consolidate test directories"
echo "4. Update .gitignore for log files"
echo ""
read -p "Do you want to continue? (y/n): " CONTINUE

if [ "$CONTINUE" != "y" ]; then
  echo "Operation canceled"
  exit 0
fi

echo ""
echo "Step 1: Creating new directory structure..."

# Create directories if they don't exist
mkdir -p "$FRONTEND_DIR/app/components/common"
mkdir -p "$FRONTEND_DIR/app/components/layout"
mkdir -p "$FRONTEND_DIR/app/components/exercises/base"
mkdir -p "$FRONTEND_DIR/app/components/exercises/types"
mkdir -p "$FRONTEND_DIR/app/features/auth"
mkdir -p "$FRONTEND_DIR/app/features/courses"
mkdir -p "$FRONTEND_DIR/app/features/dashboard"
mkdir -p "$FRONTEND_DIR/app/features/exercises"
mkdir -p "$FRONTEND_DIR/app/features/lessons"
mkdir -p "$FRONTEND_DIR/app/context"
mkdir -p "$FRONTEND_DIR/app/services"
mkdir -p "$FRONTEND_DIR/app/utils"
mkdir -p "$FRONTEND_DIR/app/tests"

echo "Step 2: Moving components to appropriate locations..."

# Move NavBar to layout directory if it exists in components
if [ -f "$FRONTEND_DIR/app/components/NavBar.tsx" ]; then
  mv "$FRONTEND_DIR/app/components/NavBar.tsx" "$FRONTEND_DIR/app/components/layout/"
  echo "- Moved NavBar.tsx to app/components/layout/"
fi

# Move utils from root to app/utils
if [ -d "$FRONTEND_DIR/utils" ]; then
  for file in "$FRONTEND_DIR/utils/"*; do
    filename=$(basename "$file")
    # Convert .js files to .ts when moving
    if [[ "$filename" == *.js ]]; then
      ts_filename="${filename%.js}.ts"
      echo "- Converting $filename to TypeScript and moving to app/utils/$ts_filename"
      # Use cp instead of mv to preserve the original file for backwards compatibility
      cp "$file" "$FRONTEND_DIR/app/utils/$ts_filename"
    else
      echo "- Moving $filename to app/utils/"
      cp "$file" "$FRONTEND_DIR/app/utils/"
    fi
  done
fi

# Create ExerciseTypes.ts if it doesn't exist
if [ ! -f "$FRONTEND_DIR/app/components/exercises/ExerciseTypes.ts" ]; then
  echo "- Creating ExerciseTypes.ts template"
  cat > "$FRONTEND_DIR/app/components/exercises/ExerciseTypes.ts" << 'EOL'
/**
 * Exercise Types and Interfaces
 * 
 * This file contains type definitions for all exercise components
 */

export enum ExerciseType {
  MULTIPLE_CHOICE = 'multiple_choice',
  TRUE_FALSE = 'true_false',
  SHORT_ANSWER = 'short_answer',
  LONG_ANSWER = 'long_answer',
  FILL_BLANKS = 'fill_blanks',
  CLOZE_TEST = 'cloze_test',
  IMAGE_LABELING = 'image_labeling',
  MATCHING_WORDS = 'matching_words',
  SENTENCE_REORDERING = 'sentence_reordering',
  WORD_SCRAMBLE = 'word_scramble'
}

export interface BaseExerciseProps {
  id: string;
  type: ExerciseType;
  question: string;
  instructions?: string;
  feedback?: string;
  isSubmitted?: boolean;
  isCorrect?: boolean;
  onSubmit?: (answer: any) => void;
  onReset?: () => void;
}

// Add your exercise type interfaces here
EOL
fi

echo "Step 3: Consolidating test directories..."

# Find all test and showcase directories
find "$FRONTEND_DIR/app" -maxdepth 1 -type d \( -name "*test*" -o -name "*showcase*" -o -name "*debug*" \) | while read test_dir; do
  if [ "$(basename "$test_dir")" != "tests" ]; then
    dir_name=$(basename "$test_dir")
    target_dir="$FRONTEND_DIR/app/tests/$dir_name"
    
    # Create target directory if needed
    mkdir -p "$target_dir"
    
    # Move contents to tests directory
    echo "- Moving $dir_name to app/tests/$dir_name"
    cp -r "$test_dir"/* "$target_dir"/ 2>/dev/null || true
  fi
done

# Create test index page if it doesn't exist
if [ ! -f "$FRONTEND_DIR/app/tests/page.tsx" ]; then
  echo "- Creating tests index page"
  echo "import TestsIndex from './index';" > "$FRONTEND_DIR/app/tests/page.tsx"
  echo "export default TestsIndex;" >> "$FRONTEND_DIR/app/tests/page.tsx"
fi

# Update .gitignore
echo "Step 4: Updating .gitignore for log files..."
if [ -f "$FRONTEND_DIR/.gitignore" ]; then
  if ! grep -q "# local logs" "$FRONTEND_DIR/.gitignore"; then
    echo "" >> "$FRONTEND_DIR/.gitignore"
    echo "# local logs" >> "$FRONTEND_DIR/.gitignore"
    echo "*.log" >> "$FRONTEND_DIR/.gitignore"
    echo "server.log" >> "$FRONTEND_DIR/.gitignore"
    echo "dev.log" >> "$FRONTEND_DIR/.gitignore"
    echo "frontend.log" >> "$FRONTEND_DIR/.gitignore"
    echo "/.next/error.log" >> "$FRONTEND_DIR/.gitignore"
    echo "- Updated .gitignore with log file patterns"
  else
    echo "- .gitignore already contains log file patterns"
  fi
fi

# Remove next.config.ts if it exists (redundant file)
if [ -f "$FRONTEND_DIR/next.config.ts" ]; then
  echo "Step 5: Removing redundant next.config.ts file..."
  rm "$FRONTEND_DIR/next.config.ts"
  echo "- Removed redundant next.config.ts file"
fi

echo ""
echo "=== Update Complete ==="
echo ""
echo "The frontend structure has been updated. Next steps:"
echo "1. Review the changes and verify everything works as expected"
echo "2. Update import paths in your components to reference the new locations"
echo "3. Continue migrating components following the new structure"
echo ""
echo "For more details, see the documentation in:"
echo "lms/documentation/cleanup/frontend_structure.md"
echo "lms/documentation/cleanup/frontend_cleanup_summary.md" 