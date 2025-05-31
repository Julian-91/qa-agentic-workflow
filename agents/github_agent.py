from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any
from state import QaWorkflowState
import os
from langchain_core.messages import AIMessage

load_dotenv()

# Configureer de MCP client met de GitHub MCP server
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

# Maak een agent met de GitHub tool
agent = create_react_agent("gpt-4o-mini", tools)

def github_agent_node(state: QaWorkflowState) -> QaWorkflowState:
    repo = state.get("repo")
    pr_number = state.get("pr_number")
    issue_number = state.get("issue_number")
    try:
        prompt = (
            f"Call the GitHub tool to get the diff for pull request #{pr_number} in repository '{repo}'. "
            f"Then, call the GitHub tool to get the issue with number {issue_number} in the same repository. "
            "Return ONLY a valid JSON object with keys 'pr_code_changes' (containing the diff as a string) and 'github_issue' (an object with 'title' and 'description'). "
            "Do NOT include any explanation, markdown, or formatting. Only output the JSON object."
        )
        response = asyncio.run(
            agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
        )
        messages = response.get("messages", [])
        ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
        if ai_message is not None:
            import json
            try:
                result = json.loads(ai_message.content)
            except Exception:
                result = {"raw": ai_message.content}
            return {**state, **result}
        else:
            return {**state, "errors": ["No AIMessage found in response"]}
    except Exception as e:
        return {**state, "errors": [str(e)]}