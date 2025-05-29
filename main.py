from langgraph.graph import StateGraph
from state import QaWorkflowState
from agents.accessibility_scan import accessibility_scan_node
from agents.security_scan import security_scan_node
from pprint import pprint

if __name__ == "__main__":
    graph = StateGraph(QaWorkflowState)

    graph.add_node("accessibility_scan", accessibility_scan_node)
    graph.add_node("security_scan", security_scan_node)

    graph.add_edge("accessibility_scan", "security_scan")
    graph.set_entry_point("accessibility_scan")

    app = graph.compile()

    state = {"url": "https://www.w3.org/WAI/",
        "accessibility_scan_results": None,
        "security_scan_results": None,
        "errors": None
    }

    result = app.invoke(state)

    print("Scan results:")
    pprint(result)