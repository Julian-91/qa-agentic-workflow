from langgraph.graph import StateGraph
from states import QaWorkflowState
from agents.accessibility_scan import accessibility_scan_node
from agents.security_scan import security_scan_node
from agents.test_design import test_design_node
from agents.github_agent import github_agent_node
from agents.ui_test import ui_test_node
from pprint import pprint

if __name__ == "__main__":
    graph = StateGraph(QaWorkflowState)

    graph.add_node("github_agent", github_agent_node)
    graph.add_node("test_design", test_design_node)
    graph.add_node("ui_test", ui_test_node)
    graph.add_node("accessibility_scan", accessibility_scan_node)
    graph.add_node("security_scan", security_scan_node)

    graph.add_edge("github_agent", "test_design")
    graph.add_edge("test_design", "ui_test")
    graph.add_edge("ui_test", "accessibility_scan")
    graph.add_edge("accessibility_scan", "security_scan")
    graph.set_entry_point("github_agent")

    app = graph.compile()

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

    result = app.invoke(state)

    print("Workflow results:")
    pprint(result)