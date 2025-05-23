"""
Strategy Hub Routes for SustainaTrend™ Platform

This module provides routes for the Strategy Hub, which offers tools and frameworks
for developing, analyzing, and implementing sustainability strategies.
"""

import logging
import json
import random
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
bp = Blueprint('strategy', __name__)

# Define strategy frameworks
STRATEGY_FRAMEWORKS = {
    "porters": {
        "name": "Porter's Five Forces",
        "description": "Assess competitive sustainability positioning by analyzing supplier power, buyer power, competitive rivalry, threat of substitution, and threat of new entry.",
        "dimensions": ["supplier_power", "buyer_power", "competitive_rivalry", "threat_of_substitution", "threat_of_new_entry"],
        "icon": "chart-bar",
    },
    "swot": {
        "name": "SWOT Analysis",
        "description": "Evaluate internal strengths and weaknesses alongside external opportunities and threats for sustainability initiatives.",
        "dimensions": ["strengths", "weaknesses", "opportunities", "threats"],
        "icon": "th-large",
    },
    "bcg": {
        "name": "BCG Growth-Share Matrix",
        "description": "Prioritize green investments and assets based on market growth rate and relative market share.",
        "dimensions": ["market_growth", "market_share"],
        "icon": "chart-pie",
    },
    "mckinsey": {
        "name": "McKinsey 9-Box Matrix",
        "description": "Rank real estate assets based on market attractiveness and competitive position for sustainability ROI.",
        "dimensions": ["market_attractiveness", "competitive_position"],
        "icon": "th",
    },
    "strategy_pyramid": {
        "name": "Strategy Pyramid",
        "description": "Define sustainability mission, objectives, strategies, and tactical plans in a hierarchical framework.",
        "dimensions": ["mission", "objectives", "strategies", "tactics"],
        "icon": "sort-amount-up",
    },
    "blue_ocean": {
        "name": "Blue Ocean Strategy",
        "description": "Create uncontested market space by focusing on sustainable innovation and differentiation.",
        "dimensions": ["eliminate", "reduce", "raise", "create"],
        "icon": "water",
    }
}

# Sample strategy data
SAMPLE_STRATEGIES = [
    {
        'id': 1,
        'name': 'Carbon Neutral Initiative',
        'description': 'Achieve carbon neutrality by 2025',
        'framework': 'Strategy Pyramid',
        'status': 'In Progress',
        'progress': 65,
        'metrics': {
            'carbon_reduction': 45,
            'renewable_energy': 60,
            'energy_efficiency': 75
        }
    },
    {
        'id': 2,
        'name': 'Circular Economy Program',
        'description': 'Implement circular economy principles',
        'framework': 'Blue Ocean Strategy',
        'status': 'Planning',
        'progress': 30,
        'metrics': {
            'waste_reduction': 25,
            'recycling_rate': 40,
            'material_efficiency': 35
        }
    },
    {
        'id': 3,
        'name': 'Sustainable Supply Chain',
        'description': 'Optimize supply chain for sustainability',
        'framework': 'Porter\'s Five Forces',
        'status': 'In Progress',
        'progress': 55,
        'metrics': {
            'supplier_sustainability': 50,
            'logistics_efficiency': 60,
            'carbon_footprint': 45
        }
    },
    {
        'id': 4,
        'name': 'Renewable Energy Transition',
        'description': 'Transition to 100% renewable energy',
        'framework': 'McKinsey 9-Box Matrix',
        'status': 'In Progress',
        'progress': 80,
        'metrics': {
            'renewable_percentage': 75,
            'cost_savings': 65,
            'emissions_reduction': 70
        }
    },
    {
        'id': 5,
        'name': 'Waste Reduction Initiative',
        'description': 'Reduce waste by 50% by 2024',
        'framework': 'SWOT Analysis',
        'status': 'Planning',
        'progress': 45,
        'metrics': {
            'waste_reduction': 40,
            'recycling_increase': 50,
            'cost_savings': 35
        }
    }
]

