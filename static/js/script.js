// Flash message close functionality
document.addEventListener('DOMContentLoaded', function() {
    // Close flash messages
    const closeButtons = document.querySelectorAll('.flash-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.opacity = '0';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });
    
    // Auto-close flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Note summarization
    const summarizeButtons = document.querySelectorAll('.summarize-btn');
    summarizeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const noteId = this.dataset.noteId;
            const summaryElement = document.getElementById(`summary-${noteId}`);
            
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Summarizing...';
            
            fetch(`/notes/${noteId}/summarize`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        summaryElement.innerHTML = `<p class="error">Error: ${data.error}</p>`;
                    } else {
                        summaryElement.innerHTML = `<h4>Summary</h4><p>${data.summary}</p>`;
                    }
                    this.disabled = false;
                    this.innerHTML = '<i class="fas fa-file-alt"></i> Summarize';
                })
                .catch(error => {
                    summaryElement.innerHTML = `<p class="error">Error: ${error.message}</p>`;
                    this.disabled = false;
                    this.innerHTML = '<i class="fas fa-file-alt"></i> Summarize';
                });
        });
    });
    
    // Tag input functionality
    const tagInputs = document.querySelectorAll('.tag-input');
    tagInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const value = this.value.trim();
                if (value) {
                    addTag(value, this);
                    this.value = '';
                }
            }
        });
        
        input.addEventListener('blur', function() {
            const value = this.value.trim();
            if (value) {
                addTag(value, this);
                this.value = '';
            }
        });
    });
    
    function addTag(value, input) {
        const tagsContainer = input.previousElementSibling;
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerHTML = `${value} <button type="button" class="tag-remove">&times;</button>`;
        
        const removeBtn = tag.querySelector('.tag-remove');
        removeBtn.addEventListener('click', function() {
            tag.remove();
            updateHiddenInput(tagsContainer);
        });
        
        tagsContainer.appendChild(tag);
        updateHiddenInput(tagsContainer);
    }
    
    function updateHiddenInput(tagsContainer) {
        const hiddenInput = tagsContainer.nextElementSibling;
        const tags = Array.from(tagsContainer.querySelectorAll('.tag'))
            .map(tag => tag.textContent.replace('×', '').trim());
        hiddenInput.value = tags.join(',');
    }
    
    // Initialize existing tags
    document.querySelectorAll('.tags-container .tag').forEach(tag => {
        const removeBtn = tag.querySelector('.tag-remove');
        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                tag.remove();
                const tagsContainer = tag.parentElement;
                updateHiddenInput(tagsContainer);
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
  const toggleBtn = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const body = document.body;

  // Load saved theme
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    body.classList.add(savedTheme);
    themeIcon.className = savedTheme === 'dark-mode' ? 'fas fa-sun' : 'fas fa-moon';
  } else {
    body.classList.add('light-mode');
  }

  toggleBtn.addEventListener('click', function() {
    if (body.classList.contains('light-mode')) {
      body.classList.remove('light-mode');
      body.classList.add('dark-mode');
      themeIcon.className = 'fas fa-sun';
      localStorage.setItem('theme', 'dark-mode');
    } else {
      body.classList.remove('dark-mode');
      body.classList.add('light-mode');
      themeIcon.className = 'fas fa-moon';
      localStorage.setItem('theme', 'light-mode');
    }
  });
});