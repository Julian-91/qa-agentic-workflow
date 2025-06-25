from langgraph.graph import StateGraph, START, END
from states import QaWorkflowState
from agents.test_design import test_design_node
from agents.github_agent import github_agent_node
from agents.ui_test import ui_test_node
from agents.assign_worker import assign_worker_node
from agents.accessibility_test import accessibility_test_node
from agents.security_test import security_test_node
from agents.github_reporter import github_reporter_node
from pprint import pprint
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
import uuid

def human_approval_node(state: QaWorkflowState) -> QaWorkflowState:
    question = "Agents needed: " + str(state.get("agents_needed")) + "\nType 'approve' or 'reject': "
    answer = interrupt(question)

    if answer == "approve":
        return Command(goto="test_design", update={"decision": "approved"})
    elif answer == "reject":
        return Command(goto=END, update={"decision": "rejected"})

graph_builder = StateGraph(QaWorkflowState)

graph_builder.add_node("github_agent", github_agent_node)
graph_builder.add_node("assign_worker", assign_worker_node)
graph_builder.add_node("human_approval", human_approval_node)
graph_builder.add_node("test_design", test_design_node)
graph_builder.add_node("ui_test", ui_test_node)
graph_builder.add_node("accessibility_scan", accessibility_test_node)
graph_builder.add_node("security_scan", security_test_node)
graph_builder.add_node("github_reporter", github_reporter_node)

graph_builder.add_edge(START, "github_agent")
graph_builder.add_edge("github_agent", "assign_worker")
graph_builder.add_edge("assign_worker", "human_approval")
graph_builder.add_conditional_edges("test_design", lambda state: state.get("agents_needed", []), {
    "ui_test": "ui_test",
    "accessibility_scan": "accessibility_scan",
    "security_scan": "security_scan",
})
graph_builder.add_edge("ui_test", "github_reporter")
graph_builder.add_edge("accessibility_scan", "github_reporter")
graph_builder.add_edge("security_scan", "github_reporter")
graph_builder.add_edge("github_reporter", END)

checkpointer = MemorySaver()
workflow = graph_builder.compile(checkpointer=checkpointer)

state = {
    "url": "http://localhost:4200/add",
    "repo": "https://github.com/Julian-91/angular-todo-app",
    "pr_number": 20,
    "issue_number": 19,
    "github_issue": None,
    "pr_code_changes": None,
    "agents_needed": None,
    "reasoning": None,
    "ui_test_results": None,
    "decision": None,
    "errors": None
}

config = {"configurable": {"thread_id": uuid.uuid4()}}

result = workflow.invoke(state, config=config)

if '__interrupt__' in result:
    decision = input(result['__interrupt__'][0].value)  # This will print the question
    final_result = workflow.invoke(Command(resume=decision), config=config)
else:
    final_result = result

print("Workflow results:")
pprint(result)