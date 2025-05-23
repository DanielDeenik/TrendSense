/**
 * TrendSense™ Tour Configuration
 *
 * This file contains the configuration for the Chain of Thought (CoT) guided tour.
 * It defines the steps, narration, and UI elements for each part of the tour.
 *
 * The tour is designed to reveal the AI's reasoning process rather than providing
 * static instructions, making it more intuitive and AI-native.
 */

// Initialize tour when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Create TourMode instance if not already created
    if (!window.tourMode) {
        initializeTour();
    }

    // Check if tour should start automatically
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('tour') === 'true') {
        // Small delay to ensure DOM is ready
        setTimeout(() => {
            if (window.tourMode) {
                window.tourMode.startTour();
            }
        }, 500);
    }

    // Add event listener to tour toggle checkbox if it exists
    const tourToggle = document.getElementById('tourToggle');
    if (tourToggle) {
        tourToggle.addEventListener('change', function() {
            if (this.checked) {
                // Store tour state
                localStorage.setItem('TrendSense_Tour', 'on');
                // Start tour
                if (window.tourMode) {
                    window.tourMode.startTour();
                }
            } else {
                // Store tour state
                localStorage.setItem('TrendSense_Tour', 'off');
                // End tour
                if (window.tourMode) {
                    window.tourMode.endTour();
                }
            }
        });

        // Set initial state based on localStorage
        if (localStorage.getItem('TrendSense_Tour') === 'on') {
            tourToggle.checked = true;
        }
    }

    // Add navigation links for tour routes
    setupTourNavigation();

    // Initialize help logger if tour is active
    if (window.tourMode && window.tourMode.isActive()) {
        // Load help modal component
        loadHelpComponents();
    }
});

/**
 * Setup navigation links for tour routes
 * This ensures all routes needed for the tour are accessible
 */
function setupTourNavigation() {
    // Define the routes needed for the tour
    const tourRoutes = [
        { name: 'TrendRadar', path: '/trendradar', id: 'trendradar-nav' },
        { name: 'VC Lens', path: '/vc-lens', id: 'vc-lens-nav' },
        { name: 'Graph Analytics', path: '/graph-analytics', id: 'graph-analytics-nav' },
        { name: 'Lifecycle Analysis', path: '/lifecycle', id: 'lifecycle-nav' },
        { name: 'Copilot', path: '/copilot', id: 'copilot-nav' }
    ];

    // Check if we need to add navigation links
    const navContainer = document.querySelector('.tour-navigation');
    if (!navContainer) {
        // Create a container for tour navigation if it doesn't exist
        const container = document.createElement('div');
        container.className = 'tour-navigation hidden fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800 rounded-lg shadow-lg p-2 z-50 flex space-x-2';

        // Add navigation links
        tourRoutes.forEach(route => {
            const link = document.createElement('a');
            link.href = route.path;
            link.id = route.id;
            link.className = 'px-3 py-1 text-sm text-gray-300 hover:text-white hover:bg-gray-700 rounded';
            link.textContent = route.name;
            container.appendChild(link);
        });

        // Add to document
        document.body.appendChild(container);
    }
}

/**
 * Load help components for the tour
 * This includes the help button and modal
 */
function loadHelpComponents() {
    // Load help logger script if not already loaded
    if (!window.tourHelpLogger) {
        loadScript('/static/js/tour-help-logger.js');
    }

    // Load Co-Pilot responses script if not already loaded
    if (!window.tourCopilotResponses) {
        loadScript('/static/js/tour-copilot-responses.js');
    }

    // Load help modal component if not already loaded
    if (!document.getElementById('tour-help-modal')) {
        // Create container for help modal
        const modalContainer = document.createElement('div');
        modalContainer.id = 'tour-help-modal-container';
        document.body.appendChild(modalContainer);

        // Load help modal content
        fetch('/templates/components/help_modal.html')
            .then(response => response.text())
            .then(html => {
                modalContainer.innerHTML = html;

                // Initialize any scripts in the modal
                const scripts = modalContainer.getElementsByTagName('script');
                for (let i = 0; i < scripts.length; i++) {
                    eval(scripts[i].innerText);
                }
            })
            .catch(error => {
                console.error('Error loading help modal:', error);
                // Fallback to creating a simple help button
                createSimpleHelpButton();
            });
    }
}

