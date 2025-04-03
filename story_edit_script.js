<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Story Details button
        const storyDetailsBtn = document.getElementById('storyDetailsBtn');
        if (storyDetailsBtn) {
            storyDetailsBtn.addEventListener('click', function() {
                window.location.href = "{{ url_for('stories.view_story', story_id=story.id) if story else '#' }}";
            });
        }
        
        // Close Edit button
        const closeEditBtn = document.getElementById('closeEditBtn');
        if (closeEditBtn) {
            closeEditBtn.addEventListener('click', function() {
                window.location.href = "{{ url_for('stories.view_story', story_id=story.id) if story else url_for('stories.stories_home') }}";
            });
        }
        
        // Co-Pilot button
        const copilotBtn = document.getElementById('copilotBtn');
        const copilotContainer = document.getElementById('copilotContainer');
        const closeCopilotBtn = document.getElementById('closeCopilotBtn');
        
        if (copilotBtn && copilotContainer) {
            copilotBtn.addEventListener('click', function() {
                copilotContainer.style.display = copilotContainer.style.display === 'none' ? 'block' : 'none';
            });
        }
        
        if (closeCopilotBtn && copilotContainer) {
            closeCopilotBtn.addEventListener('click', function() {
                copilotContainer.style.display = 'none';
            });
        }
        
        // Handle form submission
        const form = document.getElementById('storyEditForm');
        const errorElement = document.getElementById('storyEditError');
        
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Hide any previous errors
                if (errorElement) {
                    errorElement.classList.add('d-none');
                }
                
                // Disable submit button to prevent double submission
                const saveBtn = document.getElementById('saveStoryBtn');
                if (saveBtn) {
                    saveBtn.disabled = true;
                    saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';
                }
                
                // Get form data
                const formData = {
                    title: document.getElementById('storyTitle').value,
                    audience: document.getElementById('storyAudience').value,
                    category: document.getElementById('storyCategory').value,
                    content: document.getElementById('storyContent').value,
                    recommendations: document.getElementById('storyRecommendations').value.split('\n').filter(r => r.trim() !== '')
                };
                
                // Send AJAX request
                fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Redirect to story detail page
                        window.location.href = "{{ url_for('stories.view_story', story_id=story.id) if story else url_for('stories.stories_home') }}";
                    } else {
                        showError(data.error || 'An error occurred while saving the story');
                    }
                })
                .catch(error => {
                    showError('Network error: ' + error.message);
                    if (saveBtn) {
                        saveBtn.disabled = false;
                        saveBtn.innerHTML = '<i class="fas fa-save me-2"></i> Save Changes';
                    }
                });
            });
        }
        
        // Copilot functionality
        const askCopilotBtn = document.getElementById('askCopilotBtn');
        const copilotPrompt = document.getElementById('copilotPrompt');
        
        if (askCopilotBtn && copilotPrompt) {
            askCopilotBtn.addEventListener('click', function() {
                const prompt = copilotPrompt.value.trim();
                
                if (prompt === '') {
                    alert('Please enter a prompt for the Co-Pilot');
                    return;
                }
                
                // Disable button and show loading state
                askCopilotBtn.disabled = true;
                askCopilotBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
                
                // Call Co-Pilot API
                fetch('{{ url_for("storytelling.api_copilot_assist") }}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        story_id: '{{ story.id if story else "" }}',
                        context: 'story_edit'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    // Re-enable button
                    askCopilotBtn.disabled = false;
                    askCopilotBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i> Ask Co-Pilot';
                    
                    if (data.success) {
                        // Display response in a properly styled response panel
                        showCopilotResponse(data.response);
                    } else {
                        showCopilotError(data.error || 'Unknown error occurred while processing your request');
                    }
                })
                .catch(error => {
                    console.error('Error calling Co-Pilot:', error);
                    alert('Error calling Co-Pilot. Please try again.');
                    askCopilotBtn.disabled = false;
                    askCopilotBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i> Ask Co-Pilot';
                });
            });
        }
        
        function showError(message) {
            if (errorElement) {
                errorElement.textContent = message;
                errorElement.classList.remove('d-none');
            } else {
                alert(message);
            }
            
            const saveBtn = document.getElementById('saveStoryBtn');
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fas fa-save me-2"></i> Save Changes';
            }
        }
        
        // Copilot response handlers
        const responseContainer = document.getElementById('copilotResponseContainer');
        const responseContent = document.getElementById('copilotResponseContent');
        const applyToStoryBtn = document.getElementById('applyToStoryBtn');
        const dismissResponseBtn = document.getElementById('dismissResponseBtn');
        const errorContainer = document.getElementById('copilotErrorContainer');
        const errorContent = document.getElementById('copilotErrorContent');
        const dismissErrorBtn = document.getElementById('dismissErrorBtn');
        
        // Function to display Copilot response
        function showCopilotResponse(response) {
            // Hide error container if visible
            if (errorContainer) {
                errorContainer.style.display = 'none';
            }
            
            // Set response content and show container
            if (responseContent && responseContainer) {
                responseContent.textContent = response;
                responseContainer.style.display = 'block';
                
                // Scroll to response container
                responseContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
        
        // Function to display Copilot error
        function showCopilotError(error) {
            // Hide response container if visible
            if (responseContainer) {
                responseContainer.style.display = 'none';
            }
            
            // Set error content and show container
            if (errorContent && errorContainer) {
                errorContent.textContent = error;
                errorContainer.style.display = 'block';
                
                // Scroll to error container
                errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
        
        // Apply suggestion to story content
        if (applyToStoryBtn) {
            applyToStoryBtn.addEventListener('click', function() {
                const suggestion = responseContent.textContent;
                const storyContent = document.getElementById('storyContent');
                
                if (suggestion && storyContent) {
                    // Append the suggestion to the story content
                    storyContent.value += '\n\n' + suggestion;
                    
                    // Hide response container
                    responseContainer.style.display = 'none';
                    
                    // Clear prompt input
                    document.getElementById('copilotPrompt').value = '';
                    
                    // Show success message
                    alert('Suggestion applied to your story!');
                }
            });
        }
        
        // Dismiss response
        if (dismissResponseBtn) {
            dismissResponseBtn.addEventListener('click', function() {
                responseContainer.style.display = 'none';
            });
        }
        
        // Dismiss error
        if (dismissErrorBtn) {
            dismissErrorBtn.addEventListener('click', function() {
                errorContainer.style.display = 'none';
            });
        }
    });
</script>
