from langgraph.graph import StateGraph
from state import QaWorkflowState
from agents.accessibility_scan import accessibility_scan_node
from agents.security_scan import security_scan_node
from agents.test_design import test_design_node
from pprint import pprint

if __name__ == "__main__":
    graph = StateGraph(QaWorkflowState)

    graph.add_node("test_design", test_design_node)
    graph.add_node("accessibility_scan", accessibility_scan_node)
    graph.add_node("security_scan", security_scan_node)

    graph.add_edge("test_design", "accessibility_scan")
    graph.add_edge("accessibility_scan", "security_scan")
    graph.set_entry_point("test_design")

    app = graph.compile()

    state = {
        "url": "https://www.w3.org/WAI/",
        "code": """
def add(a, b):
    \"\"\"Returns the sum of a and b\"\"\"
    return a + b
""",
        "description": "A function that adds two numbers and returns the result.",
        "accessibility_scan_results": None,
        "security_scan_results": None,
        "testcases": None,
        "errors": None
}

#     state = {
#         "code": """
# def add(a, b):
#     \"\"\"Returns the sum of a and b\"\"\"
#     return a + b
# """,
#         "description": "A function that adds two numbers and returns the result.",
#         "testcases": None,
#         "errors": None
#     }

#     graph = StateGraph(TestDesignState)

#     graph.add_node("test_design", test_design_node)

#     graph.set_entry_point("test_design")

#     app = graph.compile()

    result = app.invoke(state)

    print("Workflow results:")
    pprint(result)