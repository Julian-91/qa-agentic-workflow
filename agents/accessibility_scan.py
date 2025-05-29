from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from state import AccessibilityScanState
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

async def get_tools():
    return await mcp_client.get_tools()

tools = asyncio.run(get_tools())

agent = create_react_agent("gpt-4o-mini", tools)

def accessibility_scan_node(state: AccessibilityScanState) -> dict:
    url = state["url"]
    try:
        response = asyncio.run(
            agent.ainvoke({"messages": [{"role": "user", "content": f"Voer een accessibility scan uit op: {url}"}]})
        )
        messages = response["messages"]
        ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
        scan_content = ai_message.content if ai_message else None
        return {
            "scan_results": scan_content,
            "errors": None
        }
    except Exception as e:
        return {
            "scan_results": None,
            "errors": [str(e)]
        }