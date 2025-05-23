/**
 * Demo Mode Controller
 *
 * This module provides functionality for creating demo-ready videos of TrendSense.
 * It orchestrates a series of predefined actions to showcase features like the
 * guided tour and error handling.
 */

class DemoModeController {
    constructor() {
        this.isActive = false;
        this.currentScenario = null;
        this.scenarios = {};
        this.steps = [];
        this.currentStepIndex = 0;
        this.autoplayEnabled = false;
        this.autoplayDelay = 3000; // Default delay between steps (ms)
        this.autoplayTimer = null;
        this.controlPanel = null;
        this.initialized = false;
        this.eventListeners = {};
        this.recordingIndicator = null;
    }

    /**
     * Initialize the demo mode controller
     */
    init() {
        if (this.initialized) return;

        // Define demo scenarios
        this.defineScenarios();

        // Create control panel
        this.createControlPanel();

        // Create recording indicator
        this.createRecordingIndicator();

        // Check URL parameters for demo activation
        this.checkUrlForDemoActivation();

        this.initialized = true;
        console.log('Demo Mode Controller initialized');
    }

    /**
     * Define available demo scenarios
     */
    defineScenarios() {
        // Check if demo config is available
        if (window.demoConfig && window.demoConfig.scenarios) {
            // Load scenarios from config
            Object.keys(window.demoConfig.scenarios).forEach(key => {
                const configScenario = window.demoConfig.scenarios[key];

                // Create scenario with steps and actions
                this.scenarios[key] = {
                    name: configScenario.name,
                    description: configScenario.description,
                    steps: configScenario.steps.map(step => {
                        return {
                            name: step.name,
                            description: step.description,
                            delay: step.delay,
                            action: this.getActionForStep(key, step.name)
                        };
                    })
                };

                // Set autoplay settings if specified
                if (configScenario.autoplay) {
                    this.autoplayEnabled = configScenario.autoplay;
                }

                if (configScenario.autoplayDelay) {
                    this.autoplayDelay = configScenario.autoplayDelay;
                }
            });

            console.log('Loaded scenarios from config:', Object.keys(this.scenarios));
        } else {
            // Fallback to default scenarios
            this.defineDefaultScenarios();
            console.log('Using default scenarios');
        }
    }

