// Test script for Word Scramble component jitter issue

console.log('Running Word Scramble jitter test');

// Wait for page to load
setTimeout(() => {
  // Select all word buttons in the first exercise
  const wordButtons = document.querySelectorAll('.test-case-1 button');
  
  console.log(`Found ${wordButtons.length} word buttons`);
  
  // Record initial positions
  const initialPositions = Array.from(wordButtons).map(button => {
    const rect = button.getBoundingClientRect();
    return {
      text: button.textContent.trim(),
      left: rect.left,
      top: rect.top
    };
  });
  
  console.log('Initial positions:', initialPositions);
  
  // Create a function to verify positions haven't changed
  const verifyPositions = () => {
    const currentPositions = Array.from(document.querySelectorAll('.test-case-1 button')).map(button => {
      const rect = button.getBoundingClientRect();
      return {
        text: button.textContent.trim(),
        left: rect.left,
        top: rect.top
      };
    });
    
    console.log('Current positions:', currentPositions);
    
    // Check if any visible button has moved
    const movedButtons = initialPositions.filter((initialPos, index) => {
      if (index >= currentPositions.length) return false;
      const currentPos = currentPositions.find(p => p.text === initialPos.text);
      if (!currentPos) return false;
      
      const hasMoved = 
        Math.abs(initialPos.left - currentPos.left) > 1 || 
        Math.abs(initialPos.top - currentPos.top) > 1;
      
      return hasMoved;
    });
    
    if (movedButtons.length > 0) {
      console.error('JITTER DETECTED! The following buttons moved:', movedButtons);
    } else {
      console.log('No jitter detected. All buttons maintained their positions.');
    }
  };
  
  // Click a button and check if other buttons maintain position
  if (wordButtons.length > 0) {
    console.log('Clicking first button...');
    wordButtons[0].click();
    
    // Wait a bit and verify positions
    setTimeout(() => {
      verifyPositions();
      console.log('Test complete');
    }, 500);
  }
}, 1000); 