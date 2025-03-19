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
  
  console.log('Initial positions recorded');
  
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
    
    // Check if any visible button has moved
    const movedButtons = initialPositions.filter((initialPos) => {
      const currentPos = currentPositions.find(p => p.text === initialPos.text);
      if (!currentPos) return false; // This button is no longer visible
      
      const hasMoved = 
        Math.abs(initialPos.left - currentPos.left) > 1 || 
        Math.abs(initialPos.top - currentPos.top) > 1;
      
      return hasMoved;
    });
    
    if (movedButtons.length > 0) {
      console.error('JITTER DETECTED! Some buttons moved from their original positions.');
      movedButtons.forEach(button => {
        console.error(`Button "${button.text}" moved from its original position.`);
      });
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
      
      // Try clicking a slot to place the word
      const slots = document.querySelectorAll('.test-case-1 [class*="min-w-[80px]"]');
      if (slots.length > 0) {
        console.log('Clicking first slot...');
        slots[0].click();
        
        // Wait again and verify positions
        setTimeout(() => {
          verifyPositions();
          console.log('Test complete');
        }, 500);
      } else {
        console.log('No slots found to click');
        console.log('Test complete');
      }
    }, 500);
  }
}, 1000); 