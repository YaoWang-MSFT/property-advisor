import openai
from typing import Any, Dict, List, Optional
from app.ai.tools.contract_reviewer import review_contract_tool, format_contract_review_response, get_contract_review_system_prompt

class AdvisorAgent:
    def __init__(self, openai_api_key: str, deployment_name: str, api_base: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.deployment_name = deployment_name
        self.api_base = api_base
        self.tools = {}
        self._setup_openai_client()

    def _setup_openai_client(self):
        openai.api_key = self.openai_api_key
        if self.api_base:
            openai.api_base = self.api_base

    def register_tool(self, name: str, tool_callable):
        self.tools[name] = tool_callable

    def infer(self, prompt: str, tools: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        # Prepare tools for the response API if any are specified
        tool_list = [self.tools[name] for name in tools] if tools else []
        # Call AOAI LLM using the responses API
        response = openai.ChatCompletion.create(
            deployment_id=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            tools=tool_list,
            **kwargs
        )
        return response

    def analyze_contract(self, file_content: str) -> Dict[str, Any]:
        """
        Analyze a property contract using the contract reviewer tool.
        
        Args:
            file_content: The text content of the contract to analyze
            
        Returns:
            Dict containing contract analysis with summary, highlights, warnings, and suggestions
        """
        try:
            # Get the system and user prompts from the tool
            tool_response = review_contract_tool(file_content)
            system_prompt = tool_response["system_prompt"]
            user_prompt = tool_response["user_prompt"]
            
            # Call OpenAI API with the prompts
            response = openai.ChatCompletion.create(
                deployment_id=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Lower temperature for more consistent analysis
                max_tokens=2000
            )
            
            # Extract the AI response
            ai_response = response.choices[0].message.content
            
            # Format and return the structured response
            return format_contract_review_response(ai_response)
            
        except Exception as e:
            return {
                "summary": f"Error analyzing contract: {str(e)}",
                "highlights": [],
                "warnings": [f"Analysis failed: {str(e)}"],
                "suggestions": ["Please try again or check the contract format"]
            }

# Initialize the global advisor agent (you may want to move this to a config or dependency injection)
# agent = AdvisorAgent(openai_api_key="your-api-key", deployment_name="your-deployment-name")
# agent.register_tool("contract_reviewer", review_contract_tool)
