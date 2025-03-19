// Simple test script for Word Scramble component

console.log('Running Word Scramble jitter test - Version 3');

// Wait for page to fully load and stabilize
setTimeout(() => {
  try {
    console.log('Starting jitter test...');
    
    // Get all visible buttons in the word bank
    const wordButtons = document.querySelectorAll('.available-words button');
    console.log(`Found ${wordButtons.length} word buttons`);
    
    if (wordButtons.length === 0) {
      console.log('No word buttons found. Test cannot continue.');
      return;
    }
    
    // Record initial positions of all buttons
    const initialPositions = [];
    wordButtons.forEach(button => {
      const rect = button.getBoundingClientRect();
      initialPositions.push({
        text: button.textContent.trim(),
        left: Math.round(rect.left),
        top: Math.round(rect.top)
      });
    });
    console.log('Recorded initial positions of all buttons');
    
    // Function to check if positions have changed
    function checkPositions() {
      const currentButtons = document.querySelectorAll('.available-words button');
      console.log(`Currently found ${currentButtons.length} buttons`);
      
      let jitterDetected = false;
      
      // Check each initial button to see if it's still visible and if it moved
      initialPositions.forEach(initial => {
        // Find the matching button by text content
        for (let i = 0; i < currentButtons.length; i++) {
          const button = currentButtons[i];
          if (button.textContent.trim() === initial.text) {
            const rect = button.getBoundingClientRect();
            const current = {
              left: Math.round(rect.left),
              top: Math.round(rect.top)
            };
            
            // Check if position changed significantly
            if (Math.abs(current.left - initial.left) > 3 || 
                Math.abs(current.top - initial.top) > 3) {
              console.error(`JITTER: Button "${initial.text}" moved from (${initial.left},${initial.top}) to (${current.left},${current.top})`);
              jitterDetected = true;
            }
            break;
          }
        }
      });
      
      if (!jitterDetected) {
        console.log('No jitter detected - all visible buttons maintained their positions');
      }
    }
    
    // Click the first word button and check positions
    if (wordButtons.length > 0) {
      console.log(`Clicking first button (${wordButtons[0].textContent.trim()})...`);
      wordButtons[0].click();
      
      // Check positions after click
      setTimeout(() => {
        checkPositions();
        console.log('Test complete');
      }, 500);
    }
  } catch (error) {
    console.error('Error during test:', error.message);
  }
}, 2000); // Wait 2 seconds for page to stabilize 