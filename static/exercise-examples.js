document.addEventListener('DOMContentLoaded', function() {
    // Word Scramble and Sentence Reordering functionality
    setupDragAndDrop();
    
    // Multiple Choice, True/False
    setupRadioButtons();
    
    // Setup Cloze Test Word Bank
    setupWordBank();
    
    // Setup all submit buttons
    setupSubmitButtons();
});

// Function to setup drag and drop functionality
function setupDragAndDrop() {
    const dragAreas = document.querySelectorAll('.drag-area');
    const dropAreas = document.querySelectorAll('.drop-area');
    
    dragAreas.forEach((dragArea, idx) => {
        const dragItems = dragArea.querySelectorAll('.drag-item');
        const dropArea = dropAreas[Math.min(idx, dropAreas.length - 1)];
        
        dragItems.forEach(item => {
            item.draggable = true;
            
            item.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', this.textContent);
                this.classList.add('dragging');
            });
            
            item.addEventListener('dragend', function() {
                this.classList.remove('dragging');
            });
            
            // Allow clicking to move items as an alternative to drag-and-drop
            item.addEventListener('click', function() {
                const clone = this.cloneNode(true);
                setupDragItemListeners(clone);
                dropArea.appendChild(clone);
                this.style.opacity = '0.5';
                this.style.pointerEvents = 'none';
            });
        });
        
        if (dropArea) {
            dropArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('dragover');
            });
            
            dropArea.addEventListener('dragleave', function() {
                this.classList.remove('dragover');
            });
            
            dropArea.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
                
                const text = e.dataTransfer.getData('text/plain');
                const draggedItems = document.querySelectorAll('.drag-item');
                
                // Find the original item that was dragged
                let originalItem;
                draggedItems.forEach(item => {
                    if (item.textContent === text && item.classList.contains('dragging')) {
                        originalItem = item;
                    }
                });
                
                if (originalItem) {
                    const clone = originalItem.cloneNode(true);
                    setupDragItemListeners(clone);
                    this.appendChild(clone);
                    originalItem.style.opacity = '0.5';
                    originalItem.style.pointerEvents = 'none';
                }
            });
        }
    });
    
    // Helper function to set up listeners for cloned drag items
    function setupDragItemListeners(item) {
        item.addEventListener('click', function() {
            this.parentNode.removeChild(this);
            // Find and restore the original
            const originalText = this.textContent;
            const originals = document.querySelectorAll('.drag-item');
            
            originals.forEach(orig => {
                if (orig.textContent === originalText && orig.style.opacity === '0.5') {
                    orig.style.opacity = '1';
                    orig.style.pointerEvents = 'auto';
                    return;
                }
            });
        });
    }
}

// Function to handle radio button selections
function setupRadioButtons() {
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Find all radios in the same group
            const name = this.getAttribute('name');
            const group = document.querySelectorAll(`input[name="${name}"]`);
            
            // Add a visual indicator to the selected option
            group.forEach(btn => {
                const label = btn.nextElementSibling;
                if (btn.checked) {
                    label.style.fontWeight = 'bold';
                    label.style.color = '#2980b9';
                } else {
                    label.style.fontWeight = 'normal';
                    label.style.color = '#333';
                }
            });
        });
    });
}

// Function to setup word bank for cloze test
function setupWordBank() {
    const wordBank = document.querySelector('.word-bank');
    const blanks = document.querySelectorAll('.blank');
    
    if (!wordBank || !blanks.length) return;
    
    const bankWords = wordBank.querySelectorAll('.bank-word');
    
    bankWords.forEach(word => {
        word.draggable = true;
        
        word.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', this.textContent);
            this.classList.add('dragging');
        });
        
        word.addEventListener('dragend', function() {
            this.classList.remove('dragging');
        });
        
        // Click to place in first empty blank
        word.addEventListener('click', function() {
            for (let blank of blanks) {
                if (!blank.textContent.trim()) {
                    blank.textContent = this.textContent;
                    blank.dataset.word = this.textContent;
                    this.style.opacity = '0.5';
                    this.style.pointerEvents = 'none';
                    break;
                }
            }
        });
    });
    
    blanks.forEach(blank => {
        blank.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        blank.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });
        
        blank.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            const text = e.dataTransfer.getData('text/plain');
            this.textContent = text;
            this.dataset.word = text;
            
            // Find the original bank word and disable it
            const bankWords = document.querySelectorAll('.bank-word');
            bankWords.forEach(word => {
                if (word.textContent === text && word.classList.contains('dragging')) {
                    word.style.opacity = '0.5';
                    word.style.pointerEvents = 'none';
                }
            });
        });
        
        // Click to remove word and restore bank word
        blank.addEventListener('click', function() {
            if (this.textContent.trim()) {
                const word = this.dataset.word;
                const bankWords = document.querySelectorAll('.bank-word');
                
                bankWords.forEach(bankWord => {
                    if (bankWord.textContent === word && bankWord.style.opacity === '0.5') {
                        bankWord.style.opacity = '1';
                        bankWord.style.pointerEvents = 'auto';
                    }
                });
                
                this.textContent = '';
                this.dataset.word = '';
            }
        });
    });
}

// Function to handle submit button clicks
function setupSubmitButtons() {
    const submitButtons = document.querySelectorAll('button');
    
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Find the parent exercise container
            const container = this.closest('.exercise-container');
            if (!container) return;
            
            // Create feedback message
            const feedback = document.createElement('div');
            feedback.style.marginTop = '15px';
            feedback.style.padding = '10px';
            feedback.style.backgroundColor = '#e8f8f5';
            feedback.style.borderRadius = '4px';
            feedback.style.color = '#27ae60';
            feedback.style.fontWeight = 'bold';
            
            // Check if there's already a feedback message
            const existingFeedback = container.querySelector('.feedback-message');
            if (existingFeedback) {
                container.querySelector('.exercise-body').removeChild(existingFeedback);
            }
            
            feedback.textContent = 'Thank you for your answer! In a real implementation, this would be evaluated and feedback would be provided.';
            feedback.classList.add('feedback-message');
            
            container.querySelector('.exercise-body').appendChild(feedback);
            
            // Scroll to the feedback
            feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    });
} 