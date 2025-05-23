/**
 * Generative UI functionality for TrendSense
 *
 * This file contains functions for handling generative UI buttons and interactions
 */

// Initialize generative UI components
document.addEventListener('DOMContentLoaded', function() {
    initGenerativeButtons();
    setupGenerativeActions();
});

/**
 * Initialize generative UI buttons
 */
function initGenerativeButtons() {
    // Find all generative UI buttons
    const generativeButtons = document.querySelectorAll('.generative-ui-btn');
    console.log(`Generative UI: Found ${generativeButtons.length} generative buttons`);

    if (generativeButtons.length === 0) {
        console.warn('Generative UI: No generative buttons found. This might indicate a navigation structure issue.');
    }

    generativeButtons.forEach(button => {
        // Make sure the button has the necessary attributes
        const action = button.getAttribute('data-action');
        const target = button.getAttribute('data-target');

        if (!action || !target) {
            console.warn('Generative UI: Button missing required attributes', button);
            return;
        }

        // Remove any existing event listeners (to prevent duplicates)
        button.removeEventListener('click', handleGenerativeButtonClick);

        // Add click event listener
        button.addEventListener('click', handleGenerativeButtonClick);
    });
}

/**
 * Handle generative button click event
 *
 * @param {Event} e - The click event
 */
function handleGenerativeButtonClick(e) {
    e.preventDefault();

    const button = e.currentTarget;
    const action = button.getAttribute('data-action');
    const target = button.getAttribute('data-target');

    console.log(`Generative UI: Button clicked - ${action} for ${target}`);

    // Show a subtle feedback effect
    button.classList.add('bg-blue-900', 'bg-opacity-20');
    setTimeout(() => {
        button.classList.remove('bg-blue-900', 'bg-opacity-20');
    }, 300);

    // Handle the generative action
    handleGenerativeAction(action, target);
}

/**
 * Handle generative UI actions
 *
 * @param {string} action - The action to perform
 * @param {string} target - The target element or data
 */
function handleGenerativeAction(action, target) {
    console.log(`Handling generative action: ${action} for target: ${target}`);

    switch(action) {
        case 'generate-trend':
            generateTrend(target);
            break;
        case 'generate-insights':
            generateInsights(target);
            break;
        case 'generate-report':
            generateReport(target);
            break;
        case 'generate-visualization':
            generateVisualization(target);
            break;
        case 'generate-strategy':
            generateStrategy(target);
            break;
        default:
            console.warn(`Unknown generative action: ${action}`);
    }
}

/**
 * Generate trend analysis
 *
 * @param {string} target - The target data or category
 */
function generateTrend(target) {
    // Show loading indicator
    showGenerativeLoading('Generating trend analysis...');

    // Simulate API call
    setTimeout(() => {
        // Hide loading indicator
        hideGenerativeLoading();

        // Show results
        showGenerativeResults('trend', {
            title: 'Generated Trend Analysis',
            description: `AI-generated trend analysis for ${target}`,
            data: {
                score: 85,
                momentum: 'Rising',
                confidence: 'High',
                sources: ['Social Media', 'News', 'Academic Papers']
            }
        });
    }, 1500);
}

/**
 * Call an API endpoint for generative content
 *
 * @param {string} endpoint - The API endpoint to call
 * @param {object} data - The data to send to the API
 * @param {string} loadingMessage - The loading message to display
 * @param {function} successCallback - The callback to call on success
 * @returns {Promise} - The fetch promise
 */
function callGenerativeApi(endpoint, data, loadingMessage, successCallback) {
    // Show loading indicator
    showGenerativeLoading(loadingMessage);

    // Track the API call for debugging
    const apiCallInfo = {
        endpoint,
        requestData: data,
        timestamp: new Date().toISOString()
    };

    // Call the API
    return fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Hide loading indicator
        hideGenerativeLoading();

        // Call success callback
        successCallback(data);

        // Track successful API response
        apiCallInfo.success = true;
        apiCallInfo.responseData = data;

        // Log successful API call for debugging
        if (window.tourErrorLog) {
            window.tourErrorLog.unshift({
                type: 'api_success',
                ...apiCallInfo,
                timestamp: new Date().toISOString()
            });
        }
    })
    .catch(error => {
        console.error(`Error calling ${endpoint}:`, error);
        hideGenerativeLoading();

        // Track API error
        apiCallInfo.success = false;
        apiCallInfo.error = error.message;

        // Log error for debugging
        if (window.tourErrorLog) {
            window.tourErrorLog.unshift({
                type: 'api_error',
                ...apiCallInfo,
                timestamp: new Date().toISOString()
            });
        }

        // Show error message
        const errorMessage = `Failed to generate content: ${error.message}. Please try again.`;
        showGenerativeError(errorMessage, endpoint, data);
    });
}