@bp.route('/')
def index():
    """Render the Strategy Hub main page."""
    try:
        logger.info("Rendering Strategy Hub main page")
        return render_template('strategy/strategy_hub.html',
                              active_nav='strategy',
                              frameworks=STRATEGY_FRAMEWORKS,
                              strategies=SAMPLE_STRATEGIES)
    except Exception as e:
        logger.error(f"Error rendering Strategy Hub: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/framework/<framework_id>')
def framework_detail(framework_id):
    """Render the framework detail page."""
    try:
        if framework_id not in STRATEGY_FRAMEWORKS:
            logger.warning(f"Framework not found: {framework_id}")
            return jsonify({'error': 'Framework not found'}), 404

        framework = STRATEGY_FRAMEWORKS[framework_id]

        # Get example strategies for this framework
        example_strategies = [s for s in SAMPLE_STRATEGIES if s['framework'] == framework['name']]

        logger.info(f"Rendering framework detail for {framework_id}")
        return render_template('strategy/framework_detail.html',
                              active_nav='strategy',
                              framework_id=framework_id,
                              framework=framework,
                              example_strategies=example_strategies)
    except Exception as e:
        logger.error(f"Error rendering framework detail: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/strategy/<int:strategy_id>')
def strategy_detail(strategy_id):
    """Render the strategy detail page."""
    try:
        # Find the strategy by ID
        strategy = next((s for s in SAMPLE_STRATEGIES if s['id'] == strategy_id), None)

        if not strategy:
            logger.warning(f"Strategy not found: {strategy_id}")
            return jsonify({'error': 'Strategy not found'}), 404

        logger.info(f"Rendering strategy detail for {strategy_id}")
        return render_template('strategy/strategy_detail.html',
                              active_nav='strategy',
                              strategy=strategy)
    except Exception as e:
        logger.error(f"Error rendering strategy detail: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/strategy/<int:strategy_id>/edit')
def strategy_edit(strategy_id):
    """Render the strategy edit page."""
    try:
        # Find the strategy by ID
        strategy = next((s for s in SAMPLE_STRATEGIES if s['id'] == strategy_id), None)

        if not strategy:
            logger.warning(f"Strategy not found: {strategy_id}")
            return jsonify({'error': 'Strategy not found'}), 404

        logger.info(f"Rendering strategy edit for {strategy_id}")
        return render_template('strategy/strategy_edit.html',
                              active_nav='strategy',
                              strategy=strategy,
                              frameworks=STRATEGY_FRAMEWORKS)
    except Exception as e:
        logger.error(f"Error rendering strategy edit page: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/create-strategy', methods=['POST'])
def create_strategy():
    """Create a new strategy."""
    try:
        framework_id = request.form.get('framework_id')
        strategy_name = request.form.get('strategy_name')
        strategy_description = request.form.get('strategy_description')

        if not framework_id or not strategy_name:
            logger.warning("Missing required fields for strategy creation")
            return jsonify({'error': 'Missing required fields'}), 400

        if framework_id not in STRATEGY_FRAMEWORKS:
            logger.warning(f"Framework not found: {framework_id}")
            return jsonify({'error': 'Framework not found'}), 404

        # In a real application, we would save the strategy to a database
        # For now, we'll just redirect back to the strategy hub
        logger.info(f"Strategy creation requested: {strategy_name} using framework {framework_id}")

        return redirect(url_for('strategy.index'))
    except Exception as e:
        logger.error(f"Error creating strategy: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Error creating strategy: {str(e)}'}), 500

@bp.route('/strategy/<int:strategy_id>/update', methods=['POST'])
def update_strategy(strategy_id):
    """Update an existing strategy."""
    try:
        # Find the strategy by ID
        strategy = next((s for s in SAMPLE_STRATEGIES if s['id'] == strategy_id), None)

        if not strategy:
            logger.warning(f"Strategy not found: {strategy_id}")
            return jsonify({'error': 'Strategy not found'}), 404

        # In a real application, we would update the strategy in the database
        # For now, we'll just redirect back to the strategy detail page
        logger.info(f"Strategy update requested for ID: {strategy_id}")

        return redirect(url_for('strategy.strategy_detail', strategy_id=strategy_id))
    except Exception as e:
        logger.error(f"Error updating strategy: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Error updating strategy: {str(e)}'}), 500

@bp.route('/api/frameworks')
def api_frameworks():
    """API endpoint for strategy frameworks."""
    try:
        return jsonify(STRATEGY_FRAMEWORKS)
    except Exception as e:
        logger.error(f"Error in API frameworks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/strategies')
def api_strategies():
    """API endpoint for strategies."""
    try:
        return jsonify(SAMPLE_STRATEGIES)
    except Exception as e:
        logger.error(f"Error in API strategies: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/execute')
def strategy_execute():
    """Render the strategy execution page."""
    try:
        logger.info("Rendering strategy execution page")
        return render_template('strategy/strategy_execute.html',
                              active_nav='strategy',
                              strategies=SAMPLE_STRATEGIES)
    except Exception as e:
        logger.error(f"Error rendering strategy execution page: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/storytelling')
def strategy_storytelling():
    """Render the strategy storytelling page."""
    try:
        logger.info("Rendering strategy storytelling page")
        return render_template('strategy/strategy_storytelling.html',
                              active_nav='strategy',
                              strategies=SAMPLE_STRATEGIES)
    except Exception as e:
        logger.error(f"Error rendering strategy storytelling page: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/story/<story_id>')
def view_shared_story(story_id):
    """View a shared story."""
    try:
        logger.info(f"Viewing shared story: {story_id}")
        return render_template('strategy/strategy_shared_story.html',
                              active_nav='strategy',
                              story_id=story_id)
    except Exception as e:
        logger.error(f"Error viewing shared story: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': f'Template rendering failed: {str(e)}'}), 500

@bp.route('/storytelling-api', methods=['POST'])
def storytelling_api():
    """API endpoint for strategy storytelling analysis."""
    try:
        # Get request data
        data = request.get_json()
        strategy_id = int(data.get('strategy_id'))
        data_source = data.get('data_source')
        narrative_type = data.get('narrative_type', 'impact')
        audience = data.get('audience', 'stakeholders')

        logger.info(f"Generating storytelling for strategy {strategy_id} with data source {data_source}")

        # Find the strategy by ID
        strategy = next((s for s in SAMPLE_STRATEGIES if s['id'] == strategy_id), None)

        if not strategy:
            logger.warning(f"Strategy not found: {strategy_id}")
            return jsonify({'error': 'Strategy not found'}), 404

        # Generate mock data for the storytelling
        result = generate_storytelling_results(strategy, data_source, narrative_type, audience)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error generating storytelling: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': str(e)}), 500

@bp.route('/execute-api', methods=['POST'])
def execute_strategy_api():
    """API endpoint for executing a strategy."""
    try:
        # Get request data
        data = request.get_json()
        strategy_id = int(data.get('strategy_id'))
        data_source = data.get('data_source')
        time_period = data.get('time_period', '1y')
        visualization_type = data.get('visualization_type', 'bar')

        logger.info(f"Executing strategy {strategy_id} with data source {data_source}")

        # Find the strategy by ID
        strategy = next((s for s in SAMPLE_STRATEGIES if s['id'] == strategy_id), None)

        if not strategy:
            logger.warning(f"Strategy not found: {strategy_id}")
            return jsonify({'error': 'Strategy not found'}), 404

        # Generate mock data for the strategy execution
        # In a real application, this would be replaced with actual data processing
        result = generate_strategy_results(strategy, data_source, time_period)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error executing strategy: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({'error': str(e)}), 500

def generate_strategy_results(strategy, data_source, time_period):
    """Generate mock results for strategy execution."""
    # Define time periods
    periods = {
        '1y': 12,
        '2y': 24,
        '5y': 60,
        'all': 120
    }
    num_periods = periods.get(time_period, 12)

    # Generate labels (months)
    current_date = datetime.now()
    labels = []
    for i in range(num_periods, 0, -1):
        month_date = current_date - timedelta(days=30 * i)
        labels.append(month_date.strftime('%b %Y'))

    # Generate datasets based on strategy metrics
    primary_datasets = []
    for metric, value in strategy['metrics'].items():
        # Generate random data with an upward trend
        data = []
        base_value = max(10, value - 40)
        for i in range(num_periods):
            trend_factor = i / num_periods  # Increases over time
            random_factor = random.uniform(-5, 5)
            point_value = base_value + (value - base_value) * trend_factor + random_factor
            data.append(round(point_value, 1))

        # Add dataset
        primary_datasets.append({
            'label': metric.replace('_', ' ').title(),
            'data': data,
            'backgroundColor': get_color_for_metric(metric, 0.7),
            'borderColor': get_color_for_metric(metric, 1),
            'borderWidth': 1
        })

    # Generate radar chart data
    radar_labels = list(strategy['metrics'].keys())
    radar_data = [strategy['metrics'][metric] for metric in radar_labels]

    # Format radar labels
    radar_labels = [label.replace('_', ' ').title() for label in radar_labels]

    # Create table data
    table_headers = ['Period'] + [ds['label'] for ds in primary_datasets]
    table_rows = []

    # Group data by period
    for i, period in enumerate(labels):
        row = [period]
        for dataset in primary_datasets:
            row.append(dataset['data'][i])
        table_rows.append(row)

    # Generate insights based on strategy and data
    insights = generate_insights(strategy, data_source)

    # Create summary text
    summary = f"""
    <p class="mb-2">Analysis of <strong>{strategy['name']}</strong> using <strong>{data_source.replace('_', ' ').title()}</strong> data.</p>
    <p class="mb-2">The strategy is currently <strong>{strategy['status']}</strong> with <strong>{strategy['progress']}%</strong> completion.</p>
    <p>Based on the {data_source.replace('_', ' ')} data, we can see trends in {', '.join([metric.replace('_', ' ') for metric in strategy['metrics']])}.
    The data shows a positive correlation between implementation progress and metric improvements.</p>
    """

    return {
        'summary': summary,
        'primary_chart': {
            'labels': labels,
            'datasets': primary_datasets
        },
        'secondary_chart': {
            'labels': radar_labels,
            'datasets': [{
                'label': 'Current Metrics',
                'data': radar_data,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'pointBackgroundColor': 'rgba(75, 192, 192, 1)',
                'pointBorderColor': '#fff',
                'pointHoverBackgroundColor': '#fff',
                'pointHoverBorderColor': 'rgba(75, 192, 192, 1)'
            }]
        },
        'table_data': {
            'headers': table_headers,
            'rows': table_rows
        },
        'insights': insights
    }

def get_color_for_metric(metric, alpha=1.0):
    """Get a color for a specific metric."""
    colors = {
        'carbon_reduction': f'rgba(75, 192, 192, {alpha})',
        'renewable_energy': f'rgba(54, 162, 235, {alpha})',
        'energy_efficiency': f'rgba(153, 102, 255, {alpha})',
        'waste_reduction': f'rgba(255, 159, 64, {alpha})',
        'recycling_rate': f'rgba(255, 99, 132, {alpha})',
        'material_efficiency': f'rgba(255, 206, 86, {alpha})',
        'supplier_sustainability': f'rgba(75, 192, 192, {alpha})',
        'logistics_efficiency': f'rgba(54, 162, 235, {alpha})',
        'carbon_footprint': f'rgba(255, 99, 132, {alpha})',
        'renewable_percentage': f'rgba(54, 162, 235, {alpha})',
        'cost_savings': f'rgba(255, 206, 86, {alpha})',
        'emissions_reduction': f'rgba(75, 192, 192, {alpha})',
        'recycling_increase': f'rgba(153, 102, 255, {alpha})'
    }

    return colors.get(metric, f'rgba(128, 128, 128, {alpha})')

def generate_storytelling_results(strategy, data_source, narrative_type, audience):
    """Generate mock results for strategy storytelling."""
    # Define the contagious framework elements
    contagious_elements = {
        'social_currency': {
            'score': random.randint(60, 95),
            'description': 'How sharing this information makes people look to others',
            'recommendation': 'Highlight unique or surprising aspects of your sustainability initiatives'
        },
        'triggers': {
            'score': random.randint(55, 90),
            'description': 'Environmental cues that prompt people to think about your product or idea',
            'recommendation': 'Connect your sustainability story to daily activities or current events'
        },
        'emotion': {
            'score': random.randint(65, 95),
            'description': 'How the content evokes feelings, especially high-arousal emotions',
            'recommendation': 'Focus on the positive impact and hopeful future your initiatives create'
        },
        'public': {
            'score': random.randint(50, 85),
            'description': 'Visibility of the behavior or adoption',
            'recommendation': 'Create visible symbols or actions that demonstrate commitment to your strategy'
        },
        'practical_value': {
            'score': random.randint(70, 95),
            'description': 'Useful information people want to share with others',
            'recommendation': 'Provide actionable insights or tips related to sustainability'
        },
        'stories': {
            'score': random.randint(65, 90),
            'description': 'Narrative structure that carries information and meaning',
            'recommendation': 'Frame your data within a compelling narrative with characters and conflict'
        }
    }

    # Generate narrative based on type
    narrative_templates = {
        'impact': f"""
            <h3>Impact Narrative</h3>
            <p>The {strategy['name']} has demonstrated significant positive impact across multiple dimensions of sustainability.
            Since implementation began, we've seen a {random.randint(20, 40)}% improvement in overall sustainability metrics.</p>

            <p>Key achievements include:</p>
            <ul>
                {''.join([f'<li>{metric.replace("_", " ").title()}: {value}% improvement</li>' for metric, value in strategy['metrics'].items()])}
            </ul>

            <p>These improvements translate to tangible benefits for our stakeholders, including cost savings,
            risk reduction, and enhanced reputation. The data clearly shows that our strategic approach is working.</p>
        """,
        'challenge': f"""
            <h3>Challenge Narrative</h3>
            <p>Implementing the {strategy['name']} hasn't been without obstacles. We faced significant challenges in
            {random.choice(['securing stakeholder buy-in', 'technical implementation', 'resource allocation', 'regulatory compliance'])},
            which initially slowed our progress.</p>

            <p>Despite these challenges, we've made substantial headway:</p>
            <ul>
                {''.join([f'<li>Overcame {metric.replace("_", " ")} barriers to achieve {value}% progress</li>' for metric, value in strategy['metrics'].items()])}
            </ul>

            <p>This journey demonstrates our resilience and commitment to sustainability, even when faced with difficult circumstances.</p>
        """,
        'innovation': f"""
            <h3>Innovation Narrative</h3>
            <p>The {strategy['name']} represents a breakthrough approach to sustainability in our industry.
            By applying innovative methodologies and technologies, we've achieved results that were previously thought impossible.</p>

            <p>Our innovative approaches include:</p>
            <ul>
                {''.join([f'<li>Novel {metric.replace("_", " ")} techniques resulting in {value}% improvement</li>' for metric, value in strategy['metrics'].items()])}
            </ul>

            <p>These innovations position us as thought leaders in sustainability and create significant competitive advantage.</p>
        """,
        'journey': f"""
            <h3>Journey Narrative</h3>
            <p>Our sustainability journey with the {strategy['name']} began {random.randint(1, 5)} years ago with a simple vision:
            {strategy['description']}. Since then, we've evolved through multiple phases of implementation and learning.</p>

            <p>Key milestones in our journey:</p>
            <ul>
                {''.join([f'<li>Phase {i+1}: {metric.replace("_", " ").title()} initiative launched, achieving {value}% progress</li>' for i, (metric, value) in enumerate(strategy['metrics'].items())])}
            </ul>

            <p>This ongoing journey reflects our commitment to continuous improvement and long-term sustainability goals.</p>
        """
    }

    # Adjust narrative based on audience
    audience_adjustments = {
        'investors': {
            'focus': 'financial returns and risk mitigation',
            'metrics': ['ROI', 'cost savings', 'risk reduction', 'market positioning'],
            'language': 'business-oriented, focusing on value creation'
        },
        'customers': {
            'focus': 'product benefits and values alignment',
            'metrics': ['product improvements', 'health benefits', 'ethical sourcing', 'community impact'],
            'language': 'accessible and benefit-focused'
        },
        'employees': {
            'focus': 'organizational purpose and workplace improvements',
            'metrics': ['workplace conditions', 'employee engagement', 'skills development', 'purpose alignment'],
            'language': 'inclusive and mission-driven'
        },
        'regulators': {
            'focus': 'compliance and industry leadership',
            'metrics': ['standards compliance', 'emissions reduction', 'waste management', 'ethical practices'],
            'language': 'formal and detailed'
        },
        'stakeholders': {
            'focus': 'balanced approach to all interests',
            'metrics': ['balanced scorecard', 'multi-dimensional impact', 'long-term sustainability', 'stakeholder engagement'],
            'language': 'balanced and comprehensive'
        }
    }

    # Generate viral potential metrics based on contagious framework
    viral_potential = {
        'overall_score': sum([element['score'] for element in contagious_elements.values()]) / len(contagious_elements),
        'elements': contagious_elements
    }

    # Generate industry benchmarks for comparison
    industry_benchmarks = {
        'sustainability': {
            'name': 'Sustainability Sector',
            'overall_score': random.randint(65, 75),
            'elements': {
                'social_currency': random.randint(60, 70),
                'triggers': random.randint(65, 75),
                'emotion': random.randint(70, 80),
                'public': random.randint(55, 65),
                'practical_value': random.randint(70, 80),
                'stories': random.randint(60, 70)
            }
        },
        'finance': {
            'name': 'Financial Sector',
            'overall_score': random.randint(60, 70),
            'elements': {
                'social_currency': random.randint(55, 65),
                'triggers': random.randint(50, 60),
                'emotion': random.randint(45, 55),
                'public': random.randint(60, 70),
                'practical_value': random.randint(75, 85),
                'stories': random.randint(55, 65)
            }
        },
        'technology': {
            'name': 'Technology Sector',
            'overall_score': random.randint(70, 80),
            'elements': {
                'social_currency': random.randint(75, 85),
                'triggers': random.randint(65, 75),
                'emotion': random.randint(60, 70),
                'public': random.randint(70, 80),
                'practical_value': random.randint(75, 85),
                'stories': random.randint(65, 75)
            }
        },
        'top_performers': {
            'name': 'Top Performers',
            'overall_score': random.randint(85, 95),
            'elements': {
                'social_currency': random.randint(85, 95),
                'triggers': random.randint(80, 90),
                'emotion': random.randint(85, 95),
                'public': random.randint(80, 90),
                'practical_value': random.randint(85, 95),
                'stories': random.randint(85, 95)
            }
        }
    }

    # Generate data visualization for storytelling
    # Time series data showing progress over time
    months = 12
    time_labels = []
    current_date = datetime.now()
    for i in range(months, 0, -1):
        month_date = current_date - timedelta(days=30 * i)
        time_labels.append(month_date.strftime('%b %Y'))

    # Generate datasets for each metric
    story_datasets = []
    for metric, value in strategy['metrics'].items():
        # Generate data with a narrative arc (beginning, middle, end)
        data = []
        for i in range(months):
            # Create a narrative arc with challenges in the middle
            if i < months / 3:  # Beginning - slow start
                progress = value * (i / (months / 3)) * 0.3
            elif i < 2 * months / 3:  # Middle - challenges and breakthrough
                midpoint = months / 2
                distance_from_mid = abs(i - midpoint)
                volatility = 1 - (distance_from_mid / (months / 6))
                progress = value * 0.3 + (value * 0.4 * (i - months/3) / (months/3)) + (random.uniform(-10, 10) * volatility)
            else:  # End - acceleration to conclusion
                progress = value * 0.7 + (value * 0.3 * (i - 2*months/3) / (months/3))

            data.append(max(0, min(100, round(progress, 1))))

        # Add dataset
        story_datasets.append({
            'label': metric.replace('_', ' ').title(),
            'data': data,
            'backgroundColor': get_color_for_metric(metric, 0.7),
            'borderColor': get_color_for_metric(metric, 1),
            'borderWidth': 1
        })

    # Create the narrative based on selected type and audience
    selected_narrative = narrative_templates.get(narrative_type, narrative_templates['impact'])
    audience_info = audience_adjustments.get(audience, audience_adjustments['stakeholders'])

    # Adjust narrative for audience
    audience_paragraph = f"""
        <h3>Audience Considerations: {audience.title()}</h3>
        <p>This narrative is tailored for {audience}, focusing on {audience_info['focus']}.
        Key metrics of interest include {', '.join(audience_info['metrics'])}.
        The language is {audience_info['language']}.</p>
    """

    # Generate storytelling recommendations
    recommendations = [
        f"Focus on {contagious_elements['emotion']['recommendation']} to increase emotional engagement.",
        f"Improve social currency by {contagious_elements['social_currency']['recommendation']}.",
        f"Create stronger triggers by {contagious_elements['triggers']['recommendation']}.",
        f"Enhance practical value by {contagious_elements['practical_value']['recommendation']}.",
        f"Develop a more compelling narrative by {contagious_elements['stories']['recommendation']}.",
        f"Make your sustainability efforts more visible by {contagious_elements['public']['recommendation']}."
    ]

    # Create benchmark comparison chart data
    benchmark_labels = [element.replace('_', ' ').title() for element in contagious_elements.keys()]
    benchmark_datasets = [
        {
            'label': 'Your Narrative',
            'data': [element['score'] for element in contagious_elements.values()],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'pointBackgroundColor': 'rgba(75, 192, 192, 1)',
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': 'rgba(75, 192, 192, 1)'
        },
        {
            'label': 'Sustainability Sector',
            'data': [industry_benchmarks['sustainability']['elements'][element] for element in contagious_elements.keys()],
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'pointBackgroundColor': 'rgba(54, 162, 235, 1)',
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': 'rgba(54, 162, 235, 1)'
        },
        {
            'label': 'Top Performers',
            'data': [industry_benchmarks['top_performers']['elements'][element] for element in contagious_elements.keys()],
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'pointBackgroundColor': 'rgba(255, 99, 132, 1)',
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': 'rgba(255, 99, 132, 1)'
        }
    ]

    # Create overall benchmark comparison data
    overall_benchmark_data = {
        'your_score': viral_potential['overall_score'],
        'benchmarks': {
            'sustainability': industry_benchmarks['sustainability']['overall_score'],
            'finance': industry_benchmarks['finance']['overall_score'],
            'technology': industry_benchmarks['technology']['overall_score'],
            'top_performers': industry_benchmarks['top_performers']['overall_score']
        }
    }

    # Generate benchmark insights
    benchmark_insights = []
    your_score = viral_potential['overall_score']

    if your_score > industry_benchmarks['top_performers']['overall_score']:
        benchmark_insights.append("Your narrative's viral potential exceeds even top performers in the industry. This is exceptional!")
    elif your_score > industry_benchmarks['sustainability']['overall_score']:
        benchmark_insights.append("Your narrative's viral potential is above the sustainability sector average, positioning you as a leader in the space.")
    else:
        benchmark_insights.append("Your narrative's viral potential is below the sustainability sector average. Consider implementing the recommendations to improve.")

    # Compare individual elements to benchmarks
    for element, data in contagious_elements.items():
        element_name = element.replace('_', ' ').title()
        if data['score'] < industry_benchmarks['sustainability']['elements'][element] - 10:
            benchmark_insights.append(f"Your {element_name} score is significantly below industry average. Focus on improving this element.")
        elif data['score'] > industry_benchmarks['top_performers']['elements'][element] - 5:
            benchmark_insights.append(f"Your {element_name} score is approaching top performer levels. This is a key strength of your narrative.")

    return {
        'narrative': {
            'content': selected_narrative,
            'audience_considerations': audience_paragraph,
            'type': narrative_type,
            'audience': audience
        },
        'viral_potential': viral_potential,
        'story_chart': {
            'labels': time_labels,
            'datasets': story_datasets
        },
        'contagious_chart': {
            'labels': benchmark_labels,
            'datasets': benchmark_datasets
        },
        'benchmarks': {
            'data': overall_benchmark_data,
            'insights': benchmark_insights
        },
        'recommendations': recommendations
    }

def generate_insights(strategy, data_source):
    """Generate insights based on strategy and data source."""
    insights = []

    # General insights based on strategy type
    if strategy['framework'] == 'Strategy Pyramid':
        insights.append(f"The {strategy['name']} shows strong alignment between mission and objectives, with tactical implementation progressing as expected.")
        insights.append("Consider accelerating the implementation of energy efficiency measures to achieve greater cost savings.")

    elif strategy['framework'] == 'Porter\'s Five Forces':
        insights.append("Supplier sustainability initiatives are creating competitive advantage and reducing supply chain risks.")
        insights.append("Consider expanding supplier engagement to include Scope 3 emissions reduction targets.")

    elif strategy['framework'] == 'SWOT Analysis':
        insights.append("Strengths in waste reduction are offsetting weaknesses in recycling infrastructure.")
        insights.append("Opportunity to leverage improved sustainability metrics for marketing and stakeholder engagement.")

    elif strategy['framework'] == 'Blue Ocean Strategy':
        insights.append("The circular economy approach is creating uncontested market space with limited competition.")
        insights.append("Consider further investment in material innovation to strengthen differentiation.")

    elif strategy['framework'] == 'McKinsey 9-Box Matrix':
        insights.append("Renewable energy transition is positioned in the high-growth, high-share quadrant, indicating strong ROI potential.")
        insights.append("Consider divesting from low-performing sustainability initiatives to focus resources on high-impact areas.")

    # Data source specific insights
    if data_source == 'sustainability_metrics':
        insights.append("Sustainability metrics show consistent improvement over the analyzed time period.")
        insights.append("Consider setting more ambitious targets based on the positive trajectory of key metrics.")

    elif data_source == 'financial_data':
        insights.append("Financial returns from sustainability initiatives are exceeding expectations, with cost savings offsetting implementation expenses.")
        insights.append("Consider developing a more detailed ROI tracking system for individual sustainability projects.")

    elif data_source == 'market_trends':
        insights.append("Market trends indicate increasing consumer preference for sustainable products and services.")
        insights.append("Consider aligning marketing strategy more closely with sustainability achievements.")

    elif data_source == 'esg_ratings':
        insights.append("ESG ratings show improvement in environmental and governance categories, with social impact as an area for further development.")
        insights.append("Consider strengthening social impact initiatives to achieve balanced ESG performance.")

    elif data_source == 'carbon_emissions':
        insights.append("Carbon emissions reduction is on track to meet targets, with energy efficiency measures delivering the greatest impact.")
        insights.append("Consider implementing a more granular carbon accounting system to identify additional reduction opportunities.")

    return insights
