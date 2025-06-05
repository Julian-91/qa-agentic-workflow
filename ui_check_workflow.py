from langgraph.graph import StateGraph, START, END
from state import QaWorkflowState
from agents.test_design import test_design_node
from agents.github_agent import github_agent_node
from agents.ui_test import ui_test_node
from pprint import pprint


graph_builder = StateGraph(QaWorkflowState)

graph_builder.add_node("github_agent", github_agent_node)
graph_builder.add_node("test_design", test_design_node)
graph_builder.add_node("ui_test", ui_test_node)

graph_builder.add_edge(START, "github_agent")
graph_builder.add_edge("github_agent", "test_design")
graph_builder.add_edge("test_design", "ui_test")
graph_builder.add_edge("ui_test", END)


workflow = graph_builder.compile()

state = {
    "url": "http://localhost:4200/add",
    "repo": "https://github.com/Julian-91/angular-todo-app",
    "pr_number": 20,
    "issue_number": 19,
    "github_issue": None,
    "pr_code_changes": None,
    "accessibility_scan_results": None,
    "security_scan_results": None,
    "testcases": None,
    "ui_test_results": None,
    "errors": None
}

result = workflow.invoke(state)

print("Workflow results:")
pprint(result)