/**
 * Generate insights
 *
 * @param {string} target - The target data or category
 */
function generateInsights(target) {
    callGenerativeApi(
        '/api/generate-insights',
        { target: target },
        'Generating insights...',
        (data) => {
            showGenerativeResults('insights', {
                title: 'Generated Insights',
                description: `AI-generated insights for ${target}`,
                insights: data.insights || []
            });
        }
    );
}

/**
 * Simulate an API call for generative content
 *
 * @param {string} type - The type of content to generate
 * @param {string} target - The target data or category
 * @param {string} loadingMessage - The loading message to display
 * @param {object} resultData - The data to return
 * @param {function} callback - Optional callback after completion
 */
function simulateGenerativeApi(type, target, loadingMessage, resultData, callback) {
    // Show loading indicator
    showGenerativeLoading(loadingMessage);

    // Simulate API call
    setTimeout(() => {
        // Hide loading indicator
        hideGenerativeLoading();

        // Show results
        showGenerativeResults(type, resultData);

        // Call callback if provided
        if (callback && typeof callback === 'function') {
            callback();
        }
    }, 1500 + Math.random() * 1000); // Random delay between 1.5-2.5 seconds
}

/**
 * Generate report
 *
 * @param {string} target - The target data or category
 */
function generateReport(target) {
    simulateGenerativeApi(
        'report',
        target,
        'Generating report...',
        {
            title: 'Generated Report',
            description: `AI-generated report for ${target}`,
            sections: [
                'Executive Summary',
                'Key Findings',
                'Recommendations',
                'Next Steps'
            ]
        }
    );
}

/**
 * Generate visualization
 *
 * @param {string} target - The target data or category
 */
function generateVisualization(target) {
    simulateGenerativeApi(
        'visualization',
        target,
        'Generating visualization...',
        {
            title: 'Generated Visualization',
            description: `AI-generated visualization for ${target}`,
            type: 'radar-chart'
        }
    );
}

/**
 * Generate strategy
 *
 * @param {string} target - The target data or category
 */
function generateStrategy(target) {
    simulateGenerativeApi(
        'strategy',
        target,
        'Generating strategy...',
        {
            title: 'Generated Strategy',
            description: `AI-generated strategy for ${target}`,
            components: [
                'Market Entry',
                'Competitive Analysis',
                'Risk Assessment',
                'Implementation Plan'
            ]
        }
    );
}

/**
 * Show generative loading indicator
 *
 * @param {string} message - The loading message to display
 */
function showGenerativeLoading(message) {
    // Create loading indicator if it doesn't exist
    if (!document.getElementById('generative-loading')) {
        const loadingEl = document.createElement('div');
        loadingEl.id = 'generative-loading';
        loadingEl.className = 'fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50';
        loadingEl.innerHTML = `
            <div class="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 shadow-lg">
                <div class="flex items-center justify-center mb-4">
                    <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
                </div>
                <p id="generative-loading-message" class="text-center text-white"></p>
            </div>
        `;
        document.body.appendChild(loadingEl);
    }

    // Update loading message
    document.getElementById('generative-loading-message').textContent = message || 'Loading...';

    // Show loading indicator
    document.getElementById('generative-loading').classList.remove('hidden');
}

/**
 * Hide generative loading indicator
 */
function hideGenerativeLoading() {
    const loadingEl = document.getElementById('generative-loading');
    if (loadingEl) {
        loadingEl.classList.add('hidden');
    }
}

/**
 * Show generative results
 *
 * @param {string} type - The type of results
 * @param {object} data - The results data
 */
function showGenerativeResults(type, data) {
    // Implementation depends on the specific UI requirements
    console.log('Generated results:', type, data);

    if (type === 'insights') {
        // Create a more detailed modal for insights
        let insightsHtml = '';

        if (Array.isArray(data.insights)) {
            // Format insights as a list with details
            insightsHtml += `<p class="mb-4">${data.description}</p>`;

            data.insights.forEach((insight, index) => {
                insightsHtml += `
                    <div class="mb-4 p-3 bg-gray-700 rounded-lg">
                        <h4 class="font-bold text-blue-400">${index + 1}. ${insight.headline || 'Insight'}</h4>
                        <p class="mt-2">${insight.description || insight.text || ''}</p>
                        ${insight.implications ? `
                            <div class="mt-2">
                                <span class="text-xs font-semibold text-gray-400">Implications:</span>
                                <p class="text-sm text-gray-300">${insight.implications}</p>
                            </div>
                        ` : ''}
                    </div>
                `;
            });
        } else {
            // If insights is not an array, display as simple text
            insightsHtml = `<p>${data.insights || 'No insights generated.'}</p>`;
        }

        showGenerativeModal(data.title, insightsHtml, true);
    } else {
        // For other types, use the default implementation
        showGenerativeModal(data.title, data.description);
    }
}

