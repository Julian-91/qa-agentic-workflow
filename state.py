from typing import TypedDict, Optional, List

class QaWorkflowState(TypedDict):
    url: str
    agents_needed: Optional[List[str]]
    accessibility_scan_results: Optional[dict]
    security_scan_results: Optional[dict]
    testcases: Optional[List[dict]]
    repo: str
    pr_number: int
    issue_number: Optional[int]
    github_issue: Optional[dict]
    pr_code_changes: Optional[str]
    ui_test_results: Optional[List[dict]]
    errors: Optional[List[str]]