    /**
     * Define default scenarios (fallback if config is not available)
     */
    defineDefaultScenarios() {
        // Error Handling Demo Scenario
        this.scenarios.errorHandling = {
            name: 'Error Handling Demo',
            description: 'Demonstrates how the guided tour handles API errors',
            steps: [
                {
                    name: 'Start Tour',
                    action: () => {
                        // Start the tour if not already active
                        if (window.tourMode && !window.tourMode.isActive()) {
                            window.tourMode.startTour();
                        }
                    },
                    delay: 2000
                },
                {
                    name: 'Navigate to TrendRadar',
                    action: () => {
                        // Navigate to TrendRadar if not already there
                        if (!window.location.pathname.includes('/trendradar')) {
                            window.location.href = '/trendradar/?tour=true';
                        }
                    },
                    delay: 2000
                },
                {
                    name: 'Trigger API Error',
                    action: () => {
                        // Simulate an API error by calling a non-existent endpoint
                        fetch('/api/non-existent-endpoint', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ target: 'market' })
                        })
                        .catch(error => {
                            console.log('Simulated API error:', error);
                            // Manually trigger error handling
                            if (typeof showGenerativeError === 'function') {
                                showGenerativeError(
                                    'Failed to connect to API: Network error',
                                    '/api/non-existent-endpoint',
                                    { target: 'market' }
                                );
                            }
                        });
                    },
                    delay: 3000
                },
                {
                    name: 'End Demo',
                    action: () => {
                        // End the tour
                        if (window.tourMode && window.tourMode.isActive()) {
                            window.tourMode.endTour();
                        }
                        // Show completion message
                        this.showNotification('Demo completed successfully!');
                    },
                    delay: 0
                }
            ]
        };
    }

    /**
     * Get action function for a step
     */
    getActionForStep(scenarioKey, stepName) {
        // Define actions for each step in each scenario
        const actions = {
            errorHandling: {
                'Start Tour': () => {
                    // Start the tour if not already active
                    if (window.tourMode && !window.tourMode.isActive()) {
                        window.tourMode.startTour();
                    }
                },
                'Navigate to TrendRadar': () => {
                    // Navigate to TrendRadar if not already there
                    if (!window.location.pathname.includes('/trendradar')) {
                        window.location.href = '/trendradar/?tour=true';
                    }
                },
                'Trigger API Error': () => {
                    // Simulate an API error by calling a non-existent endpoint
                    fetch('/api/non-existent-endpoint', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ target: 'market' })
                    })
                    .catch(error => {
                        console.log('Simulated API error:', error);
                        // Manually trigger error handling
                        if (typeof showGenerativeError === 'function') {
                            showGenerativeError(
                                'Failed to connect to API: Network error',
                                '/api/non-existent-endpoint',
                                { target: 'market' }
                            );
                        }
                    });
                },
                'Wait for Error Tour': () => {
                    // Wait for the error handling tour to appear
                    // This is just a delay step
                },
                'Navigate Through Error Tour': () => {
                    // Click the "Next" button to advance through the error tour
                    const nextButton = document.getElementById('tour-next');
                    if (nextButton) {
                        nextButton.click();
                    }
                },
                'Continue Error Tour': () => {
                    // Click the "Next" button again
                    const nextButton = document.getElementById('tour-next');
                    if (nextButton) {
                        nextButton.click();
                    }
                },
                'Open Help Modal': () => {
                    // Open the help modal
                    const helpButton = document.getElementById('tour-help-button');
                    if (helpButton) {
                        helpButton.click();
                    }
                },
                'Ask Co-Pilot': () => {
                    // Click the "Ask Co-Pilot" button
                    const askCopilotButton = document.getElementById('ask-copilot');
                    if (askCopilotButton) {
                        askCopilotButton.click();
                    }
                },
                'Close Help Modal': () => {
                    // Close the help modal
                    const cancelButton = document.getElementById('cancel-help');
                    if (cancelButton) {
                        cancelButton.click();
                    }
                },
                'End Demo': () => {
                    // End the tour
                    if (window.tourMode && window.tourMode.isActive()) {
                        window.tourMode.endTour();
                    }
                    // Show completion message
                    this.showNotification('Demo completed successfully!');
                }
            },
            guidedTour: {
                'Start Tour': () => {
                    // Start the tour if not already active
                    if (window.tourMode && !window.tourMode.isActive()) {
                        window.tourMode.startTour();
                    }
                },
                'Explore Dashboard': () => {
                    // Highlight dashboard elements
                    const dashboardElement = document.querySelector('.dashboard-container');
                    if (dashboardElement) {
                        dashboardElement.classList.add('highlight-pulse');
                        setTimeout(() => {
                            dashboardElement.classList.remove('highlight-pulse');
                        }, 2000);
                    }
                },
                'View Trends': () => {
                    // Click on a trend if available
                    const trendElement = document.querySelector('.trend-item');
                    if (trendElement) {
                        trendElement.click();
                    }
                },
                'End Demo': () => {
                    // End the tour
                    if (window.tourMode && window.tourMode.isActive()) {
                        window.tourMode.endTour();
                    }
                    // Show completion message
                    this.showNotification('Demo completed successfully!');
                }
            }
        };

        // Return the action function for this step
        return actions[scenarioKey] && actions[scenarioKey][stepName]
            ? actions[scenarioKey][stepName]
            : () => console.log(`No action defined for ${scenarioKey}.${stepName}`);
    }

    /**
     * Check URL parameters for demo activation
     */
    checkUrlForDemoActivation() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('demo') === 'true') {
            // Get scenario from URL if specified
            const scenarioName = urlParams.get('scenario') || 'errorHandling';

            // Start demo with specified scenario
            if (this.scenarios[scenarioName]) {
                this.startDemo(scenarioName);

                // Enable autoplay if specified
                if (urlParams.get('autoplay') === 'true') {
                    this.toggleAutoplay(true);
                }

                // Set custom delay if specified
                const delay = urlParams.get('delay');
                if (delay && !isNaN(parseInt(delay))) {
                    this.autoplayDelay = parseInt(delay);
                }
            }
        }
    }

    /**
     * Create demo mode control panel
     */
    createControlPanel() {
        // Create control panel element
        this.controlPanel = document.createElement('div');
        this.controlPanel.id = 'demo-control-panel';
        this.controlPanel.className = 'fixed bottom-6 right-6 bg-gray-800 rounded-lg p-4 shadow-lg z-50 hidden';

        // Create control panel content
        let scenarioOptions = '';
        Object.keys(this.scenarios).forEach(key => {
            scenarioOptions += `<option value="${key}">${this.scenarios[key].name}</option>`;
        });

        this.controlPanel.innerHTML = `
            <div class="flex items-center justify-between mb-3">
                <h3 class="text-white font-bold">Demo Mode</h3>
                <button id="demo-close" class="text-gray-400 hover:text-white">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="mb-3">
                <label class="block text-gray-300 text-sm mb-1">Scenario</label>
                <select id="demo-scenario" class="w-full bg-gray-700 text-white rounded px-2 py-1">
                    ${scenarioOptions}
                </select>
            </div>
            <div class="mb-3">
                <label class="block text-gray-300 text-sm mb-1">Autoplay Delay (ms)</label>
                <input type="number" id="demo-delay" class="w-full bg-gray-700 text-white rounded px-2 py-1" value="${this.autoplayDelay}">
            </div>
            <div class="flex items-center mb-3">
                <input type="checkbox" id="demo-autoplay" class="mr-2">
                <label for="demo-autoplay" class="text-gray-300 text-sm">Autoplay</label>
            </div>
            <div class="flex space-x-2">
                <button id="demo-start" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded">Start</button>
                <button id="demo-next" class="bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded" disabled>Next</button>
                <button id="demo-stop" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded" disabled>Stop</button>
            </div>
            <div class="mt-3">
                <div class="text-gray-300 text-sm mb-1">Current Step: <span id="demo-current-step">-</span></div>
                <div class="w-full bg-gray-700 rounded h-2 mt-1">
                    <div id="demo-progress" class="bg-blue-600 h-2 rounded" style="width: 0%"></div>
                </div>
            </div>
        `;

        // Add to document
        document.body.appendChild(this.controlPanel);

        // Add event listeners
        document.getElementById('demo-close').addEventListener('click', () => {
            this.toggleControlPanel(false);
        });

        document.getElementById('demo-start').addEventListener('click', () => {
            const scenarioName = document.getElementById('demo-scenario').value;
            this.startDemo(scenarioName);
        });

        document.getElementById('demo-next').addEventListener('click', () => {
            this.nextStep();
        });

        document.getElementById('demo-stop').addEventListener('click', () => {
            this.stopDemo();
        });

        document.getElementById('demo-autoplay').addEventListener('change', (e) => {
            this.toggleAutoplay(e.target.checked);
        });

        document.getElementById('demo-delay').addEventListener('change', (e) => {
            const delay = parseInt(e.target.value);
            if (!isNaN(delay) && delay > 0) {
                this.autoplayDelay = delay;
            }
        });
    }

    /**
     * Create recording indicator
     */
    createRecordingIndicator() {
        this.recordingIndicator = document.createElement('div');
        this.recordingIndicator.id = 'recording-indicator';
        this.recordingIndicator.className = 'fixed top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full flex items-center shadow-lg z-50 hidden';
        this.recordingIndicator.innerHTML = `
            <div class="w-3 h-3 bg-white rounded-full mr-2 animate-pulse"></div>
            <span>REC</span>
        `;

        document.body.appendChild(this.recordingIndicator);
    }

    /**
     * Toggle control panel visibility
     */
    toggleControlPanel(show) {
        if (show) {
            this.controlPanel.classList.remove('hidden');
        } else {
            this.controlPanel.classList.add('hidden');
        }
    }

    /**
     * Toggle recording indicator
     */
    toggleRecordingIndicator(show) {
        if (show) {
            this.recordingIndicator.classList.remove('hidden');
        } else {
            this.recordingIndicator.classList.add('hidden');
        }
    }

    /**
     * Start demo with specified scenario
     */
    startDemo(scenarioName) {
        if (!this.scenarios[scenarioName]) {
            console.error(`Scenario "${scenarioName}" not found`);
            return;
        }

        // Stop any running demo
        this.stopDemo();

        // Set current scenario
        this.currentScenario = scenarioName;
        this.steps = this.scenarios[scenarioName].steps;
        this.currentStepIndex = 0;
        this.isActive = true;

        // Update UI
        document.getElementById('demo-start').disabled = true;
        document.getElementById('demo-next').disabled = false;
        document.getElementById('demo-stop').disabled = false;
        document.getElementById('demo-current-step').textContent = this.steps[0].name;
        document.getElementById('demo-progress').style.width = '0%';

        // Show recording indicator
        this.toggleRecordingIndicator(true);

        // Execute first step
        this.executeCurrentStep();

        // Start autoplay if enabled
        if (this.autoplayEnabled) {
            this.scheduleNextStep();
        }

        console.log(`Started demo scenario: ${this.scenarios[scenarioName].name}`);
    }

    /**
     * Stop the current demo
     */
    stopDemo() {
        // Clear any scheduled steps
        if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
            this.autoplayTimer = null;
        }

        // Reset state
        this.isActive = false;
        this.currentScenario = null;
        this.steps = [];
        this.currentStepIndex = 0;

        // Update UI
        document.getElementById('demo-start').disabled = false;
        document.getElementById('demo-next').disabled = true;
        document.getElementById('demo-stop').disabled = true;
        document.getElementById('demo-current-step').textContent = '-';
        document.getElementById('demo-progress').style.width = '0%';

        // Hide recording indicator
        this.toggleRecordingIndicator(false);

        console.log('Demo stopped');
    }

    /**
     * Execute the current step
     */
    executeCurrentStep() {
        if (!this.isActive || this.currentStepIndex >= this.steps.length) {
            return;
        }

        const step = this.steps[this.currentStepIndex];

        // Update UI
        document.getElementById('demo-current-step').textContent = step.name;
        const progress = ((this.currentStepIndex) / (this.steps.length - 1)) * 100;
        document.getElementById('demo-progress').style.width = `${progress}%`;

        // Execute step action
        if (typeof step.action === 'function') {
            step.action();
        }

        console.log(`Executed step: ${step.name}`);
    }

    /**
     * Move to the next step
     */
    nextStep() {
        // Clear any scheduled steps
        if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
            this.autoplayTimer = null;
        }

        // Move to next step
        this.currentStepIndex++;

        // Check if demo is complete
        if (this.currentStepIndex >= this.steps.length) {
            console.log('Demo completed');
            this.stopDemo();
            return;
        }

        // Execute next step
        this.executeCurrentStep();

        // Schedule next step if autoplay is enabled
        if (this.autoplayEnabled) {
            this.scheduleNextStep();
        }
    }

    /**
     * Schedule the next step
     */
    scheduleNextStep() {
        if (!this.isActive || this.currentStepIndex >= this.steps.length - 1) {
            return;
        }

        const step = this.steps[this.currentStepIndex];
        const delay = step.delay || this.autoplayDelay;

        this.autoplayTimer = setTimeout(() => {
            this.nextStep();
        }, delay);
    }

    /**
     * Toggle autoplay
     */
    toggleAutoplay(enabled) {
        this.autoplayEnabled = enabled;
        document.getElementById('demo-autoplay').checked = enabled;

        // Update UI
        if (enabled && this.isActive) {
            this.scheduleNextStep();
        } else if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
            this.autoplayTimer = null;
        }
    }

    /**
     * Show notification
     */
    showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'demo-notification';
        notification.textContent = message;

        // Add to document
        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Create global instance
const demoMode = new DemoModeController();

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    demoMode.init();
});

// Export for global access
window.demoMode = demoMode;
