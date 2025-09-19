from typing import Dict, Any
import json

def get_contract_review_system_prompt() -> str:
    """Get the system prompt for contract review."""
    return """You are an expert real estate contract reviewer with extensive knowledge of property law, lease agreements, and real estate transactions. Your role is to analyze contracts and provide comprehensive insights.

When reviewing a contract, you must:

1. **Summary**: Provide a clear, concise summary of the contract's main purpose and key terms
2. **Highlights**: Identify and list the most important clauses, terms, and conditions
3. **Warnings**: Flag any potentially problematic, unusual, or risky clauses that require attention
4. **Suggestions**: Offer actionable recommendations for improvements, negotiations, or clarifications

Focus on these key areas:
- Financial terms (rent, deposits, fees, penalties)
- Lease duration and renewal terms
- Maintenance and repair responsibilities
- Pet policies and restrictions
- Termination and eviction clauses
- Insurance and liability requirements
- Subletting and assignment rights
- Property condition and inspection terms

Always respond in JSON format with the following structure:
{
    "summary": "Brief overview of the contract",
    "highlights": ["Key point 1", "Key point 2", ...],
    "warnings": ["Warning 1", "Warning 2", ...],
    "suggestions": ["Suggestion 1", "Suggestion 2", ...]
}

Be thorough but concise. Focus on practical implications for the parties involved."""

def review_contract_tool(file_content: str) -> Dict[str, Any]:
    """
    Tool function for contract review that can be registered with the AdvisorAgent.
    
    Args:
        file_content: The text content of the contract to review
        
    Returns:
        Dict containing the contract review analysis
    """
    system_prompt = get_contract_review_system_prompt()
    
    user_prompt = f"""Please review the following property contract and provide your analysis:

CONTRACT CONTENT:
{file_content}

Please analyze this contract and provide your response in the specified JSON format."""
    
    # This would be called by the AdvisorAgent with the prompts
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "tool_name": "contract_reviewer"
    }

def format_contract_review_response(ai_response: str) -> Dict[str, Any]:
    """
    Parse and format the AI response into a structured contract review.
    
    Args:
        ai_response: Raw response from the AI model
        
    Returns:
        Structured contract review data
    """
    try:
        # Try to parse JSON response
        parsed_response = json.loads(ai_response)
        
        # Validate required fields
        required_fields = ["summary", "highlights", "warnings", "suggestions"]
        for field in required_fields:
            if field not in parsed_response:
                parsed_response[field] = []
        
        return parsed_response
        
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "summary": "Failed to parse AI response properly",
            "highlights": ["Review the raw response for details"],
            "warnings": ["Response parsing error occurred"],
            "suggestions": ["Please try again with a clearer contract format"],
            "raw_response": ai_response
        }

# Tool configuration for registration
CONTRACT_REVIEW_TOOL_CONFIG = {
    "name": "contract_reviewer",
    "description": "Analyzes property contracts to provide summaries, highlights, warnings, and suggestions",
    "function": review_contract_tool,
    "parameters": {
        "type": "object",
        "properties": {
            "file_content": {
                "type": "string",
                "description": "The text content of the contract to review"
            }
        },
        "required": ["file_content"]
    }
}
