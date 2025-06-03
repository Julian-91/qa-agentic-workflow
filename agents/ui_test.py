from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
from typing import List
from state import QaWorkflowState
from langchain_core.messages import AIMessage

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

async def run_ui_tests(state: QaWorkflowState) -> QaWorkflowState:
    url = state.get("url")
    testcases = state.get("testcases", [])
    results = []
    async with mcp_client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent("gpt-4o-mini", tools)
        for testcase in testcases:
            title = testcase.get("title")
            steps = testcase.get("steps")
            prompt = (
                f"Use the Playwright tool to execute the following UI test on {url}:\n"
                f"Testcase: {title}\n"
                f"Steps:\n" + "\n".join(steps) + "\n"
                "Return ONLY a JSON object with keys 'title', 'passed' (true/false), and 'details' (string with error or success info)."
                "Do NOT include any explanation, markdown, or formatting."
            )
            response = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
            messages = response.get("messages", [])
            ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
            if ai_message is not None:
                import json
                try:
                    result = json.loads(ai_message.content)
                except Exception:
                    result = {"title": title, "passed": False, "details": ai_message.content}
                results.append(result)
            else:
                results.append({"title": title, "passed": False, "details": "No AIMessage found in response"})
    return {**state, "ui_test_results": results}

def ui_test_node(state: QaWorkflowState) -> QaWorkflowState:
    return asyncio.run(run_ui_tests(state))