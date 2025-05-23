/**
 * Strategy Graph Integration for SustainaTrend
 * 
 * This file provides integration between the graph analytics and strategy features.
 */

// Strategy Graph Integration Class
class StrategyGraphIntegration {
    constructor() {
        this.strategyNodes = [];
        this.strategyEdges = [];
        this.strategyGraph = null;
        this.strategyMetrics = {};
        this.strategyImpacts = {};
    }

    /**
     * Initialize the strategy graph integration
     */
    initialize() {
        // Load saved strategy nodes from localStorage
        this.loadSavedStrategyNodes();
        
        // Initialize strategy metrics
        this.initializeStrategyMetrics();
        
        // Render strategy graph if container exists
        const strategyGraphContainer = document.getElementById('strategyGraphContainer');
        if (strategyGraphContainer) {
            this.renderStrategyGraph(strategyGraphContainer);
        }
        
        // Render strategy metrics if container exists
        const strategyMetricsContainer = document.getElementById('strategyMetricsContainer');
        if (strategyMetricsContainer) {
            this.renderStrategyMetrics(strategyMetricsContainer);
        }
        
        // Render strategy impacts if container exists
        const strategyImpactsContainer = document.getElementById('strategyImpactsContainer');
        if (strategyImpactsContainer) {
            this.renderStrategyImpacts(strategyImpactsContainer);
        }
    }

    /**
     * Load saved strategy nodes from localStorage
     */
    loadSavedStrategyNodes() {
        try {
            const savedNodes = localStorage.getItem('strategyNodes');
            const savedEdges = localStorage.getItem('strategyEdges');
            
            if (savedNodes) {
                this.strategyNodes = JSON.parse(savedNodes);
            }
            
            if (savedEdges) {
                this.strategyEdges = JSON.parse(savedEdges);
            }
        } catch (error) {
            console.error('Error loading saved strategy nodes:', error);
            this.strategyNodes = [];
            this.strategyEdges = [];
        }
    }

    /**
     * Save strategy nodes to localStorage
     */
    saveStrategyNodes() {
        try {
            localStorage.setItem('strategyNodes', JSON.stringify(this.strategyNodes));
            localStorage.setItem('strategyEdges', JSON.stringify(this.strategyEdges));
        } catch (error) {
            console.error('Error saving strategy nodes:', error);
        }
    }

    /**
     * Add a node to the strategy
     * @param {Object} node - The node to add
     */
    addNodeToStrategy(node) {
        // Check if node already exists
        const existingNode = this.strategyNodes.find(n => n.id === node.id);
        if (existingNode) {
            console.warn('Node already exists in strategy:', node.id);
            return false;
        }
        
        // Add node to strategy
        this.strategyNodes.push({
            id: node.id,
            name: node.name || node.id,
            type: node.type || 'unknown',
            metrics: this.extractNodeMetrics(node),
            addedAt: new Date().toISOString()
        });
        
        // Save strategy nodes
        this.saveStrategyNodes();
        
        // Update strategy metrics
        this.updateStrategyMetrics();
        
        return true;
    }

    /**
     * Add a relationship between nodes in the strategy
     * @param {string} sourceId - The source node ID
     * @param {string} targetId - The target node ID
     * @param {string} type - The relationship type
     */
    addRelationshipToStrategy(sourceId, targetId, type = 'related') {
        // Check if both nodes exist in strategy
        const sourceExists = this.strategyNodes.some(n => n.id === sourceId);
        const targetExists = this.strategyNodes.some(n => n.id === targetId);
        
        if (!sourceExists || !targetExists) {
            console.warn('Both nodes must exist in strategy to add relationship');
            return false;
        }
        
        // Check if relationship already exists
        const existingEdge = this.strategyEdges.find(e => 
            e.source === sourceId && e.target === targetId && e.type === type
        );
        
        if (existingEdge) {
            console.warn('Relationship already exists in strategy');
            return false;
        }
        
        // Add relationship to strategy
        this.strategyEdges.push({
            id: `${sourceId}-${targetId}-${type}`,
            source: sourceId,
            target: targetId,
            type: type,
            addedAt: new Date().toISOString()
        });
        
        // Save strategy edges
        this.saveStrategyNodes();
        
        return true;
    }

    /**
     * Extract metrics from a node
     * @param {Object} node - The node to extract metrics from
     * @returns {Object} The extracted metrics
     */
    extractNodeMetrics(node) {
        const metrics = {};
        
        if (node.type === 'company' && node.sustainability_metrics) {
            metrics.environmental = node.sustainability_metrics.environmental_score || 0;
            metrics.social = node.sustainability_metrics.social_score || 0;
            metrics.governance = node.sustainability_metrics.governance_score || 0;
            metrics.esg = node.sustainability_metrics.esg_score || 0;
        } else if (node.type === 'trend') {
            metrics.relevance = node.relevance_score || node.relevance || 0;
            metrics.growth = node.growth_rate || 0;
        } else if (node.type === 'project' && node.sustainability_metrics) {
            metrics.carbonImpact = node.sustainability_metrics.carbon_impact || 0;
            metrics.sdgAlignment = node.sustainability_metrics.sdg_alignment || [];
        }
        
        return metrics;
    }

    /**
     * Initialize strategy metrics
     */
    initializeStrategyMetrics() {
        this.strategyMetrics = {
            environmentalScore: 0,
            socialScore: 0,
            governanceScore: 0,
            esgScore: 0,
            carbonImpact: 0,
            sdgCoverage: [],
            trendAlignment: 0,
            networkDensity: 0
        };
        
        this.updateStrategyMetrics();
    }

