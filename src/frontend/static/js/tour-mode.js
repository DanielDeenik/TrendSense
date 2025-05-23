/**
 * TourMode - AI-Guided UX Using Chain of Thought
 *
 * This component provides an AI-guided tour experience using Chain of Thought (CoT)
 * reasoning instead of static prompts. It makes the tour feel more intuitive,
 * AI-native, and contextual rather than scripted.
 */

class TourMode {
    constructor() {
        this.tourActive = false;
        this.currentStep = 0;
        this.tourSteps = [];
        this.cotTooltipContainer = null;
        this.highlightOverlay = null;
        this.tourConfig = null;
        this.typingSpeed = 30; // ms per character
        this.typingTimer = null;
        this.initialized = false;
        this.toggleButton = null;
    }

    /**
     * Check if the tour is currently active
     * @returns {boolean} Whether the tour is active
     */
    isActive() {
        return this.tourActive;
    }

    /**
     * Initialize the TourMode system
     */
    init() {
        if (this.initialized) return;

        // Create CoT tooltip container
        this.cotTooltipContainer = document.createElement('div');
        this.cotTooltipContainer.id = 'copilot-cot-tooltip';
        this.cotTooltipContainer.className = 'fixed bottom-6 right-6 bg-gray-900 text-sm shadow-xl rounded-xl px-4 py-3 w-96 z-50 hidden';
        document.body.appendChild(this.cotTooltipContainer);

        // Create highlight overlay
        this.highlightOverlay = document.createElement('div');
        this.highlightOverlay.className = 'fixed inset-0 pointer-events-none z-40 hidden';
        document.body.appendChild(this.highlightOverlay);

        // Add tour controls
        this.createTourControls();

        // Load tour configuration
        this.loadTourConfig();

        // Store reference to toggle button
        this.toggleButton = document.getElementById('toggle-tour-btn');

        // Check URL parameters for tour activation
        this.checkUrlForTourActivation();

        // Check user completion status
        this.checkUserCompletionStatus();

        this.initialized = true;
    }

