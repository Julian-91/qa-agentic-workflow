from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from state import QaWorkflowState
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import AIMessage

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

async def accessibility_scan(state: QaWorkflowState) -> dict:
    url = state["url"]
    async with mcp_client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent("gpt-4o-mini", tools)
        try:
            response = await agent.ainvoke({"messages": [{"role": "user", "content": f"Execute a accessibility scan on: {url}"}]})
            messages = response["messages"]
            ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
            scan_content = ai_message.content if ai_message else None
            return {
                "accessibility_scan_results": scan_content,
                "errors": None
            }
        except Exception as e:
            return {
                "accessibility_scan_results": None,
                "errors": [str(e)]
            }
        
def accessibility_scan_node(state: QaWorkflowState) -> QaWorkflowState:
    return asyncio.run(accessibility_scan(state))