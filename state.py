from typing import TypedDict, Optional, List

class QaWorkflowState(TypedDict):
    url: str
    code: Optional[str]
    description: Optional[str]
    accessibility_scan_results: Optional[dict]
    security_scan_results: Optional[dict]
    testcases: Optional[List[dict]]
    errors: Optional[List[str]]
