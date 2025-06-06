from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from states import QaWorkflowState
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

mcp_client =MultiServerMCPClient({
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ],
      "transport": "stdio"
    }
})

class AccessibilityTestResult(BaseModel):
    title: str = Field(..., description="The title of the test case that was executed.")
    passed: bool = Field(..., description="Whether the test case passed (True) or failed (False).")
    details: str = Field(..., description="Details about the test execution, such as error messages or success info.")

class AccessibilityTestAgentOutput(BaseModel):
    accessibility_test_results: List[AccessibilityTestResult] = Field(..., description="A list of results for each executed accessibility test case.")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during accessibility test execution.")

async def accessibility_scan(state: QaWorkflowState) -> dict:
    url = state["url"]
    async with mcp_client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent(model="gpt-4o-mini", tools=tools, response_format=AccessibilityTestAgentOutput)
        response = await agent.ainvoke({"messages": [{"role": "user", "content": f"Execute a accessibility scan on: {url}"}]})
    structured_response = response["structured_response"]
    return {
        "accessibility_scan_results": structured_response.accessibility_test_results,
        "errors": structured_response.errors
    }
        
def accessibility_scan_node(state: QaWorkflowState) -> QaWorkflowState:
    return asyncio.run(accessibility_scan(state))