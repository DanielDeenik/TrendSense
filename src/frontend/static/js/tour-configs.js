/**
 * Tour Configurations
 *
 * This file contains the Chain of Thought (CoT) tour configurations for different
 * sections of the TrendSense application.
 */

const tourConfigs = {
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
    },

    // TrendRadar tour configuration
    trendRadar: {
        name: "TrendRadar Analysis",
        description: "Learn how to analyze trends using TrendRadar",
        steps: [
            {
                thinking: "Let me show you how I evaluate investment potential using trend maturity and sustainability signals. I'll start by analyzing which trends are gaining strategic importance.",
                highlightSelector: "#trend-radar-visualization",
                actions: []
            },
            {
                thinking: "Trends in the Act zone have strong data signals, ESG maturity, and rising capital allocation. These are trends that are ready for immediate action.",
                highlightSelector: ".act-zone",
                actions: [
                    {
                        type: "zoom",
                        target: "act-zone"
                    }
                ]
            },
            {
                thinking: "The Prepare zone contains trends that are gaining momentum but aren't quite ready for full investment. These require monitoring and preparation.",
                highlightSelector: ".prepare-zone",
                actions: [
                    {
                        type: "zoom",
                        target: "prepare-zone"
                    }
                ]
            },
            {
                thinking: "The Watch zone contains early-stage trends with potential but higher uncertainty. These should be watched for future opportunities.",
                highlightSelector: ".watch-zone",
                actions: [
                    {
                        type: "zoom",
                        target: "watch-zone"
                    }
                ]
            },
            {
                thinking: "I can filter trends by different categories to focus on specific areas of interest. Let's look at trends related to Circularity.",
                highlightSelector: "#trend-filters",
                actions: [
                    {
                        type: "filter",
                        filterType: "category",
                        value: "Circularity"
                    }
                ]
            }
        ]
    },

    // VC Lens tour configuration
    vcLens: {
        name: "VC Lens Analysis",
        description: "Understand how to evaluate strategic fit using VC Lens",
        steps: [
            {
                thinking: "To decide if a trend aligns with a fund's thesis, I cross-reference ESG alignment, market vertical, and emerging LP interest.",
                highlightSelector: "#vc-lens-dashboard",
                actions: []
            },
            {
                thinking: "Let's apply some filters to focus our analysis. I'll filter for ESG: Circularity, Region: LATAM, and Stage: Series A.",
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
                thinking: "Now I see Circular Economy trends with traction in LATAM — especially in B2B packaging startups. This gives us a focused view of potential investment opportunities.",
                highlightSelector: "#vc-lens-results",
                actions: []
            },
            {
                thinking: "Let's assess how the market is reacting to this trend. I'll analyze sentiment, social engagement, and influencer clusters using the Venture Signal Graph.",
                highlightSelector: "#venture-signal-graph-btn",
                actions: [
                    {
                        type: "click",
                        selector: "#venture-signal-graph-btn"
                    }
                ]
            },
            {
                thinking: "The Venture Signal Graph shows relationships between companies, trends, and influencers. Let's zoom in on ReCircle, a promising startup in this space.",
                highlightSelector: "#node-ReCircle",
                actions: [
                    {
                        type: "zoom",
                        target: "ReCircle"
                    }
                ]
            },
            {
                thinking: "ReCircle has rising positive sentiment and appears in sustainability podcasts + X discussions — strong early signal. This indicates growing market interest.",
                highlightSelector: "#node-ReCircle",
                actions: []
            },
            {
                thinking: "Market interest is promising, but sustainability compliance is essential for institutional capital. Let's examine how this company aligns with ESG frameworks and upcoming regulations.",
                highlightSelector: "#esg-compliance-btn",
                actions: [
                    {
                        type: "click",
                        selector: "#esg-compliance-btn"
                    }
                ]
            },
            {
                thinking: "This company shows strong alignment with SFDR and CSRD metrics. Verified LCA submitted. Scope 3 needs work, but risk is manageable.",
                highlightSelector: "#esg-compliance-panel",
                actions: []
            },
            {
                thinking: "To gain confidence, I want to see if this trend pattern is emerging across other portfolio candidates or LP-aligned strategies.",
                highlightSelector: "#portfolio-signal-btn",
                actions: [
                    {
                        type: "click",
                        selector: "#portfolio-signal-btn"
                    }
                ]
            },
            {
                thinking: "This isn't a one-off. Multiple companies in this cluster show similar traction. Momentum is moving from fringe to thesis-fit.",
                highlightSelector: "#portfolio-signal-panel",
                actions: []
            },
            {
                thinking: "Signal quality is strong. But is there capital flowing into this space — and are exits realistic within this fund's timeline?",
                highlightSelector: "#capital-exit-btn",
                actions: [
                    {
                        type: "click",
                        selector: "#capital-exit-btn"
                    }
                ]
            },
            {
                thinking: "Early-stage capital is accelerating. Exit optionality exists via M&A, not IPO. Strategic alignment with buyers like Unilever strengthens the case.",
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
                thinking: "Graph Analytics helps visualize complex relationships between entities in the sustainability ecosystem. Let me show you how to interpret these connections.",
                highlightSelector: ".graph-card:first-child",
                actions: []
            },
            {
                thinking: "Each node represents an entity - companies, trends, funds, or projects. The connections between them show relationships like investments, influences, or partnerships.",
                highlightSelector: ".metric-card:first-child",
                actions: []
            },
            {
                thinking: "The Venture Signal Graph maps social trend influence, company interrelationships, and life cycle impacts across the investment ecosystem.",
                highlightSelector: ".graph-card:nth-child(1)",
                actions: []
            },
            {
                thinking: "The Network Graph visualizes the complete network of companies, projects, and sustainability initiatives, helping identify key players and relationships.",
                highlightSelector: ".graph-card:nth-child(2)",
                actions: []
            },
            {
                thinking: "The Supply Chain Graph analyzes supply chain relationships and sustainability impacts across tiers, helping identify risks and opportunities.",
                highlightSelector: ".graph-card:nth-child(3)",
                actions: []
            },
            {
                thinking: "The Impact Graph visualizes the impact of sustainability initiatives across environmental, social, and governance dimensions.",
                highlightSelector: ".graph-card:nth-child(4)",
                actions: []
            },
            {
                thinking: "Recent insights derived from graph analytics show emerging patterns, risks, and opportunities in the sustainability ecosystem.",
                highlightSelector: ".list-group-item:first-child",
                actions: []
            },
            {
                thinking: "By analyzing these graph visualizations, you can identify key relationships, emerging clusters, and potential risks in your sustainability investments.",
                highlightSelector: null,
                actions: []
            }
        ]
    },

    // Strategy tour configuration
    strategy: {
        name: "Strategy Hub",
        description: "Learn how to develop and test strategies",
        steps: [
            {
                thinking: "The Strategy Hub allows you to develop and test investment strategies based on sustainability trends and metrics. Let me show you how it works.",
                highlightSelector: "#strategy-dashboard",
                actions: []
            },
            {
                thinking: "You can select from different strategy frameworks or create your own custom strategy. Let's look at the Circular Economy strategy.",
                highlightSelector: "#strategy-selector",
                actions: [
                    {
                        type: "filter",
                        filterType: "strategy",
                        value: "Circular Economy"
                    }
                ]
            },
            {
                thinking: "The strategy performance metrics show how this approach has performed over time. I notice strong growth in the last 36 months with relatively low volatility.",
                highlightSelector: "#strategy-performance",
                actions: []
            },
            {
                thinking: "Let's benchmark this strategy against others to see how it compares. The Circular Economy strategy outperforms on sustainability metrics but has slightly lower financial returns.",
                highlightSelector: "#benchmark-btn",
                actions: [
                    {
                        type: "click",
                        selector: "#benchmark-btn"
                    }
                ]
            },
            {
                thinking: "Now let's create a story from this data that we can share with stakeholders. The storytelling feature helps create compelling narratives from your analysis.",
                highlightSelector: "#storytelling-btn",
                actions: [
                    {
                        type: "click",
                        selector: "#storytelling-btn"
                    }
                ]
            },
            {
                thinking: "My recommendation: Track this trend, monitor deal flow, and prepare LP reporting export. This gives you actionable next steps based on the analysis.",
                highlightSelector: "#action-buttons",
                actions: [
                    {
                        type: "display",
                        component: "action-buttons"
                    }
                ]
            }
        ]
    },

    // Error handling tour configuration
    errorHandling: {
        name: "Error Handling",
        description: "Understand and resolve errors in TrendSense",
        steps: [
            {
                thinking: "I notice there's an error with the AI content generation. Let me help you understand what's happening and how to resolve it.",
                highlightSelector: null,
                actions: []
            },
            {
                thinking: "This error might be occurring because the AI service is temporarily unavailable or there's an issue with the connection to the service.",
                highlightSelector: null,
                actions: []
            },
            {
                thinking: "If you're using the Perplexity API, make sure your API key is valid and has sufficient quota. You can check this in your Perplexity account dashboard.",
                highlightSelector: null,
                actions: []
            },
            {
                thinking: "Let's try to resolve this issue. First, you can try refreshing the page and attempting the action again. Sometimes temporary network issues can cause these errors.",
                highlightSelector: null,
                actions: []
            },
            {
                thinking: "If the error persists, you can try using the mock implementation instead. This will use pre-defined responses rather than calling the external API.",
                highlightSelector: null,
                actions: []
            },
            {
                thinking: "To use the mock implementation, you can temporarily remove your API key from the environment variables or configuration.",
                highlightSelector: null,
                actions: []
            },
            {
                thinking: "If you need further assistance, you can click the 'Need Help?' button to report the issue. Our support team will help you resolve it.",
                highlightSelector: "#tour-help-button",
                actions: []
            }
        ]
    }
};

// Export for global access
window.tourConfigs = tourConfigs;
