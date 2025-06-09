from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from states import QaWorkflowState

load_dotenv()

class TestCase(BaseModel):
    title: str = Field(..., description="A short, descriptive title for the test case.")
    steps: List[str] = Field(..., description="A list of steps to execute the test case.")
    expected_result: str = Field(..., description="The expected outcome after executing the steps.")

class TestDesignAgentOutput(BaseModel):
    testcases_ui_test: List[TestCase] = Field(None, description="A list of generated test cases for the ui_test agent.")
    testcases_accessibility_test: List[TestCase] = Field(None, description="A list of generated test cases for the accessibility_scan agent.")
    testcases_security_test: List[TestCase] = Field(None, description="A list of generated test cases for the security_scan agent.")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during test case generation.")

def test_design_node(state: QaWorkflowState) -> QaWorkflowState:
    code = state.get("pr_code_changes")
    issue = state.get("github_issue")
    agents_needed = state.get("agents_needed", [])
    llm = ChatOpenAI(model="gpt-4o-mini")
    structured_llm = llm.with_structured_output(TestDesignAgentOutput)
    messages = [
        {"role": "system", "content": "You are a test design assistant. You are given a code diff and an issue description of a pull request. "
        "You generete test cases for the agents that are given to you."
        "For the ui_test agent, you need to generate test cases that cover the happy flow of the functionality."
        "For the accessibility_test agent, you need to generate test cases that cover the accessibility of the functionality."
        "For the security_test agent, you need to generate test cases that cover the security of the functionality."
        "The test cases should be suitable for the selected agent(s) and also be added to the list of testcases for the agent."},
        {"role": "user", "content": f"Based on the following code diff and issue description, "
        f"generate test cases ONLY for the following agent types: {', '.join(agents_needed)}. "
        f"Code diff: {code}. Issue description: {issue}"}
    ]
    response = structured_llm.invoke(messages)
    print(response)
    return {
        "testcases_ui_test": response.testcases_ui_test,
        "testcases_accessibility_test": response.testcases_accessibility_test,
        "testcases_security_test": response.testcases_security_test,
        "errors": response.errors
    }
