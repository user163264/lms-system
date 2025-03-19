// Word Scramble Test Script

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Word Scramble Test Script Loaded');
  
  // Helper function to highlight elements
  function highlightElement(element, duration = 1500) {
    if (!element) return;
    
    const originalBackground = element.style.backgroundColor;
    const originalBorder = element.style.border;
    
    element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
    element.style.border = '2px solid #fbbf24';
    element.style.transition = 'all 0.3s ease';
    
    setTimeout(() => {
      element.style.backgroundColor = originalBackground;
      element.style.border = originalBorder;
    }, duration);
  }
  
  // Helper function to wait for a specified time
  function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // Function to test a specific Word Scramble exercise
  async function testExercise(exerciseIndex = 0) {
    try {
      // Select the exercise
      const exerciseButtons = document.querySelectorAll('[class*="bg-white border border-gray-300"], [class*="bg-blue-100"]');
      
      if (exerciseButtons.length > exerciseIndex) {
        console.log(`Testing exercise #${exerciseIndex + 1}`);
        exerciseButtons[exerciseIndex].click();
        highlightElement(exerciseButtons[exerciseIndex]);
        await wait(1000);
        
        // Check if instructions toggle exists and click it
        const instructionsToggle = document.querySelector('button[class*="text-sm"]');
        if (instructionsToggle) {
          console.log('Toggling instructions visibility');
          instructionsToggle.click();
          highlightElement(instructionsToggle);
          await wait(1500);
          
          // Toggle back after reading
          instructionsToggle.click();
          await wait(500);
        }
        
        // Get all words in the word bank
        const wordBankContainer = document.querySelector('[class*="word-bank"]');
        highlightElement(wordBankContainer);
        await wait(1000);
        
        const wordElements = wordBankContainer.querySelectorAll('[class*="word-item"]');
        
        // Test dragging some words to the answer area
        for (let i = 0; i < Math.min(5, wordElements.length); i++) {
          console.log(`Selecting word #${i + 1}`);
          wordElements[i].click();
          highlightElement(wordElements[i]);
          await wait(600);
        }
        
        // Try removing a word from the answer area
        const answerContainer = document.querySelector('[class*="answer-area"]');
        highlightElement(answerContainer);
        await wait(1000);
        
        const answerWords = answerContainer.querySelectorAll('[class*="word-item"]');
        if (answerWords.length > 0) {
          console.log('Removing a word from answer area');
          answerWords[0].click();
          await wait(600);
        }
        
        // Submit the answer (even if incomplete, for testing)
        const submitButton = document.querySelector('button[type="submit"], button.bg-blue-500');
        if (submitButton) {
          console.log('Submitting answer');
          highlightElement(submitButton);
          submitButton.click();
          await wait(1500);
        }
        
        return true;
      } else {
        console.error('Exercise button not found at index', exerciseIndex);
        return false;
      }
    } catch (error) {
      console.error('Error during test:', error);
      return false;
    }
  }
  
  // Run tests for each exercise with delay between
  async function runAllTests() {
    console.log('Starting automatic test of all exercises');
    
    const totalExercises = document.querySelectorAll('[class*="bg-white border border-gray-300"], [class*="bg-blue-100"]').length;
    
    for (let i = 0; i < totalExercises; i++) {
      const success = await testExercise(i);
      if (success) {
        console.log(`Exercise #${i + 1} test completed`);
      } else {
        console.log(`Exercise #${i + 1} test failed`);
      }
      await wait(2000); // Wait between exercises
    }
    
    console.log('All tests completed');
  }
  
  // Add a test control panel
  const controlPanel = document.createElement('div');
  controlPanel.className = 'fixed top-4 right-4 bg-white p-3 rounded-lg shadow-lg border border-gray-300 z-50';
  controlPanel.innerHTML = `
    <h3 class="font-medium mb-2">Test Controls</h3>
    <div class="flex flex-col gap-2">
      <button id="run-all-tests" class="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600">Run All Tests</button>
      <button id="test-exercise-0" class="px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600">Test Exercise 1</button>
      <button id="test-exercise-1" class="px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600">Test Exercise 2</button>
      <button id="test-exercise-2" class="px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600">Test Exercise 3</button>
      <button id="toggle-panel" class="px-3 py-1 bg-gray-200 text-gray-800 rounded text-sm hover:bg-gray-300 mt-2">Hide Panel</button>
    </div>
  `;
  document.body.appendChild(controlPanel);
  
  // Set up event listeners for test buttons
  document.getElementById('run-all-tests').addEventListener('click', runAllTests);
  document.getElementById('test-exercise-0').addEventListener('click', () => testExercise(0));
  document.getElementById('test-exercise-1').addEventListener('click', () => testExercise(1));
  document.getElementById('test-exercise-2').addEventListener('click', () => testExercise(2));
  
  // Toggle panel visibility
  const toggleButton = document.getElementById('toggle-panel');
  const panelContent = controlPanel.querySelector('div');
  
  toggleButton.addEventListener('click', function() {
    if (panelContent.style.display === 'none') {
      panelContent.style.display = 'flex';
      toggleButton.textContent = 'Hide Panel';
      toggleButton.className = 'px-3 py-1 bg-gray-200 text-gray-800 rounded text-sm hover:bg-gray-300 mt-2';
    } else {
      panelContent.style.display = 'none';
      toggleButton.textContent = 'Show Panel';
      toggleButton.className = 'px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600';
    }
  });
  
  console.log('Test controls added to page');
}); 