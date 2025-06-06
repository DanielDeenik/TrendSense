/**
 * LensIQ Copilot JavaScript Module
 * 
 * This module provides the frontend functionality for the AI Copilot,
 * including context tracking, UI interaction monitoring, and API communication.
 * 
 * Integrated from standalone agent.js with improvements for the main application.
 */

class LensIQCopilot {
    constructor() {
        this.version = '1.0.0';
        this.contextEvent = 'lensiq-copilot-context';
        this.initialized = false;
        this.mutationObserver = null;
        this.elements = {
            input: null,
            submit: null,
            response: null,
            thinking: null,
            content: null,
            visualization: null,
            chart: null
        };
    }

    /**
     * Initialize the copilot system
     */
    init() {
        if (this.initialized) return;

        console.info(`[LensIQ Copilot v${this.version}] Initializing...`);

        // Initialize DOM elements
        this.initElements();

        // Set up event listeners
        this.setupEventListeners();

        // Initialize context tracking
        this.initContextTracking();

        this.initialized = true;
        console.info(`[LensIQ Copilot v${this.version}] Initialized successfully.`);
    }

    /**
     * Initialize DOM element references
     */
    initElements() {
        this.elements = {
            input: document.getElementById('copilot-input'),
            submit: document.getElementById('copilot-submit'),
            response: document.getElementById('copilot-response'),
            thinking: document.getElementById('response-thinking'),
            content: document.getElementById('response-content'),
            visualization: document.getElementById('response-visualization'),
            chart: document.getElementById('response-chart')
        };
    }

    /**
     * Set up event listeners for copilot interactions
     */
    setupEventListeners() {
        // Submit button click handler
        if (this.elements.submit) {
            this.elements.submit.addEventListener('click', () => this.submitQuery());
        }

        // Enter key handler for input
        if (this.elements.input) {
            this.elements.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.submitQuery();
                }
            });
        }

        // Example queries click handlers
        const exampleQueries = document.querySelectorAll('#copilot-examples .bg-gray-700');
        exampleQueries.forEach(query => {
            query.addEventListener('click', () => {
                const queryText = query.querySelector('p')?.textContent;
                if (queryText && this.elements.input) {
                    this.elements.input.value = queryText;
                    this.submitQuery();
                }
            });
        });
    }

    /**
     * Initialize context tracking and mutation observation
     */
    initContextTracking() {
        this.setupMutationObserver();
    }

    /**
     * Get all visible UI elements with semantic meaning
     */
    getVisibleUIElements() {
        const elements = [];
        const selectors = [
            'button', 'input', 'select', 'textarea', 'a', 
            '[role="button"]', '[role="tab"]', '[role="checkbox"]', 
            '[role="menuitem"]', '[data-ai-label]'
        ];

        document.querySelectorAll(selectors.join(','))
            .forEach(el => {
                if (!el.offsetParent) return; // skip hidden elements
                
                const label = el.getAttribute('data-ai-label') || 
                             el.innerText || 
                             el.value || 
                             el.placeholder || 
                             el.getAttribute('aria-label') || '';
                
                elements.push({
                    tag: el.tagName.toLowerCase(),
                    label: label.trim(),
                    id: el.id || null,
                    classes: el.className || null,
                    rect: el.getBoundingClientRect(),
                    attributes: Array.from(el.attributes).reduce((acc, attr) => {
                        acc[attr.name] = attr.value;
                        return acc;
                    }, {})
                });
            });

        return elements;
    }

    /**
     * Take a context snapshot of the current page state
     */
    getContextSnapshot() {
        return {
            url: window.location.href,
            title: document.title,
            timestamp: new Date().toISOString(),
            elements: this.getVisibleUIElements(),
            copilotVersion: this.version
        };
    }

    /**
     * Set up mutation observer to track UI changes
     */
    setupMutationObserver() {
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
        }

        this.mutationObserver = new MutationObserver((mutations) => {
            const context = this.getContextSnapshot();
            const event = new CustomEvent(this.contextEvent, { detail: context });
            window.dispatchEvent(event);
        });

        this.mutationObserver.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true
        });
    }

    /**
     * Send context data to backend
     */
    async sendContextToBackend(endpoint, extraData = {}) {
        const payload = { ...this.getContextSnapshot(), ...extraData };
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            return await response.json();
        } catch (error) {
            console.error('Failed to send context to backend:', error);
            throw error;
        }
    }

    /**
     * Submit a query to the copilot
     */
    async submitQuery() {
        const query = this.elements.input?.value?.trim();
        if (!query) return;

        try {
            // Show loading state
            this.showLoadingState();

            // Send query to backend
            const response = await fetch('/copilot/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    query: query,
                    context: this.getContextSnapshot()
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.displayResponse(data);

        } catch (error) {
            console.error('Error submitting query:', error);
            this.displayError(error.message);
        }
    }

    /**
     * Show loading state in the UI
     */
    showLoadingState() {
        if (this.elements.response) {
            this.elements.response.classList.remove('hidden');
        }
        if (this.elements.thinking) {
            this.elements.thinking.textContent = 'Thinking...';
        }
        if (this.elements.content) {
            this.elements.content.textContent = 'Processing your query...';
        }
        if (this.elements.visualization) {
            this.elements.visualization.classList.add('hidden');
        }
    }

    /**
     * Display the copilot response
     */
    displayResponse(data) {
        if (this.elements.thinking && data.thinking) {
            this.elements.thinking.textContent = data.thinking;
        }
        if (this.elements.content && data.response) {
            this.elements.content.textContent = data.response;
        }

        // Handle visualization if present
        if (data.chart_type && this.elements.visualization) {
            this.elements.visualization.classList.remove('hidden');
            this.renderChart(data.chart_type, data);
        }
    }

    /**
     * Display an error message
     */
    displayError(message) {
        if (this.elements.response) {
            this.elements.response.classList.remove('hidden');
        }
        if (this.elements.thinking) {
            this.elements.thinking.textContent = 'Error occurred';
        }
        if (this.elements.content) {
            this.elements.content.textContent = `Sorry, I encountered an error: ${message}`;
        }
    }

    /**
     * Render a chart based on the response data
     */
    renderChart(chartType, data) {
        // This would integrate with Chart.js or other visualization library
        // Implementation depends on the specific chart requirements
        console.log(`Rendering ${chartType} chart with data:`, data);
        
        // Placeholder implementation
        if (this.elements.chart) {
            this.elements.chart.innerHTML = `
                <div class="text-center p-4">
                    <i class="fas fa-chart-${chartType === 'radar' ? 'line' : chartType} text-4xl text-blue-500 mb-2"></i>
                    <p class="text-gray-600">Chart visualization would appear here</p>
                    <p class="text-sm text-gray-500">Chart type: ${chartType}</p>
                </div>
            `;
        }
    }

    /**
     * Destroy the copilot instance and clean up
     */
    destroy() {
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
            this.mutationObserver = null;
        }
        this.initialized = false;
        console.info(`[LensIQ Copilot v${this.version}] Destroyed.`);
    }
}

// Create global instance
window.LensIQCopilot = new LensIQCopilot();

// Auto-initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('copilot-input')) {
        window.LensIQCopilot.init();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LensIQCopilot;
}
