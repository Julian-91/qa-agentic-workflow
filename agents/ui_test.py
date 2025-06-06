from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from states import QaWorkflowState

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

class UiTestResult(BaseModel):
    title: str = Field(..., description="The title of the test case that was executed.")
    passed: bool = Field(..., description="Whether the test case passed (True) or failed (False).")
    details: str = Field(..., description="Details about the test execution, such as error messages or success info.")

class UiTestAgentOutput(BaseModel):
    ui_test_results: List[UiTestResult] = Field(..., description="A list of results for each executed UI test case.")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during UI test execution.")

async def run_ui_tests(state: QaWorkflowState) -> QaWorkflowState:
    url = state.get("url")
    testcases = state.get("testcases", [])
    async with mcp_client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent("gpt-4o-mini", tools, response_format=UiTestAgentOutput)
        response = await agent.ainvoke({"messages": [{"role": "user", "content": f"Use the Playwright tool to execute the following UI test on {url}. Testcases to execute: {testcases}\n Return a structured response with a list of results with each executed UI test case."}]})
    structured_response = response["structured_response"]
    return {
        "ui_test_results": structured_response.ui_test_results,
        "errors": structured_response.errors
    }

def ui_test_node(state: QaWorkflowState) -> QaWorkflowState:
    return asyncio.run(run_ui_tests(state))