/**
 * Create a simple help button as fallback
 */
function createSimpleHelpButton() {
    // Check if button already exists
    if (document.getElementById('tour-help-button')) {
        return;
    }

    // Create button element
    const helpButton = document.createElement('button');
    helpButton.id = 'tour-help-button';
    helpButton.className = 'fixed bottom-6 left-6 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full shadow-lg flex items-center z-50';
    helpButton.innerHTML = `
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        Need Help?
    `;

    // Add click event listener
    helpButton.addEventListener('click', () => {
        // Create a simple alert with help information
        alert('Need help with the tour? Try refreshing the page and adding ?tour=true to the URL to restart the tour. If you continue to experience issues, please contact support@trendsense.ai.');
    });

    // Add to document
    document.body.appendChild(helpButton);
}

/**
 * Load a script dynamically
 */
function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

/**
 * Initialize the tour with configurations for each route
 */
function initializeTour() {
    // Define tour configurations for each route
    window.tourConfigs = {
        // TrendRadar tour configuration
        trendRadar: {
            name: "TrendRadar Analysis",
            description: "Learn how to analyze trends using TrendRadar",
            steps: [
                {
                    thinking: "I begin by scanning macro signals across the market. My first step is to identify which sustainability trends are gaining strategic importance based on multiple data sources.",
                    highlightSelector: "#trend-radar",
                    actions: []
                },
                {
                    thinking: "I'm looking at trends in the 'Act' zone - these have strong data signals, ESG maturity, and rising capital allocation. These are trends that are ready for immediate action.",
                    highlightSelector: ".act-zone",
                    actions: [
                        {
                            type: "zoom",
                            target: "act-zone"
                        }
                    ]
                },
                {
                    thinking: "For this circular economy trend, I'm seeing strong regulatory tailwinds from CSRD and EU Taxonomy alignment. The social sentiment is also positive with 72% growth in mentions.",
                    highlightSelector: "#trend-details",
                    actions: []
                },
                {
                    thinking: "I notice this trend has significant Series A and B funding momentum - up 43% YoY. This indicates market validation beyond just regulatory push.",
                    highlightSelector: "#funding-momentum",
                    actions: []
                },
                {
                    thinking: "Let me check the geographic distribution. LATAM shows particularly strong adoption signals for circular economy solutions in packaging and waste management.",
                    highlightSelector: "#geo-distribution",
                    actions: []
                },
                {
                    thinking: "Based on this analysis, I'll focus on circular economy startups in LATAM with B2B models that have regulatory alignment and proven market traction.",
                    highlightSelector: "#trend-summary",
                    actions: []
                }
            ]
        },

        // VC Lens tour configuration
        vcLens: {
            name: "VC Lens Analysis",
            description: "Understand how to evaluate strategic fit using VC Lens",
            steps: [
                {
                    thinking: "Now I'll filter by fund strategy to find the most promising opportunities. I'm looking for companies that align with our thesis on circularity in LATAM.",
                    highlightSelector: "#vc-lens-panel",
                    actions: []
                },
                {
                    thinking: "I'll apply filters for ESG: Circularity, Region: LATAM, and Stage: Series A. This narrows our focus to high-alignment, high-impact startups.",
                    highlightSelector: "#vc-lens-filters",
                    actions: [
                        {
                            type: "filter",
                            filterType: "esg",
                            value: "Circularity"
                        },
                        {
                            type: "filter",
                            filterType: "region",
                            value: "LATAM"
                        },
                        {
                            type: "filter",
                            filterType: "stage",
                            value: "Series A"
                        }
                    ]
                },
                {
                    thinking: "ReCircle stands out with an ESG score of 85 and growth of +42%. Their B2B packaging solution shows strong product-market fit and scalability potential.",
                    highlightSelector: "#company-recircle",
                    actions: []
                },
                {
                    thinking: "Market interest is promising, but sustainability compliance is essential for institutional capital. Let me examine how ReCircle aligns with ESG frameworks and upcoming regulations.",
                    highlightSelector: "#esg-compliance-btn",
                    actions: [
                        {
                            type: "click",
                            selector: "#esg-compliance-btn"
                        }
                    ]
                },
                {
                    thinking: "ReCircle shows strong alignment with SFDR and CSRD metrics. They have a verified LCA submitted. Their Scope 3 emissions tracking needs work, but the risk is manageable.",
                    highlightSelector: "#esg-compliance-panel",
                    actions: []
                },
                {
                    thinking: "Let me check if this trend pattern is emerging across other portfolio candidates. This helps validate our thesis and identify potential synergies.",
                    highlightSelector: "#portfolio-signal-btn",
                    actions: [
                        {
                            type: "click",
                            selector: "#portfolio-signal-btn"
                        }
                    ]
                },
                {
                    thinking: "I see similar companies with strong social momentum. There are 3 LP-backed portfolio companies in adjacent spaces, suggesting ecosystem validation.",
                    highlightSelector: "#portfolio-signal-panel",
                    actions: []
                },
                {
                    thinking: "Finally, I need to analyze capital flows and exit pathways. This helps assess the full investment lifecycle potential.",
                    highlightSelector: "#capital-exit-btn",
                    actions: [
                        {
                            type: "click",
                            selector: "#capital-exit-btn"
                        }
                    ]
                },
                {
                    thinking: "Capital inflows to circular economy in LATAM are up 37% YoY. There are 5 strategic corporate buyers showing interest, and the average time-to-exit is 5.2 years.",
                    highlightSelector: "#capital-exit-panel",
                    actions: []
                }
            ]
        },

        // Graph Analytics tour configuration
        graphAnalytics: {
            name: "Graph Analytics",
            description: "Explore relationships using Graph Analytics",
            steps: [
                {
                    thinking: "The Venture Signal Graph helps visualize complex relationships between entities in the sustainability ecosystem. Let me show you how to interpret these connections.",
                    highlightSelector: "#signal-graph",
                    actions: []
                },
                {
                    thinking: "Each node represents an entity - companies, trends, funds, or projects. The connections between them show relationships like investments, influences, or partnerships.",
                    highlightSelector: "#graph-legend",
                    actions: []
                },
                {
                    thinking: "ReCircle is gaining significant traction through social channels and ecosystem mentions. I can see strong upward momentum in both investor interest and customer adoption.",
                    highlightSelector: "#node-recircle",
                    actions: [
                        {
                            type: "zoom",
                            target: "node-recircle"
                        }
                    ]
                },
                {
                    thinking: "The connections show ReCircle has partnerships with 3 major CPG companies and is mentioned alongside other successful circular economy startups. This network effect strengthens their position.",
                    highlightSelector: "#connections-recircle",
                    actions: []
                },
                {
                    thinking: "I notice a strong connection between ReCircle and renewable energy trends. This suggests they're positioning their circular solution as part of a broader sustainability ecosystem.",
                    highlightSelector: "#cluster-renewable-circular",
                    actions: []
                },
                {
                    thinking: "Even if a trend is hot, we need to look at impact and risk. Let me check CO₂ impact, circularity potential, and regulation readiness for ReCircle.",
                    highlightSelector: "#lifecycle-btn",
                    actions: [
                        {
                            type: "click",
                            selector: "#lifecycle-btn"
                        }
                    ]
                }
            ]
        },

        // Lifecycle tour configuration
        lifecycle: {
            name: "Lifecycle Analysis",
            description: "Understand lifecycle impacts and ESG metrics",
            steps: [
                {
                    thinking: "The Lifecycle Scorecard shows ReCircle's sustainability metrics across their entire value chain. This is crucial for assessing true impact and regulatory alignment.",
                    highlightSelector: "#lifecycle-panel",
                    actions: []
                },
                {
                    thinking: "ReCircle shows low carbon intensity (17.3 tCO2e/unit), high reuse factor (8.4x), and strong CSRD compliance readiness (83%). These metrics improve their risk-adjusted return potential.",
                    highlightSelector: "#lifecycle-scorecard",
                    actions: []
                },
                {
                    thinking: "Their circularity metrics are particularly strong - 94% recyclable materials and 72% closed-loop processes. This aligns perfectly with EU Taxonomy requirements.",
                    highlightSelector: "#circularity-metrics",
                    actions: []
                },
                {
                    thinking: "Water usage is 43% below industry average, and they have zero hazardous waste output. These environmental factors reduce regulatory risk significantly.",
                    highlightSelector: "#environmental-metrics",
                    actions: []
                },
                {
                    thinking: "Social impact metrics show 1,200+ waste collector jobs created and 85% fair wage certification. This strengthens their social license to operate in LATAM markets.",
                    highlightSelector: "#social-metrics",
                    actions: []
                },
                {
                    thinking: "The LP-Ready badge indicates this company meets institutional investor ESG requirements. This facilitates smoother capital raising in future rounds.",
                    highlightSelector: "#lp-ready-badge",
                    actions: []
                }
            ]
        },

        // Copilot tour configuration
        copilot: {
            name: "AI Copilot",
            description: "Learn how to use the AI Copilot",
            steps: [
                {
                    thinking: "The AI Copilot allows you to ask questions and get insights about trends, companies, and investment opportunities. I synthesize signals and ESG data into actionable insights.",
                    highlightSelector: "#copilot-bar",
                    actions: []
                },
                {
                    thinking: "You can ask me to summarize trends, suggest exit strategies, generate LP-ready investment memos, or analyze competitive landscapes - all using natural language.",
                    highlightSelector: "#copilot-examples",
                    actions: []
                },
                {
                    thinking: "For example, you could ask: 'Compare ReCircle's unit economics to industry benchmarks' or 'Generate an ESG impact summary for LP reporting'.",
                    highlightSelector: "#copilot-input",
                    actions: []
                },
                {
                    thinking: "My responses include Chain of Thought reasoning so you can see how I arrived at my conclusions. This transparency builds trust in the insights provided.",
                    highlightSelector: "#copilot-response",
                    actions: []
                },
                {
                    thinking: "I can also generate visualizations, export data to spreadsheets, or create presentation-ready slides based on your requests.",
                    highlightSelector: "#copilot-tools",
                    actions: []
                },
                {
                    thinking: "The more you interact with me, the better I understand your investment preferences and decision-making style, allowing for more personalized insights over time.",
                    highlightSelector: "#copilot-personalization",
                    actions: []
                }
            ]
        },

        // Default tour configuration
        default: {
            name: "TrendSense Overview",
            description: "Explore the key features of TrendSense",
            steps: [
                {
                    thinking: "Welcome to TrendSense! I'm your AI guide to understanding sustainability trends and investment opportunities. Let me show you around the platform.",
                    highlightSelector: null,
                    actions: []
                },
                {
                    thinking: "The navigation menu on the left provides access to all the key features of TrendSense. Let's explore what each section offers.",
                    highlightSelector: "#sidebar",
                    actions: []
                },
                {
                    thinking: "TrendSense helps you identify, analyze, and capitalize on emerging sustainability trends using advanced AI and data analytics.",
                    highlightSelector: null,
                    actions: []
                }
            ]
        }
    };

    // Create TourMode instance
    window.tourMode = new TourMode();
    window.tourMode.init();
}
