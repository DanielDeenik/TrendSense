"""
Venture Signal Graph with Life Cycle Analysis Service

This module provides functionality for analyzing company relationships,
social trend influences, and life cycle impacts across the investment ecosystem.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple

import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph

# Set up logging
logger = logging.getLogger(__name__)

class VentureSignalGraph:
    """
    A service for analyzing venture signals, social trends, and life cycle impacts.
    """
    
    def __init__(self):
        """Initialize the Venture Signal Graph service."""
        self.graph = nx.DiGraph()
        self.companies = {}
        self.trends = {}
        self.relationships = []
        self.lca_data = {}
    
    def load_data(self, companies: List[Dict], trends: List[Dict], 
                 relationships: List[Dict], lca_data: Optional[Dict] = None) -> None:
        """
        Load data into the graph.
        
        Args:
            companies: List of company dictionaries with metadata
            trends: List of social trend dictionaries
            relationships: List of relationship dictionaries
            lca_data: Dictionary of life cycle assessment data by company
        """
        self.companies = {company['id']: company for company in companies}
        self.trends = {trend['id']: trend for trend in trends}
        self.relationships = relationships
        self.lca_data = lca_data or {}
        
        # Build the graph
        self._build_graph()
        
        logger.info(f"Loaded {len(self.companies)} companies, {len(self.trends)} trends, "
                   f"and {len(self.relationships)} relationships into the graph.")
    
    def _build_graph(self) -> None:
        """Build the NetworkX graph from the loaded data."""
        # Clear existing graph
        self.graph.clear()
        
        # Add company nodes
        for company_id, company in self.companies.items():
            self.graph.add_node(company_id, 
                               type='company',
                               name=company.get('name', ''),
                               sector=company.get('sector', ''),
                               **{k: v for k, v in company.items() if k not in ['id', 'name', 'sector']})
        
        # Add trend nodes
        for trend_id, trend in self.trends.items():
            self.graph.add_node(trend_id,
                               type='trend',
                               name=trend.get('name', ''),
                               category=trend.get('category', ''),
                               **{k: v for k, v in trend.items() if k not in ['id', 'name', 'category']})
        
        # Add relationship edges
        for rel in self.relationships:
            source_id = rel.get('source')
            target_id = rel.get('target')
            rel_type = rel.get('type')
            
            if not (source_id and target_id and rel_type):
                logger.warning(f"Skipping relationship with missing data: {rel}")
                continue
                
            if source_id not in self.graph or target_id not in self.graph:
                logger.warning(f"Skipping relationship with unknown node: {rel}")
                continue
            
            self.graph.add_edge(source_id, target_id, 
                               type=rel_type,
                               **{k: v for k, v in rel.items() if k not in ['source', 'target', 'type']})
    
    def get_graph_data(self) -> Dict:
        """
        Get the graph data in a format suitable for visualization.
        
        Returns:
            Dictionary with nodes and links for visualization
        """
        return json_graph.node_link_data(self.graph)
    
    def analyze_social_signals(self) -> Dict[str, Dict]:
        """
        Analyze social signal strengths for each company.
        
        Returns:
            Dictionary mapping company IDs to their social signal analysis
        """
        results = {}
        
        for company_id, company in self.companies.items():
            # Get incoming edges from trends
            trend_edges = [
                (u, v, d) for u, v, d in self.graph.in_edges(company_id, data=True)
                if self.graph.nodes[u]['type'] == 'trend'
            ]
            
            # Calculate signal strength based on number and weight of trend connections
            signal_strength = "Low"
            if len(trend_edges) >= 5:
                signal_strength = "High"
            elif len(trend_edges) >= 2:
                signal_strength = "Medium"
            
            # Extract influencers from company data
            influencers = company.get('influencers', [])
            
            # Extract sentiment from company data or calculate from relationships
            sentiment = company.get('sentiment', 'Neutral')
            
            results[company_id] = {
                'signal_strength': signal_strength,
                'key_influencers': influencers,
                'trending_sentiment': sentiment,
                'connected_trends': [self.trends[u]['name'] for u, _, _ in trend_edges]
            }
        
        return results
    
    def analyze_life_cycle_impacts(self) -> Dict[str, Dict]:
        """
        Analyze life cycle impacts for each company.
        
        Returns:
            Dictionary mapping company IDs to their life cycle impact analysis
        """
        results = {}
        
        for company_id, company in self.companies.items():
            # Get LCA data for this company
            lca = self.lca_data.get(company_id, {})
            
            # Determine carbon footprint
            carbon_footprint = lca.get('carbon_footprint', 'Medium')
            
            # Determine resource efficiency
            resource_efficiency = lca.get('resource_efficiency', 'Moderate')
            
            # Determine circularity potential
            circularity_potential = lca.get('circularity_potential', 'Medium')
            
            # Determine compliance readiness
            compliance_readiness = []
            if lca.get('csrd_ready', False):
                compliance_readiness.append('CSRD')
            if lca.get('sfdr_ready', False):
                compliance_readiness.append('SFDR')
            
            compliance_str = ', '.join(compliance_readiness) if compliance_readiness else 'None'
            
            results[company_id] = {
                'carbon_footprint': carbon_footprint,
                'resource_efficiency': resource_efficiency,
                'circularity_potential': circularity_potential,
                'compliance_readiness': compliance_str
            }
        
        return results
    
    def generate_investor_summaries(self) -> Dict[str, Dict]:
        """
        Generate investor summaries for each company.
        
        Returns:
            Dictionary mapping company IDs to their investor summaries
        """
        social_signals = self.analyze_social_signals()
        life_cycle_impacts = self.analyze_life_cycle_impacts()
        
        results = {}
        
        for company_id, company in self.companies.items():
            signals = social_signals.get(company_id, {})
            impacts = life_cycle_impacts.get(company_id, {})
            
            # Determine trend fit
            trend_fit = signals.get('connected_trends', [])
            
            # Determine investor attractiveness based on signals and impacts
            attractiveness = self._calculate_attractiveness(signals, impacts)
            
            # Determine recommended action
            recommended_action = self._determine_recommended_action(attractiveness)
            
            results[company_id] = {
                'name': company.get('name', ''),
                'trend_fit': trend_fit,
                'signal_strength': signals.get('signal_strength', 'Low'),
                'key_influencers': signals.get('key_influencers', []),
                'trending_sentiment': signals.get('trending_sentiment', 'Neutral'),
                'lca_summary': impacts,
                'investor_attractiveness': attractiveness,
                'recommended_action': recommended_action
            }
        
        return results
    
    def _calculate_attractiveness(self, signals: Dict, impacts: Dict) -> str:
        """
        Calculate investor attractiveness based on signals and impacts.
        
        Args:
            signals: Social signal analysis for a company
            impacts: Life cycle impact analysis for a company
            
        Returns:
            String describing investor attractiveness
        """
        # Score signal strength
        signal_score = {
            'High': 3,
            'Medium': 2,
            'Low': 1
        }.get(signals.get('signal_strength', 'Low'), 1)
        
        # Score sentiment
        sentiment_score = {
            'Positive': 3,
            'Neutral': 2,
            'Negative': 1
        }.get(signals.get('trending_sentiment', 'Neutral'), 2)
        
        # Score carbon footprint (inverse - lower is better)
        carbon_score = {
            'Low': 3,
            'Medium': 2,
            'High': 1
        }.get(impacts.get('carbon_footprint', 'Medium'), 2)
        
        # Score circularity potential
        circularity_score = {
            'High': 3,
            'Medium': 2,
            'Low': 1
        }.get(impacts.get('circularity_potential', 'Medium'), 2)
        
        # Calculate total score
        total_score = signal_score + sentiment_score + carbon_score + circularity_score
        
        # Determine attractiveness based on total score
        if total_score >= 10:
            return "Strong early-stage signal, aligned with sustainability trends, leading positive sentiment."
        elif total_score >= 7:
            return "Moderate potential, some alignment with sustainability trends, mixed signals."
        else:
            return "Limited current signals, may require further development or pivoting."
    
    def _determine_recommended_action(self, attractiveness: str) -> str:
        """
        Determine recommended action based on attractiveness.
        
        Args:
            attractiveness: Investor attractiveness description
            
        Returns:
            Recommended action string
        """
        if "Strong" in attractiveness:
            return "Strong Candidate"
        elif "Moderate" in attractiveness:
            return "Monitor Closely"
        else:
            return "Low Priority"
    
    def get_prompt_template(self) -> str:
        """
        Get the GPT-4.1 prompt template for Venture Signal Graph analysis.
        
        Returns:
            String containing the prompt template
        """
        template = """