    /**
     * Update strategy metrics based on current nodes
     */
    updateStrategyMetrics() {
        // Reset metrics
        const metrics = {
            environmentalScore: 0,
            socialScore: 0,
            governanceScore: 0,
            esgScore: 0,
            carbonImpact: 0,
            sdgCoverage: [],
            trendAlignment: 0,
            networkDensity: 0
        };
        
        // Count node types
        const companyNodes = this.strategyNodes.filter(n => n.type === 'company');
        const trendNodes = this.strategyNodes.filter(n => n.type === 'trend');
        const projectNodes = this.strategyNodes.filter(n => n.type === 'project');
        
        // Calculate ESG metrics from company nodes
        if (companyNodes.length > 0) {
            let envTotal = 0, socTotal = 0, govTotal = 0, esgTotal = 0;
            
            companyNodes.forEach(node => {
                envTotal += node.metrics.environmental || 0;
                socTotal += node.metrics.social || 0;
                govTotal += node.metrics.governance || 0;
                esgTotal += node.metrics.esg || 0;
            });
            
            metrics.environmentalScore = envTotal / companyNodes.length;
            metrics.socialScore = socTotal / companyNodes.length;
            metrics.governanceScore = govTotal / companyNodes.length;
            metrics.esgScore = esgTotal / companyNodes.length;
        }
        
        // Calculate carbon impact and SDG coverage from project nodes
        projectNodes.forEach(node => {
            metrics.carbonImpact += node.metrics.carbonImpact || 0;
            
            if (node.metrics.sdgAlignment && node.metrics.sdgAlignment.length > 0) {
                node.metrics.sdgAlignment.forEach(sdg => {
                    if (!metrics.sdgCoverage.includes(sdg)) {
                        metrics.sdgCoverage.push(sdg);
                    }
                });
            }
        });
        
        // Calculate trend alignment
        if (trendNodes.length > 0) {
            let trendAlignmentTotal = 0;
            
            trendNodes.forEach(node => {
                trendAlignmentTotal += node.metrics.relevance || 0;
            });
            
            metrics.trendAlignment = trendAlignmentTotal / trendNodes.length;
        }
        
        // Calculate network density
        if (this.strategyNodes.length > 1) {
            const maxPossibleEdges = this.strategyNodes.length * (this.strategyNodes.length - 1) / 2;
            metrics.networkDensity = this.strategyEdges.length / maxPossibleEdges;
        }
        
        // Update strategy metrics
        this.strategyMetrics = metrics;
        
        // Calculate strategy impacts
        this.updateStrategyImpacts();
    }

    /**
     * Update strategy impacts based on current metrics
     */
    updateStrategyImpacts() {
        this.strategyImpacts = {
            sustainabilityImpact: this.calculateSustainabilityImpact(),
            marketImpact: this.calculateMarketImpact(),
            innovationImpact: this.calculateInnovationImpact(),
            overallStrategyScore: 0
        };
        
        // Calculate overall strategy score
        this.strategyImpacts.overallStrategyScore = (
            this.strategyImpacts.sustainabilityImpact +
            this.strategyImpacts.marketImpact +
            this.strategyImpacts.innovationImpact
        ) / 3;
    }

    /**
     * Calculate sustainability impact score
     * @returns {number} The sustainability impact score (0-100)
     */
    calculateSustainabilityImpact() {
        const esgWeight = 0.4;
        const carbonWeight = 0.3;
        const sdgWeight = 0.3;
        
        const esgScore = this.strategyMetrics.esgScore;
        
        // Normalize carbon impact (negative is better)
        const carbonImpact = this.strategyMetrics.carbonImpact < 0 ? 100 : 0;
        
        // Normalize SDG coverage (more is better, max 17)
        const sdgCoverage = (this.strategyMetrics.sdgCoverage.length / 17) * 100;
        
        return (esgScore * esgWeight) + (carbonImpact * carbonWeight) + (sdgCoverage * sdgWeight);
    }

    /**
     * Calculate market impact score
     * @returns {number} The market impact score (0-100)
     */
    calculateMarketImpact() {
        const trendWeight = 0.6;
        const networkWeight = 0.4;
        
        // Normalize trend alignment (0-1 to 0-100)
        const trendAlignment = this.strategyMetrics.trendAlignment * 100;
        
        // Normalize network density (0-1 to 0-100)
        const networkDensity = this.strategyMetrics.networkDensity * 100;
        
        return (trendAlignment * trendWeight) + (networkDensity * networkWeight);
    }

    /**
     * Calculate innovation impact score
     * @returns {number} The innovation impact score (0-100)
     */
    calculateInnovationImpact() {
        // Simplified calculation based on trend alignment and project count
        const trendCount = this.strategyNodes.filter(n => n.type === 'trend').length;
        const projectCount = this.strategyNodes.filter(n => n.type === 'project').length;
        
        // More trends and projects = higher innovation score
        const trendFactor = Math.min(trendCount / 5, 1); // Max 5 trends
        const projectFactor = Math.min(projectCount / 10, 1); // Max 10 projects
        
        return ((trendFactor + projectFactor) / 2) * 100;
    }
}

// Initialize strategy graph integration when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.strategyGraphIntegration = new StrategyGraphIntegration();
    window.strategyGraphIntegration.initialize();
});
