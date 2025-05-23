/**
 * Demo Mode Configuration
 * 
 * This file contains the configuration for the demo mode, including scenarios,
 * API simulation settings, and keyboard shortcuts.
 */

const demoConfig = {
    // Demo scenarios
    scenarios: {
        // Error Handling Demo
        errorHandling: {
            name: 'Error Handling Demo',
            description: 'Demonstrates how the guided tour handles API errors',
            autoplay: true,
            autoplayDelay: 3000,
            steps: [
                {
                    name: 'Start Tour',
                    description: 'Start the AI-guided tour',
                    delay: 2000
                },
                {
                    name: 'Navigate to TrendRadar',
                    description: 'Go to the TrendRadar page',
                    delay: 2000
                },
                {
                    name: 'Trigger API Error',
                    description: 'Simulate an API error',
                    delay: 3000
                },
                {
                    name: 'Wait for Error Tour',
                    description: 'Wait for the error handling tour to appear',
                    delay: 5000
                },
                {
                    name: 'Navigate Through Error Tour',
                    description: 'Go through the error handling steps',
                    delay: 3000
                },
                {
                    name: 'Continue Error Tour',
                    description: 'Continue through the error handling steps',
                    delay: 3000
                },
                {
                    name: 'Open Help Modal',
                    description: 'Open the help modal',
                    delay: 4000
                },
                {
                    name: 'Ask Co-Pilot',
                    description: 'Get suggestions from the Co-Pilot',
                    delay: 5000
                },
                {
                    name: 'Close Help Modal',
                    description: 'Close the help modal',
                    delay: 2000
                },
                {
                    name: 'End Demo',
                    description: 'End the demo',
                    delay: 0
                }
            ]
        },
        
        // Guided Tour Demo
        guidedTour: {
            name: 'Guided Tour Demo',
            description: 'Demonstrates the AI-guided tour feature',
            autoplay: true,
            autoplayDelay: 3000,
            steps: [
                {
                    name: 'Start Tour',
                    description: 'Start the AI-guided tour',
                    delay: 2000
                },
                {
                    name: 'Explore Dashboard',
                    description: 'Explore the main dashboard',
                    delay: 3000
                },
                {
                    name: 'View Trends',
                    description: 'View sustainability trends',
                    delay: 3000
                },
                {
                    name: 'End Demo',
                    description: 'End the demo',
                    delay: 0
                }
            ]
        }
    },
    
    // API simulation settings
    apiSimulation: {
        // Default error rate (percentage of requests that should fail)
        defaultErrorRate: 0,
        
        // Default response delay (ms)
        defaultResponseDelay: 1000,
        
        // Simulated endpoints
        endpoints: {
            '/api/generate-insights': {
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
            },
            '/api/analyze-trend': {
                method: 'POST',
                response: {
                    trend: {
                        name: "Renewable Energy",
                        score: 85,
                        momentum: "Increasing",
                        maturity: "Growth",
                        analysis: "Renewable energy continues to show strong growth potential with increasing adoption rates across both developed and emerging markets. Policy support remains strong, and technological improvements are driving down costs."
                    }
                }
            }
        }
    },
    
    // Keyboard shortcuts
    keyboardShortcuts: {
        toggleControlPanel: {
            key: 'D',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Toggle demo control panel'
        },
        startDemo: {
            key: 'S',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Start demo with selected scenario'
        },
        stopDemo: {
            key: 'X',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Stop demo'
        },
        nextStep: {
            key: 'N',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Go to next step'
        },
        toggleAutoplay: {
            key: 'A',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Toggle autoplay'
        },
        toggleRecordingIndicator: {
            key: 'R',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Toggle recording indicator'
        }
    }
};

// Export for global access
window.demoConfig = demoConfig;
