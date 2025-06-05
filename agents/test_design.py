from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.prebuilt import create_react_agent
from state import QaWorkflowState

load_dotenv()

class TestCase(BaseModel):
    title: str = Field(..., description="A short, descriptive title for the test case.")
    steps: List[str] = Field(..., description="A list of steps to execute the test case.")
    expected_result: str = Field(..., description="The expected outcome after executing the steps.")

class TestDesignAgentOutput(BaseModel):
    testcases: List[TestCase] = Field(..., description="A list of generated test cases for the given code/issue.")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during test case generation.")

def test_design_node(state: QaWorkflowState) -> QaWorkflowState:
    code = state.get("pr_code_changes")
    issue = state.get("github_issue")
    llm = ChatOpenAI(model="gpt-4o-mini")
    structured_llm = llm.with_structured_output(TestDesignAgentOutput)
    response = structured_llm.invoke(f"Based on the following code diff and issue description, generate a list of test cases. The test cases are for functional UI testing. Only create testcases that will cover the happy flow. Use both sources for maximum coverage. Code diff: {code}. Issue description: {issue}")
    return {
        "testcases": response.testcases,
        "errors": response.errors
    }
