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
        
        // New Top Interface Edit Story Button
        const editStoryBtn = document.getElementById('editStoryBtn');
        if (editStoryBtn) {
            editStoryBtn.addEventListener('click', function() {
                // Just scroll to the story content section
                const storyContent = document.getElementById('storyContent');
                if (storyContent) {
                    storyContent.scrollIntoView({ behavior: 'smooth' });
                    storyContent.focus();
                }
            });
        }
        
        // New Top Interface Close Button
        const topCloseBtn = document.getElementById('closeBtn');
        if (topCloseBtn) {
            topCloseBtn.addEventListener('click', function() {
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
        
        // Process Copilot Request Function - Unified for both interfaces
        function processCopilotRequest(prompt, buttonElement, isTopInterface = false) {
            if (prompt === '') {
                alert('Please enter a prompt for the Co-Pilot');
                return;
            }
            
            // Store original button content
            const originalButtonHtml = buttonElement.innerHTML;
            
            // Disable button and show loading state
            buttonElement.disabled = true;
            buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            
            // Call Co-Pilot API
            fetch('{{ url_for("sustainability_copilot.api_query") }}', {
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
                buttonElement.disabled = false;
                buttonElement.innerHTML = originalButtonHtml;
                
                if (data.success) {
                    if (isTopInterface) {
                        // Update the conversation text in the top interface
                        updateCopilotConversation(data.response);
                    } else {
                        // Display response in the panel
                        showCopilotResponse(data.response);
                    }
                } else {
                    const errorMessage = data.error || 'Unknown error occurred while processing your request';
                    if (isTopInterface) {
                        // Show error in the conversation area
                        updateCopilotConversation("Error: " + errorMessage);
                    } else {
                        showCopilotError(errorMessage);
                    }
                }
            })
            .catch(error => {
                console.error('Error calling Co-Pilot:', error);
                buttonElement.disabled = false;
                buttonElement.innerHTML = originalButtonHtml;
                
                const errorMessage = 'Error calling Co-Pilot. Please try again.';
                if (isTopInterface) {
                    updateCopilotConversation("Error: " + errorMessage);
                } else {
                    alert(errorMessage);
                }
            });
        }
        
        // Function to update the conversation in the top interface
        function updateCopilotConversation(text) {
            const conversationElement = document.querySelector('.copilot-conversation');
            if (conversationElement) {
                conversationElement.textContent = text;
                conversationElement.scrollIntoView({ behavior: 'smooth' });
            }
        }
        
        // Top Interface Ask Copilot Button
        const topAskCopilotBtn = document.getElementById('askCopilotBtn');
        const topCopilotPrompt = document.getElementById('copilotPrompt');
        
        if (topAskCopilotBtn && topCopilotPrompt) {
            topAskCopilotBtn.addEventListener('click', function() {
                const prompt = topCopilotPrompt.value.trim();
                processCopilotRequest(prompt, topAskCopilotBtn, true);
            });
            
            // Also handle enter key in the textarea
            topCopilotPrompt.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    const prompt = topCopilotPrompt.value.trim();
                    processCopilotRequest(prompt, topAskCopilotBtn, true);
                }
            });
        }
        
        // Panel Copilot functionality
        const askCopilotBtnPanel = document.getElementById('askCopilotBtnPanel');
        const copilotPromptPanel = document.getElementById('copilotPromptPanel');
        
        if (askCopilotBtnPanel && copilotPromptPanel) {
            askCopilotBtnPanel.addEventListener('click', function() {
                const prompt = copilotPromptPanel.value.trim();
                processCopilotRequest(prompt, askCopilotBtnPanel, false);
            });
            
            // Also handle enter key in the textarea
            copilotPromptPanel.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    const prompt = copilotPromptPanel.value.trim();
                    processCopilotRequest(prompt, askCopilotBtnPanel, false);
                }
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
                    if (copilotPromptPanel) {
                        copilotPromptPanel.value = '';
                    }
                    
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