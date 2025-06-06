from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any
from states import QaWorkflowState
import os
from langchain_core.messages import AIMessage
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

async def get_tools():
    return await mcp_client.get_tools()

tools = asyncio.run(get_tools())

class GithubResponse(BaseModel):
    pr_code_changes: str = Field(description="The code changes from the pull request")
    github_issue: str = Field(description="The content from the GitHub issue, only title and description")
    
def github_agent_node(state: QaWorkflowState) -> QaWorkflowState:
    repo = state.get("repo")
    pr_number = state.get("pr_number")
    issue_number = state.get("issue_number")
    agent = create_react_agent(model="gpt-4o-mini", tools=tools, response_format=GithubResponse)
    response =  asyncio.run(agent.ainvoke({"messages": [{"role": "user", "content": f"Call the GitHub tool to get the diff for pull request #{pr_number} in repository {repo}. Then, call the GitHub tool to get the issue with number #{issue_number} in the same repository. Return the code changes and the issue content in a structured response."}]}))
    structured_response = response["structured_response"]
    return {
        "pr_code_changes": structured_response.pr_code_changes,
        "github_issue": structured_response.github_issue
    }