/**
 * Show generative modal
 *
 * @param {string} title - The modal title
 * @param {string} content - The modal content
 * @param {boolean} isHtml - Whether content is HTML
 * @param {object} options - Additional options for the modal
 */
function showGenerativeModal(title, content, isHtml = false, options = {}) {
    // Create modal if it doesn't exist
    if (!document.getElementById('generative-modal')) {
        const modalEl = document.createElement('div');
        modalEl.id = 'generative-modal';
        modalEl.className = 'fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50 hidden';
        modalEl.innerHTML = `
            <div class="bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4 shadow-lg max-h-[80vh] overflow-y-auto">
                <div class="flex justify-between items-center mb-4">
                    <h3 id="generative-modal-title" class="text-xl font-bold text-white"></h3>
                    <button id="generative-modal-close" class="text-gray-400 hover:text-white">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div id="generative-modal-content" class="text-white"></div>
                <div id="generative-modal-actions" class="flex justify-end mt-4">
                    <button id="generative-modal-close-btn" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg mr-2">
                        Close
                    </button>
                    <button id="generative-modal-action" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
                        View Details
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modalEl);

        // Add event listeners
        document.getElementById('generative-modal-close').addEventListener('click', function() {
            document.getElementById('generative-modal').classList.add('hidden');
        });

        document.getElementById('generative-modal-close-btn').addEventListener('click', function() {
            document.getElementById('generative-modal').classList.add('hidden');
        });

        document.getElementById('generative-modal-action').addEventListener('click', function() {
            document.getElementById('generative-modal').classList.add('hidden');
            // Navigate to appropriate page based on the current context
            // This would be implemented based on specific requirements

            // For now, just navigate to the trend radar page
            window.location.href = '/trendradar';
        });
    }

    // Update modal content
    document.getElementById('generative-modal-title').textContent = title;

    if (isHtml) {
        document.getElementById('generative-modal-content').innerHTML = content;
    } else {
        document.getElementById('generative-modal-content').textContent = content;
    }

    // Handle custom actions
    const actionsContainer = document.getElementById('generative-modal-actions');
    const defaultAction = document.getElementById('generative-modal-action');

    // Reset actions to default
    if (options.hideDefaultAction) {
        defaultAction.classList.add('hidden');
    } else {
        defaultAction.classList.remove('hidden');
        defaultAction.textContent = options.actionText || 'View Details';
    }

    // Add custom actions if provided
    if (options.customActions) {
        // Remove any previous custom actions
        const customActions = actionsContainer.querySelectorAll('.custom-action');
        customActions.forEach(btn => btn.remove());

        // Add new custom actions
        options.customActions.forEach(action => {
            const btn = document.createElement('button');
            btn.className = `custom-action ${action.className || 'bg-blue-600 hover:bg-blue-700 text-white'} px-4 py-2 rounded-lg ml-2`;
            btn.textContent = action.text;
            btn.addEventListener('click', action.onClick);
            actionsContainer.appendChild(btn);
        });
    }

    // Show modal
    document.getElementById('generative-modal').classList.remove('hidden');
}

/**
 * Show generative error with help integration
 *
 * @param {string} errorMessage - The error message to display
 * @param {string} endpoint - The API endpoint that failed
 * @param {object} requestData - The data sent to the API
 */
function showGenerativeError(errorMessage, endpoint, requestData) {
    // Create error content with details
    const errorContent = `
        <div class="bg-red-900 bg-opacity-30 p-3 rounded-lg mb-4">
            <p class="text-red-300">${errorMessage}</p>
        </div>
        <p class="text-sm text-gray-400 mb-2">This error occurred while trying to generate AI content.</p>
    `;

    // Prepare error data for logging
    const errorData = {
        message: errorMessage,
        endpoint: endpoint,
        requestData: requestData,
        timestamp: new Date().toISOString()
    };

    // Check if tour mode is active
    const isTourActive = window.tourMode && window.tourMode.isActive();

    // Create custom actions based on context
    const customActions = [
        {
            text: 'Get Help',
            className: 'bg-green-600 hover:bg-green-700 text-white',
            onClick: function() {
                // Hide the error modal
                document.getElementById('generative-modal').classList.add('hidden');

                // Log the issue with the help logger
                if (window.tourHelpLogger) {
                    window.tourHelpLogger.logIssue({
                        issueType: 'feature-access',
                        description: `Error generating AI content: ${errorMessage}`,
                        errorData: errorData
                    });
                }

                // Open the help modal
                if (typeof window.openHelpModal === 'function') {
                    window.openHelpModal();

                    // Pre-fill the form with error details
                    setTimeout(() => {
                        const issueTypeSelect = document.getElementById('issue-type');
                        const descriptionField = document.getElementById('issue-description');

                        if (issueTypeSelect) issueTypeSelect.value = 'feature-access';
                        if (descriptionField) descriptionField.value = `Error generating AI content: ${errorMessage}`;
                    }, 100);
                }
            }
        }
    ];

    // If tour mode is active, add option to highlight in tour
    if (isTourActive) {
        customActions.push({
            text: 'Highlight in Tour',
            className: 'bg-blue-600 hover:bg-blue-700 text-white',
            onClick: function() {
                // Hide the error modal
                document.getElementById('generative-modal').classList.add('hidden');

                // Highlight the error in the tour
                highlightErrorInTour(errorData);
            }
        });
    }

    // Show the error modal with custom actions
    showGenerativeModal(
        'Error Generating Content',
        errorContent,
        true,
        {
            hideDefaultAction: true,
            customActions: customActions
        }
    );

    // If tour mode is active, automatically highlight the error
    if (isTourActive) {
        highlightErrorInTour(errorData);
    }
}

/**
 * Highlight an error in the tour mode
 *
 * @param {object} errorData - Data about the error
 */
function highlightErrorInTour(errorData) {
    if (!window.tourMode || !window.tourMode.isActive()) return;

    // Check if we're already in the error handling tour
    if (window.tourMode.tourConfig && window.tourMode.tourConfig.name === "Error Handling") {
        // Already in error handling tour, just update the thinking
        const thinking = `
            I notice there's another error with the AI content generation.
            The system tried to call ${errorData.endpoint} but encountered an error: "${errorData.message}".
            This might be because the AI service is temporarily unavailable or there's an issue with the data format.
            Let me help you understand what's happening and how to resolve it.
        `;

        window.tourMode.showCoTThinking(thinking);
        return;
    }

    // Store the current tour state to return to later
    const previousTourConfig = window.tourMode.tourConfig;
    const previousStep = window.tourMode.currentStep;

    // Switch to the error handling tour
    window.tourMode.tourConfig = window.tourConfigs.errorHandling;
    window.tourMode.tourSteps = window.tourConfigs.errorHandling.steps;
    window.tourMode.currentStep = 0;

    // Customize the first step with specific error details
    const customizedThinking = `
        I notice there's an error with the AI content generation.
        The system tried to call ${errorData.endpoint} but encountered an error: "${errorData.message}".
        This might be because the AI service is temporarily unavailable or there's an issue with the data format.
        Let me help you understand what's happening and how to resolve it.
    `;

    window.tourMode.tourSteps[0].thinking = customizedThinking;

    // Find the generative UI button that triggered this action
    const generativeButton = document.querySelector('[data-generative-action="generate-insights"]');

    if (generativeButton) {
        // Highlight the button that caused the error
        window.tourMode.tourSteps[0].highlightSelector = '[data-generative-action="generate-insights"]';
    }

    // Show the first step of the error handling tour
    window.tourMode.showStep(0);

    // Add a custom event listener to return to the previous tour when done
    const tourNextButton = document.getElementById('tour-next');
    const originalNextHandler = tourNextButton.onclick;

    // Create a function to handle the "next" button click
    const handleErrorTourNext = function() {
        // If we're at the last step of the error tour
        if (window.tourMode.currentStep === window.tourMode.tourSteps.length - 1) {
            // Remove this custom handler
            tourNextButton.removeEventListener('click', handleErrorTourNext);

            // Restore the original handler
            tourNextButton.onclick = originalNextHandler;

            // Return to the previous tour if it exists
            if (previousTourConfig) {
                window.tourMode.tourConfig = previousTourConfig;
                window.tourMode.tourSteps = previousTourConfig.steps;
                window.tourMode.currentStep = previousStep;
                window.tourMode.showStep(previousStep);

                // Add a custom message about returning to the previous tour
                setTimeout(() => {
                    window.tourMode.showCoTThinking(
                        `Now that we've addressed the error, let's continue with the ${previousTourConfig.name} tour.`
                    );
                }, 500);
            }
        }
    };

    // Replace the next button handler
    tourNextButton.onclick = null;
    tourNextButton.addEventListener('click', handleErrorTourNext);
}

/**
 * Setup generative actions
 */
function setupGenerativeActions() {
    // Add event listeners for generative action buttons
    const actionButtons = document.querySelectorAll('[data-generative-action]');

    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.getAttribute('data-generative-action');
            const target = this.getAttribute('data-generative-target');

            handleGenerativeAction(action, target);
        });
    });
}
