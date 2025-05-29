from typing import TypedDict, Optional, List

class QaWorkflowState(TypedDict):
    url: str
    accessibility_scan_results: Optional[dict]
    security_scan_results: Optional[dict]
    errors: Optional[List[str]]
