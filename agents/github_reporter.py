from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any, List, Optional
from states import QaWorkflowState
import os
from pydantic import BaseModel, Field

load_dotenv()

mcp_client = MultiServerMCPClient({
   "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
      },
      "transport": "stdio",
    }
})

class GithubResponse(BaseModel):
    report: str = Field(description="The report of the test results, agents used and reasoning of the used agents")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during the report generation.")

async def run_github_reporter(state: QaWorkflowState) -> QaWorkflowState:
    repo = state.get("repo")
    pr_number = state.get("pr_number")
    agents_needed = state.get("agents_needed")
    reasoning = state.get("reasoning")
    ui_test_results = state.get("ui_test_results", [])
    accessibility_scan_results = state.get("accessibility_scan_results", [])
    security_test_results = state.get("security_test_results", [])
    all_test_results = ui_test_results + accessibility_scan_results + security_test_results
    async with mcp_client.session("github") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent(model="gpt-4o-mini", tools=tools, response_format=GithubResponse)
        response = await agent.ainvoke({"messages": [{"role": "user", "content": f"Use the GitHub tool to post a review comment on pull request #{pr_number} in repository {repo} with a report of the test results, agents used and reasoning of the used agents.\n"
                                                         f"The test results: {all_test_results}\n"
                                                         f"The agents used: {agents_needed}\n"
                                                         f"The reasoning of the used agents: ${reasoning}"}]})
    structured_response = response["structured_response"]
    return {
        "report": structured_response.report,
        "errors": structured_response.errors
    }

def github_reporter_node(state: QaWorkflowState) -> QaWorkflowState:
    return asyncio.run(run_github_reporter(state))