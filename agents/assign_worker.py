from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from states import QaWorkflowState

load_dotenv()

class AssignWorkerAgentOutput(BaseModel):
    agents_needed: List[str] = Field(..., description="A list of agent names/IDs that should be assigned to this task.")
    reasoning: Optional[str] = Field(None, description="Explanation of why these agents were selected.")
    errors: Optional[List[str]] = Field(None, description="A list of error messages, if any occurred during agent assignment.")

def assign_worker_node(state: QaWorkflowState) -> QaWorkflowState:
    code = state.get("pr_code_changes")
    issue = state.get("github_issue")
    llm = ChatOpenAI(model="gpt-4o-mini")
    structured_llm = llm.with_structured_output(AssignWorkerAgentOutput)
    response = structured_llm.invoke("You are a QA manager. You are given a code diff and an issue description of a pull request. "
                                     "You need to assign the appropriate agents to test the pull request."
                                     "The agents are: \n"
                                     "- 'accessibility_scan': this a accessibility test agent\n"
                                     "- 'security_scan': this is a security test agent\n"
                                     "- 'ui_test': this is a UI test agent\n"
                                     "If the pull request cannot be tested with these agents, return an empty list.\n"
                                     f"Code diff: {code}. Issue description: {issue}")
    return {
        "agents_needed": response.agents_needed,
        "reasoning": response.reasoning,
        "errors": response.errors
    }