    /**
     * Check URL parameters for tour activation
     */
    checkUrlForTourActivation() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('tour') === 'true') {
            // Start tour if URL parameter is present
            setTimeout(() => this.startTour(), 500); // Small delay to ensure DOM is ready
        }
    }

    /**
     * Check if user has completed the tour
     */
    checkUserCompletionStatus() {
        // Try to get completion status from Firebase if user is authenticated
        if (window.firebase && window.firebase.auth().currentUser) {
            this.getFirebaseCompletionStatus();
        } else {
            // Fallback to localStorage for non-authenticated users
            this.getLocalStorageCompletionStatus();
        }
    }

    /**
     * Get tour completion status from Firebase
     */
    getFirebaseCompletionStatus() {
        const userId = window.firebase.auth().currentUser.uid;
        window.firebase.database().ref(`users/${userId}/tourCompleted`).once('value')
            .then(snapshot => {
                const completed = snapshot.val();
                if (completed) {
                    this.handleTourCompleted();
                }
            })
            .catch(error => {
                console.error('Error getting tour completion status from Firebase:', error);
                // Fallback to localStorage
                this.getLocalStorageCompletionStatus();
            });
    }

    /**
     * Get tour completion status from localStorage
     */
    getLocalStorageCompletionStatus() {
        const completed = localStorage.getItem('tourCompleted') === 'true';
        if (completed) {
            this.handleTourCompleted();
        }
    }

    /**
     * Handle tour completed state
     */
    handleTourCompleted() {
        // Hide toggle button if tour is completed
        if (this.toggleButton && !this.isManuallyEnabled()) {
            this.toggleButton.classList.add('hidden');
        }
    }

    /**
     * Check if tour was manually enabled
     */
    isManuallyEnabled() {
        return localStorage.getItem('tourManuallyEnabled') === 'true';
    }

    /**
     * Create tour control buttons
     */
    createTourControls() {
        const tourControls = document.createElement('div');
        tourControls.id = 'tour-controls';
        tourControls.className = 'fixed bottom-6 left-6 flex space-x-2 z-50 hidden';

        tourControls.innerHTML = `
            <button id="tour-prev" class="bg-gray-800 hover:bg-gray-700 text-white px-3 py-1.5 rounded-lg text-sm flex items-center">
                <i class="fas fa-chevron-left mr-1"></i> Previous
            </button>
            <button id="tour-next" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-sm flex items-center">
                Next <i class="fas fa-chevron-right ml-1"></i>
            </button>
            <button id="tour-exit" class="bg-gray-800 hover:bg-gray-700 text-white px-3 py-1.5 rounded-lg text-sm flex items-center ml-2">
                <i class="fas fa-times mr-1"></i> Exit Tour
            </button>
        `;

        document.body.appendChild(tourControls);

        // Add event listeners
        document.getElementById('tour-prev').addEventListener('click', () => this.prevStep());
        document.getElementById('tour-next').addEventListener('click', () => this.nextStep());
        document.getElementById('tour-exit').addEventListener('click', () => this.endTour());
    }

    /**
     * Load tour configuration based on current page
     */
    loadTourConfig() {
        // Determine current page
        const path = window.location.pathname;

        // Load appropriate tour config
        if (path.includes('/vc-lens')) {
            this.tourConfig = tourConfigs.vcLens;
        } else if (path.includes('/trendradar')) {
            this.tourConfig = tourConfigs.trendRadar;
        } else if (path.includes('/graph-analytics')) {
            this.tourConfig = tourConfigs.graphAnalytics;
        } else if (path.includes('/strategy')) {
            this.tourConfig = tourConfigs.strategy;
        } else {
            this.tourConfig = tourConfigs.default;
        }
    }

    /**
     * Start the tour
     */
    startTour() {
        if (!this.initialized) this.init();
        if (this.tourActive) return;

        this.tourActive = true;
        this.currentStep = 0;
        this.tourSteps = this.tourConfig.steps;

        // Show tour controls
        document.getElementById('tour-controls').classList.remove('hidden');

        // Show tour navigation if it exists
        const tourNav = document.querySelector('.tour-navigation');
        if (tourNav) {
            tourNav.classList.remove('hidden');
        }

        // Update toggle button appearance
        if (this.toggleButton) {
            this.toggleButton.classList.remove('bg-blue-600', 'hover:bg-blue-700');
            this.toggleButton.classList.add('bg-green-600', 'hover:bg-green-700');
            this.toggleButton.querySelector('span').textContent = 'Exit AI Tour';
        }

        // Initialize help components
        if (typeof loadHelpComponents === 'function') {
            loadHelpComponents();
        }

        // Start first step
        this.showStep(this.currentStep);
    }

    /**
     * End the tour
     */
    endTour(completed = false) {
        this.tourActive = false;
        this.currentStep = 0;

        // Hide tour controls
        document.getElementById('tour-controls').classList.add('hidden');

        // Hide CoT tooltip
        this.cotTooltipContainer.classList.add('hidden');

        // Hide highlight overlay
        this.highlightOverlay.classList.add('hidden');

        // Hide tour navigation if it exists
        const tourNav = document.querySelector('.tour-navigation');
        if (tourNav) {
            tourNav.classList.add('hidden');
        }

        // Update toggle button appearance
        if (this.toggleButton) {
            this.toggleButton.classList.remove('bg-green-600', 'hover:bg-green-700');
            this.toggleButton.classList.add('bg-blue-600', 'hover:bg-blue-700');
            this.toggleButton.querySelector('span').textContent = 'AI-Guided Tour';
        }

        // Store completion status if tour was completed
        if (completed) {
            this.storeTourCompletionStatus();
        }

        // Clear any typing timer
        if (this.typingTimer) clearInterval(this.typingTimer);
    }

    /**
     * Store tour completion status
     */
    storeTourCompletionStatus() {
        // Store in Firebase if user is authenticated
        if (window.firebase && window.firebase.auth().currentUser) {
            const userId = window.firebase.auth().currentUser.uid;
            window.firebase.database().ref(`users/${userId}/tourCompleted`).set(true)
                .catch(error => {
                    console.error('Error storing tour completion status in Firebase:', error);
                    // Fallback to localStorage
                    localStorage.setItem('tourCompleted', 'true');
                });
        } else {
            // Fallback to localStorage for non-authenticated users
            localStorage.setItem('tourCompleted', 'true');
        }

        // Hide toggle button unless manually enabled
        if (this.toggleButton && !this.isManuallyEnabled()) {
            this.toggleButton.classList.add('hidden');
        }
    }

    /**
     * Show a specific tour step
     */
    showStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= this.tourSteps.length) return;

        const step = this.tourSteps[stepIndex];

        // Update CoT tooltip with thinking
        this.showCoTThinking(step.thinking);

        // Highlight element if specified
        if (step.highlightSelector) {
            this.highlightElement(step.highlightSelector);
        } else {
            this.highlightOverlay.classList.add('hidden');
        }

        // Execute any actions
        if (step.actions) {
            this.executeActions(step.actions);
        }

        // Update button states
        document.getElementById('tour-prev').disabled = stepIndex === 0;
        document.getElementById('tour-next').disabled = stepIndex === this.tourSteps.length - 1;
        document.getElementById('tour-next').textContent = stepIndex === this.tourSteps.length - 1 ? 'Finish' : 'Next';
    }

    /**
     * Show Chain of Thought thinking with typewriter effect
     */
    showCoTThinking(thinking) {
        // Clear any existing typing timer
        if (this.typingTimer) clearInterval(this.typingTimer);

        // Show the tooltip container
        this.cotTooltipContainer.classList.remove('hidden');
        this.cotTooltipContainer.innerHTML = '<p class="text-gray-300 italic">🧠 ""</p>';

        // Get the paragraph element
        const paragraph = this.cotTooltipContainer.querySelector('p');

        // Set up typewriter effect
        let charIndex = 0;
        const text = thinking;

        this.typingTimer = setInterval(() => {
            if (charIndex < text.length) {
                // Update the text with the next character
                paragraph.innerHTML = `🧠 "${text.substring(0, charIndex + 1)}"`;
                charIndex++;
            } else {
                // Clear the interval when done
                clearInterval(this.typingTimer);
                this.typingTimer = null;
            }
        }, this.typingSpeed);
    }

    /**
     * Highlight a specific element
     */
    highlightElement(selector) {
        const element = document.querySelector(selector);
        if (!element) {
            this.highlightOverlay.classList.add('hidden');
            return;
        }

        const rect = element.getBoundingClientRect();

        // Show highlight overlay
        this.highlightOverlay.classList.remove('hidden');
        this.highlightOverlay.innerHTML = `
            <div class="absolute bg-black bg-opacity-60 inset-0"></div>
            <div class="absolute border-2 border-blue-500 rounded-lg" style="
                top: ${rect.top + window.scrollY}px;
                left: ${rect.left + window.scrollX}px;
                width: ${rect.width}px;
                height: ${rect.height}px;
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.6);
            "></div>
        `;
    }

    /**
     * Execute actions for a step
     */
    executeActions(actions) {
        actions.forEach(action => {
            switch (action.type) {
                case 'click':
                    const clickElement = document.querySelector(action.selector);
                    if (clickElement) clickElement.click();
                    break;
                case 'filter':
                    // Handle filter actions
                    if (action.filterType && action.value) {
                        this.applyFilter(action.filterType, action.value);
                    }
                    break;
                case 'zoom':
                    // Handle zoom actions
                    if (action.target) {
                        this.zoomToElement(action.target);
                    }
                    break;
                case 'display':
                    // Handle display actions
                    if (action.component) {
                        this.displayComponent(action.component);
                    }
                    break;
            }
        });
    }

    /**
     * Apply a filter
     */
    applyFilter(filterType, value) {
        // Implementation depends on the specific filters in your application
        console.log(`Applying filter: ${filterType} = ${value}`);

        // Example implementation
        const filterSelect = document.querySelector(`select[data-filter="${filterType}"]`);
        if (filterSelect) {
            filterSelect.value = value;
            filterSelect.dispatchEvent(new Event('change'));
        }
    }

    /**
     * Zoom to an element
     */
    zoomToElement(target) {
        // Implementation depends on your visualization library
        console.log(`Zooming to: ${target}`);

        // Example implementation for graph visualization
        if (window.graphInstance && typeof window.graphInstance.zoomToNode === 'function') {
            window.graphInstance.zoomToNode(target);
        }
    }

    /**
     * Display a component
     */
    displayComponent(component) {
        // Implementation depends on your application's components
        console.log(`Displaying component: ${component}`);

        // Example implementation
        const componentElement = document.querySelector(`#${component}`);
        if (componentElement) {
            componentElement.classList.remove('hidden');
        }
    }

    /**
     * Go to the next step
     */
    nextStep() {
        if (this.currentStep < this.tourSteps.length - 1) {
            this.currentStep++;
            this.showStep(this.currentStep);
        } else {
            // End tour and mark as completed when reaching the last step
            this.endTour(true);
        }
    }

    /**
     * Go to the previous step
     */
    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showStep(this.currentStep);
        }
    }
}

// Create global instance
const tourMode = new TourMode();

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    tourMode.init();
});

// Export for global access
window.tourMode = tourMode;
