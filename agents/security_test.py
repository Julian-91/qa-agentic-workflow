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

mcp_client = MultiServerMCPClient({
    "playwright": {
        "command": "npx",
        "args": [
            "@playwright/mcp@latest"
        ],
        "transport": "stdio"
    }
})

class SecurityTestResult(BaseModel):
    title: str = Field(..., description="The title of the test case that was executed.")
    passed: bool = Field(..., description="Whether the test case passed (True) or failed (False).")
    details: str = Field(..., description="Details about the test execution, such as error messages or success info.")

class SecurityTestAgentOutput(BaseModel):
    security_test_results: List[SecurityTestResult] = Field(..., description="A list of results for each executed security test case.")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during security test execution.")

async def security_test(state: QaWorkflowState) -> dict:
    url = state["url"]
    testcases = state.get("testcases_security_test", [])
    async with mcp_client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent(model="gpt-4o-mini", tools=tools, response_format=SecurityTestAgentOutput)
        response = await agent.ainvoke({"messages": [{"role": "user", "content": f"You are a security testing agent. "
            f"Execute the following security test cases on: {url}\n"
            f"Testcases to execute: {testcases}\n"
            "For each test case, return a result object with keys 'title', 'passed' (true/false), and 'details' (string with error or success info). "}]})
        structured_response = response["structured_response"]
        return {
            "security_scan_results": structured_response.security_test_results,
            "errors": structured_response.errors
        }
        
def security_test_node(state: QaWorkflowState) -> QaWorkflowState:
    return asyncio.run(security_test(state))