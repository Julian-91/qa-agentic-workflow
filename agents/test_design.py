from langchain_openai import ChatOpenAI
import asyncio
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import json
from state import QaWorkflowState

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

async def generate_testcases(code: Optional[str], description: Optional[str]) -> List[dict]:
    prompt = "You are a test design assistant. "
    if code and description:
        prompt += (
            "Based on the following code AND description, generate a list of test cases. "
            "Use both sources for maximum coverage.\n\n"
            f"Code:\n{code}\n\nDescription:\n{description}\n"
        )
    elif code:
        prompt += f"Based on the following code, generate a list of test cases:\n{code}\n"
    elif description:
        prompt += f"Based on the following description, generate a list of test cases:\n{description}\n"
    prompt += (
        "Return ONLY a JSON array, where each testcase has 'title', 'steps', and 'expected_result'."
    )
    response = await llm.ainvoke(prompt)
    try:
        return json.loads(response.content)
    except Exception:
        return [response.content]
    
def test_design_node(state: QaWorkflowState) -> QaWorkflowState:
    code = state.get("code")
    description = state.get("description")
    testcases = asyncio.run(generate_testcases(code, description))
    return {**state, "testcases": testcases}
