/**
 * Demo API Simulator
 *
 * This module simulates API responses for demo purposes.
 * It intercepts fetch requests and returns predefined responses.
 */

class DemoApiSimulator {
    constructor() {
        this.enabled = false;
        this.originalFetch = window.fetch;
        this.endpoints = {};
        this.errorRate = 0; // Percentage of requests that should fail (0-100)
        this.responseDelay = 1000; // Simulated network delay in ms
        this.initialized = false;
    }

    /**
     * Initialize the API simulator
     */
    init() {
        if (this.initialized) return;

        // Define simulated endpoints
        this.defineEndpoints();

        // Check URL parameters for simulator activation
        this.checkUrlForSimulatorActivation();

        this.initialized = true;
        console.log('Demo API Simulator initialized');
    }

    /**
     * Define simulated endpoints
     */
    defineEndpoints() {
        // Check if demo config is available
        if (window.demoConfig && window.demoConfig.apiSimulation && window.demoConfig.apiSimulation.endpoints) {
            // Load endpoints from config
            const configEndpoints = window.demoConfig.apiSimulation.endpoints;

            // Add each endpoint from config
            Object.keys(configEndpoints).forEach(endpoint => {
                this.endpoints[endpoint] = configEndpoints[endpoint];
            });

            // Set error rate and response delay if specified
            if (window.demoConfig.apiSimulation.defaultErrorRate !== undefined) {
                this.errorRate = window.demoConfig.apiSimulation.defaultErrorRate;
            }

            if (window.demoConfig.apiSimulation.defaultResponseDelay !== undefined) {
                this.responseDelay = window.demoConfig.apiSimulation.defaultResponseDelay;
            }

            console.log('Loaded API endpoints from config:', Object.keys(this.endpoints));
        } else {
            // Fallback to default endpoints
            this.defineDefaultEndpoints();
            console.log('Using default API endpoints');
        }
    }

    /**
     * Define default endpoints (fallback if config is not available)
     */
    defineDefaultEndpoints() {
        // Generate Insights endpoint
        this.endpoints['/api/generate-insights'] = {
            method: 'POST',
            response: {
                insights: [
                    {
                        headline: "Renewable Energy Growth Accelerating",
                        description: "Renewable energy trends show a 24% growth rate, significantly outpacing traditional energy sectors. This acceleration is particularly notable in solar and wind technologies.",
                        implications: "Investors should consider increasing allocation to renewable energy portfolios, especially those with strong solar and wind components."
                    },
                    {
                        headline: "ESG Integration Becoming Standard Practice",
                        description: "ESG metrics are increasingly being integrated into investment decision-making, with a 32% growth in adoption across funds.",
                        implications: "Portfolio companies without strong ESG frameworks may face increased scrutiny and potential devaluation."
                    },
                    {
                        headline: "Circular Economy Creating New Market Opportunities",
                        description: "Circular economy business models show 28% growth with particularly strong performance in packaging and consumer goods sectors.",
                        implications: "Early-stage investments in circular economy startups could yield significant returns as the model becomes mainstream."
                    }
                ]
            }
        };
    }

    /**
     * Check URL parameters for simulator activation
     */
    checkUrlForSimulatorActivation() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('demo') === 'true' && urlParams.get('simulate-api') === 'true') {
            this.enable();

            // Set error rate if specified
            const errorRate = urlParams.get('error-rate');
            if (errorRate && !isNaN(parseInt(errorRate))) {
                this.errorRate = parseInt(errorRate);
            }

            // Set response delay if specified
            const responseDelay = urlParams.get('response-delay');
            if (responseDelay && !isNaN(parseInt(responseDelay))) {
                this.responseDelay = parseInt(responseDelay);
            }
        }
    }

    /**
     * Enable the API simulator
     */
    enable() {
        if (this.enabled) return;

        // Override fetch
        window.fetch = this.fetchOverride.bind(this);
        this.enabled = true;
        console.log('Demo API Simulator enabled');
    }

    /**
     * Disable the API simulator
     */
    disable() {
        if (!this.enabled) return;

        // Restore original fetch
        window.fetch = this.originalFetch;
        this.enabled = false;
        console.log('Demo API Simulator disabled');
    }

    /**
     * Override fetch to simulate API responses
     */
    async fetchOverride(url, options = {}) {
        // Extract endpoint from URL
        const endpoint = new URL(url, window.location.origin).pathname;

        // Check if this endpoint is simulated
        if (this.endpoints[endpoint]) {
            const endpointConfig = this.endpoints[endpoint];

            // Check if method matches
            if (!options.method || options.method === endpointConfig.method) {
                // Simulate network delay
                await new Promise(resolve => setTimeout(resolve, this.responseDelay));

                // Randomly determine if this request should fail
                if (Math.random() * 100 < this.errorRate) {
                    // Simulate a network error
                    throw new Error('Network error');
                }

                // Return simulated response
                return new Response(JSON.stringify(endpointConfig.response), {
                    status: 200,
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            }
        }

        // For non-simulated endpoints, use the original fetch
        return this.originalFetch(url, options);
    }

    /**
     * Set the error rate
     *
     * @param {number} rate - Percentage of requests that should fail (0-100)
     */
    setErrorRate(rate) {
        if (rate >= 0 && rate <= 100) {
            this.errorRate = rate;
            console.log(`Demo API Simulator error rate set to ${rate}%`);
        }
    }

    /**
     * Set the response delay
     *
     * @param {number} delay - Simulated network delay in ms
     */
    setResponseDelay(delay) {
        if (delay >= 0) {
            this.responseDelay = delay;
            console.log(`Demo API Simulator response delay set to ${delay}ms`);
        }
    }

    /**
     * Add a simulated endpoint
     *
     * @param {string} endpoint - The endpoint path (e.g., '/api/example')
     * @param {string} method - The HTTP method (e.g., 'GET', 'POST')
     * @param {object} response - The response object
     */
    addEndpoint(endpoint, method, response) {
        this.endpoints[endpoint] = {
            method: method,
            response: response
        };
        console.log(`Added simulated endpoint: ${method} ${endpoint}`);
    }
}

// Create global instance
const demoApiSimulator = new DemoApiSimulator();

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    demoApiSimulator.init();
});

// Export for global access
window.demoApiSimulator = demoApiSimulator;
