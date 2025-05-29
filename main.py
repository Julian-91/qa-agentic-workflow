from langgraph.graph import StateGraph
from state import AccessibilityScanState
from agents.accessibility_scan import accessibility_scan_node
from pprint import pprint

if __name__ == "__main__":

    graph = StateGraph(AccessibilityScanState)

    graph.add_node("accessibility_scan", accessibility_scan_node)

    graph.set_entry_point("accessibility_scan")

    app = graph.compile()

    # Voorbeeld input
    state = {"url": "https://www.w3.org/WAI/",
             "scan_results": None,
             "errors": None
             }

    result = app.invoke(state)

    print("Accessibility scan result:")
    pprint(result)