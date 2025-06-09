from langgraph.graph import StateGraph, START, END
from states import QaWorkflowState
from agents.test_design import test_design_node
from agents.github_agent import github_agent_node
from agents.ui_test import ui_test_node
from agents.assign_worker import assign_worker_node
from agents.accessibility_test import accessibility_test_node
from agents.security_test import security_test_node
from pprint import pprint


graph_builder = StateGraph(QaWorkflowState)

graph_builder.add_node("github_agent", github_agent_node)
graph_builder.add_node("assign_worker", assign_worker_node)
graph_builder.add_node("test_design", test_design_node)
graph_builder.add_node("ui_test", ui_test_node)
graph_builder.add_node("accessibility_scan", accessibility_test_node)
graph_builder.add_node("security_scan", security_test_node)

graph_builder.add_edge(START, "github_agent")
graph_builder.add_edge("github_agent", "assign_worker")
graph_builder.add_edge("assign_worker", "test_design")
graph_builder.add_conditional_edges("test_design", lambda state: state.get("agents_needed", []), {
    "ui_test": "ui_test",
    "accessibility_scan": "accessibility_scan",
    "security_scan": "security_scan",
})
graph_builder.add_edge("ui_test", END)
graph_builder.add_edge("accessibility_scan", END)
graph_builder.add_edge("security_scan", END)


workflow = graph_builder.compile()

state = {
    "url": "http://localhost:4200/add",
    "repo": "https://github.com/Julian-91/angular-todo-app",
    "pr_number": 20,
    "issue_number": 19,
    "github_issue": None,
    "pr_code_changes": None,
    "agents_needed": None,
    "reasoning": None,
    "testcases": None,
    "ui_test_results": None,
    "errors": None
}

result = workflow.invoke(state)

print("Workflow results:")
pprint(result)