## ✅ GPT-4.1 Prompt Template

### **System Role**

You are a **Venture Signal Graph Analyst and Sustainability Life Cycle Expert**.
Your task is to **map social trend influence**, **company interrelationships**, and **life cycle impacts** across the investment ecosystem.

---

### **Instructions**

You will be given:

* **A list of companies** with their public signals (e.g., social mentions, partnerships, influencer traction)
* **A list of social trends** they are associated with
* **Life Cycle Assessment (LCA) data** or sustainability claims (e.g., carbon footprint, waste reduction, water usage)

You will:

1. **Map the relationships** into a graph structure
2. **Analyze social signal strengths and cluster influence**
3. **Apply life cycle thinking** to score the environmental impact
4. **Provide an investor summary** showing:

   * Trend fit
   * Social traction
   * LCA advantage or risk
   * Overall investment attractiveness

---

### **Output Structure**

#### 1. **Graph Representation Summary**

List relationships using natural language:

* **[Trend]** influences **[Company]**
* **[Company]** collaborates with **[Company]**
* **[Company]** competes with **[Company]**

#### 2. **Social Signal Scoring**

For each company, provide:

* **Signal Strength**: High / Medium / Low
* **Key Influencers**: (names or profiles)
* **Trending Sentiment**: Positive / Neutral / Negative

#### 3. **Life Cycle Impact Summary**

Evaluate based on provided data:

* **Carbon Footprint**: High / Medium / Low
* **Resource Efficiency**: Good / Moderate / Poor
* **Circularity Potential**: High / Medium / Low
* **Compliance Readiness**: Meets CSRD / SFDR / None

#### 4. **Investor Summary Card**

Example format:

```
Company: GreenTechX
Trend Fit: Climate Action, Circular Economy
Signal Strength: High
Influencers: @climateleader, @greentechfounder
Sentiment: Positive

LCA Summary:
- Carbon Footprint: Low
- Circularity: High
- CSRD Readiness: Yes

Investor Attractiveness: Strong early-stage signal, aligned with EU Green Deal, leading positive sentiment.
```

#### 5. **Recommended Action**

Choose one:

* **Strong Candidate**
* **Monitor Closely**
* **Low Priority**
"""
        return template
