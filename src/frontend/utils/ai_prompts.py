"""
AI Prompts Module for SustainaTrend™

This module contains all the prompts used for AI interactions in the application.
Centralizing prompts here makes them easier to maintain and update.
"""

from typing import Dict, Any

# Regulatory compliance assessment prompts
def get_framework_assessment_prompt(framework: Dict[str, Any], framework_id: str, categories: Dict[str, str]) -> str:
    """
    Generate a prompt for framework assessment.
    
    Args:
        framework: Framework details
        framework_id: Framework ID
        categories: Framework categories
        
    Returns:
        str: The generated prompt
    """
    return f"""
    You are an expert in sustainability reporting and regulatory compliance.
    You need to assess a document's compliance with the {framework.get('full_name', framework_id)} framework.
    
    Framework details:
    - Full name: {framework.get('full_name', framework_id)}
    - Description: {framework.get('description', 'No description available')}
    - Categories to assess: {categories}
    
    Provide a structured assessment with:
    1. Overall compliance score (0-100)
    2. Score for each category (0-100)
    3. Findings for each category
    4. Recommendations for each category
    5. Overall findings and recommendations
    
    Format your response as a JSON object with the following structure:
    {{
        "framework": "Full framework name",
        "framework_id": "Framework ID",
        "date": "Assessment date (ISO format)",
        "overall_score": "Overall score (0-100)",
        "categories": {{
            "category_id": {{
                "score": "Score for this category (0-100)",
                "compliance_level": "Compliance level description",
                "findings": ["Finding 1", "Finding 2"],
                "recommendations": ["Recommendation 1", "Recommendation 2"]
            }}
        }},
        "overall_findings": ["Finding 1", "Finding 2"],
        "overall_recommendations": ["Recommendation 1", "Recommendation 2"]
    }}
    """

def get_document_assessment_prompt(document_text: str, framework_name: str) -> str:
    """
    Generate a prompt for document assessment.
    
    Args:
        document_text: The document text to assess
        framework_name: Name of the framework
        
    Returns:
        str: The generated prompt
    """
    # Truncate document text to fit model context limits
    truncated_text = document_text[:48000]
    
    return f"""
    Document to assess:
    
    {truncated_text}
    
    Assess this document according to the {framework_name} framework.
    """

# RAG analysis prompts
def get_rag_analysis_prompt(contexts: list, query: str, framework_name: str) -> str:
    """
    Generate a prompt for RAG analysis.
    
    Args:
        contexts: Context information
        query: User query
        framework_name: Name of the framework
        
    Returns:
        str: The generated prompt
    """
    return f"""
    CONTEXT INFORMATION:
    {' '.join(contexts)}
    
    QUERY:
    {query}
    
    TASK:
    Based on the regulatory context information, please provide a detailed answer to the query.
    Focus on providing specific information from the document that addresses the query.
    If the context doesn't contain relevant information, state that clearly.
    
    FRAMEWORK:
    {framework_name}
    """

def get_follow_up_question_prompt(contexts: list, question: str) -> str:
    """
    Generate a prompt for follow-up questions.
    
    Args:
        contexts: Context information
        question: Follow-up question
        
    Returns:
        str: The generated prompt
    """
    return f"""
    CONTEXT INFORMATION:
    {' '.join(contexts)}
    
    FOLLOW-UP QUESTION:
    {question}
    
    TASK:
    Based on the regulatory context information, please provide a detailed answer to the follow-up question.
    Focus on providing specific information from the document that addresses the question.
    If the context doesn't contain relevant information, state that clearly.
    """

# Trend analysis prompts
def get_trend_analysis_prompt(trends_data: Dict[str, Any], user_role: str = "analyst") -> str:
    """
    Generate a prompt for trend analysis based on user role.
    
    Args:
        trends_data: Trend data
        user_role: User role (analyst or executive)
        
    Returns:
        str: The generated prompt
    """
    if user_role.lower() == "executive":
        return f"""
        You are a sustainability expert providing insights to an executive.
        
        Based on the following sustainability trend data:
        {trends_data}
        
        Provide a high-level summary of the most important trends and their business implications.
        Focus on strategic insights and actionable recommendations.
        Keep your response concise and executive-friendly.
        """
    else:  # Default to analyst
        return f"""
        You are a sustainability expert providing detailed analysis to an analyst.
        
        Based on the following sustainability trend data:
        {trends_data}
        
        Provide a detailed analysis of all trends, including:
        1. Trend momentum and growth trajectory
        2. Industry adoption patterns
        3. Regulatory implications
        4. Potential business impacts
        5. Detailed recommendations for action
        
        Include specific metrics and data points in your analysis.
        """
